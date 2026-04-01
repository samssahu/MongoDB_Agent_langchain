import warnings
warnings.filterwarnings("ignore")

import os
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_mongodb.agent_toolkit import (
    MONGODB_AGENT_SYSTEM_PROMPT,
    MongoDBDatabase,
    MongoDBDatabaseToolkit,
)
import dotenv

dotenv.load_dotenv()

MONGODB_URI = 'mongodb://localhost:27017/'
DB_NAME = 'stateWiseData'

EXTRA_INSTRUCTIONS = """
CRITICAL QUERY RULES - YOU MUST FOLLOW THESE:
1. ALL field names and string values MUST be wrapped in double quotes.
2. NEVER use unquoted identifiers in any query.
3. CORRECT:   { "$match": { "cropName": "Ground nut PeanutMung phalli" } }
4. INCORRECT: { "$match": { cropName: "Ground nut PeanutMung phalli" } }
5. Every key in the pipeline dict MUST be a quoted string.

The 'crops' collection has these exact fields:
- "_id"               : ObjectId
- "cropCode"          : String  (e.g. "A0402")
- "cropName"          : String  (e.g. "Ground nut PeanutMung phalli")
- "destinationClass"  : String  (e.g. "FOUNDATION I")
- "districtCode"      : String  (e.g. "362")
- "districtName"      : String  (e.g. "KHORDHA")
- "season"            : String  (e.g. "KHARIF (2023)")
- "stateCode"         : String  (e.g. "21")
- "stateName"         : String  (e.g. "Odisha")
- "varietyCode"       : String  (e.g. "A0402270")
- "varietyName"       : String  (e.g. "K 1812 (Kadiri Lepakshi)")
- "year"              : String  (e.g. "2023-24")
- "estimatedYield"    : Double
- "intakeQuantity"    : Int32
- "passQuantity"      : Int32
- "processedQuantity" : Int32
- "taggedQuantity"    : Int32
- "testedQuantity"    : Int32
- "usedQuantity"      : Double
- "createdAt"         : Date
- "updatedAt"         : Date
"""

class NaturalLanguageToMQL:
    def __init__(self):
        self.llm = ChatGroq(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0
        )
        self.system_message = MONGODB_AGENT_SYSTEM_PROMPT.format(top_k=5) + EXTRA_INSTRUCTIONS
        self.db_wrapper = MongoDBDatabase.from_connection_string(
                            MONGODB_URI,
                            database=DB_NAME,
                            include_collections=["crops"])
        self.toolkit = MongoDBDatabaseToolkit(db=self.db_wrapper, llm=self.llm)
        self.agent = create_react_agent(
                        self.llm,
                        self.toolkit.get_tools(),
                        prompt=self.system_message)

    def ask(self, query):
        self.messages = []
        events = self.agent.stream(
            {"messages": [("user", query)]},
            stream_mode="values",
        )
        for event in events:
            self.messages.extend(event["messages"])
        print("\n📊 Answer:", self.messages[-1].content)
        print("-" * 60)

def main():
    converter = NaturalLanguageToMQL()
    print("=" * 60)
    print("   🌾 MongoDB Crop Data Query Agent")
    print("   Type 'exit' or 'quit' to stop")
    print("=" * 60)

    while True:
        query = input("\n💬 Ask a question: ").strip()
        if not query:
            print("⚠️  Please enter a question.")
            continue
        if query.lower() in ("exit", "quit"):
            print("👋 Goodbye!")
            break
        converter.ask(query)

if __name__ == '__main__':
    main()
