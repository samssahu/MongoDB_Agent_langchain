# 🌾 MongoDB Crop Data Query Agent

A natural language to MongoDB Query Language (MQL) converter powered by LangChain and LLMs. This agent allows you to query crop data using plain English questions and automatically generates and executes MongoDB queries.

## Features

- **Natural Language Processing**: Ask questions in plain English
- **Intelligent Query Generation**: Automatically converts natural language to MongoDB queries
- **Crop Data Management**: Query agricultural crop data including:
  - Crop information (name, code, variety)
  - Geographic data (state, district)
  - Season and year information
  - Yield and quantity metrics
- **React Agent Architecture**: Uses LangChain's ReAct agent with MongoDB toolkit
- **User-Friendly Interface**: Interactive CLI for easy interaction

## Prerequisites

- Python 3.8+
- MongoDB running locally on `localhost:27017`
- API key for Groq LLM service
- Required Python packages (see Installation)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd agent-mongo
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   MONGODB_URI=mongodb://localhost:27017/
   ```

## Database Setup

This project requires a MongoDB database with the following structure:

### Database: `stateWiseData`
### Collection: `crops`

**Collection Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `_id` | ObjectId | Unique identifier |
| `cropCode` | String | Crop code (e.g., "A0402") |
| `cropName` | String | Crop name (e.g., "Ground nut PeanutMung phalli") |
| `destinationClass` | String | Classification (e.g., "FOUNDATION I") |
| `districtCode` | String | District code (e.g., "362") |
| `districtName` | String | District name (e.g., "KHORDHA") |
| `season` | String | Season (e.g., "KHARIF (2023)") |
| `stateCode` | String | State code (e.g., "21") |
| `stateName` | String | State name (e.g., "Odisha") |
| `varietyCode` | String | Variety code (e.g., "A0402270") |
| `varietyName` | String | Variety name (e.g., "K 1812 (Kadiri Lepakshi)") |
| `year` | String | Year (e.g., "2023-24") |
| `estimatedYield` | Double | Estimated yield |
| `intakeQuantity` | Int32 | Intake quantity |
| `passQuantity` | Int32 | Pass quantity |
| `processedQuantity` | Int32 | Processed quantity |
| `taggedQuantity` | Int32 | Tagged quantity |
| `testedQuantity` | Int32 | Tested quantity |
| `usedQuantity` | Double | Used quantity |
| `createdAt` | Date | Creation timestamp |
| `updatedAt` | Date | Last update timestamp |

## Usage

Run the interactive agent:

```bash
python natural_language_to_mql.py
```

### Example Queries

```
💬 Ask a question: How many crops are grown in Odisha?
📊 Answer: [Agent processes the question and returns results]

💬 Ask a question: Show me all groundnut varieties in the KHARIF season
📊 Answer: [Results with matching varieties]

💬 Ask a question: What is the total yield for rice in 2023-24?
📊 Answer: [Aggregated yield data]
```

Type `exit` or `quit` to stop the agent.

## Architecture

### Components

1. **NaturalLanguageToMQL Class**
   - Initializes the Groq LLM with Llama model
   - Sets up MongoDB connection and toolkit
   - Creates a ReAct agent for query processing

2. **Query Processing Flow**
   - User input → LLM processing
   - Natural language → MQL generation
   - MongoDB execution → Results presentation

3. **System Prompt**
   - Enhanced with MongoDB-specific instructions
   - Includes critical query rules for proper MQL syntax
   - Provides schema information to the agent

## Query Rules

The agent follows strict rules for MongoDB query generation:

1. **All field names must be quoted** (double quotes)
2. **All string values must be quoted** (double quotes)
3. **Every key in the pipeline dict must be a quoted string**

Example (CORRECT):
```json
{ "$match": { "cropName": "Ground nut PeanutMung phalli" } }
```

Example (INCORRECT):
```json
{ "$match": { cropName: "Ground nut PeanutMung phalli" } }
```

## Configuration

Key configuration variables in `natural_language_to_mql.py`:

```python
MONGODB_URI = 'mongodb://localhost:27017/'
DB_NAME = 'stateWiseData'
MODEL_NAME = 'meta-llama/llama-4-scout-17b-16e-instruct'
TEMPERATURE = 0
```

## Dependencies

- `langchain-groq`: Groq LLM integration
- `langgraph`: Graph-based agent framework
- `langchain-mongodb`: MongoDB toolkit for LangChain
- `python-dotenv`: Environment variable management

## Troubleshooting

### MongoDB Connection Error
- Ensure MongoDB is running on `localhost:27017`
- Check MONGODB_URI in `.env` file

### API Key Error
- Verify `GROQ_API_KEY` is set in `.env` file
- Check that the API key is valid

### Query Errors
- Ensure all field names match the collection schema
- Check that the database and collection exist

## Project Structure

```
agent-mongo/
├── natural_language_to_mql.py  # Main agent implementation
├── .env                        # Environment variables (not tracked)
├── .gitignore                  # Git ignore rules
├── venv/                       # Virtual environment
└── README.md                   # This file
```

## License

MIT License - Feel free to use this project for educational and commercial purposes.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## Author

Created by [Your Name] - MongoDB Agent with LangChain

## Support

For issues or questions, please create an issue in the repository.
