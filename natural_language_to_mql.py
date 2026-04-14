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
6. If a query fails, rewrite it with ALL keys and values in double quotes and retry.

AGGREGATION FUNCTIONS - SUPPORT ALL THESE:
7. For SUM queries: Use { "$group": { "_id": null, "total": { "$sum": "$fieldName" } } }
8. For AVG queries: Use { "$group": { "_id": null, "average": { "$avg": "$fieldName" } } }
9. For MIN queries: Use { "$group": { "_id": null, "minimum": { "$min": "$fieldName" } } }
10. For MAX queries: Use { "$group": { "_id": null, "maximum": { "$max": "$fieldName" } } }
11. For COUNT queries: Use { "$group": { "_id": null, "count": { "$sum": 1 } } }
12. For GROUP BY: Use { "$group": { "_id": "$fieldName", "count": { "$sum": 1 } } }

SCOPE RULES:
13. You ONLY answer questions about the 'crops' collection.
14. If the question is completely unrelated to crops, agriculture, districts,
    seasons, yield, or any field in the crops collection, reply EXACTLY with:
    "This data is not available in the database."
15. Do NOT answer general knowledge, math, weather, coding, or non-database questions.

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
        try:
            self.messages = []
            events = self.agent.stream(
                {"messages": [("user", query)]},
                stream_mode="values",
            )
            for event in events:
                self.messages.extend(event["messages"])

            answer = self.messages[-1].content

            # Only check if agent explicitly said no data
            no_data_phrases = [
                "not available in the database",
                "no results", "no records", "no documents",
                "no data found", "could not find", "couldn't find",
            ]
            if any(phrase in answer.lower() for phrase in no_data_phrases):
                print("\n❌ Answer: This data is not available in the database.")
            else:
                print("\n📊 Answer:", answer)

        except Exception as e:
            print(f"\n⚠️  Something went wrong: {e}")

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