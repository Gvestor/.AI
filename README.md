

---

# HackBangalore Rag Trial Project

## Overview

This Flask-based API service is designed to enhance content discoverability and interaction within a knowledge base or document corpus by leveraging advanced NLP techniques. The service uses LangChain's OpenAI module for natural language processing and Pinecone's vector database for semantic search capabilities.

## Features

- **Keyword Extraction:** Automatically extracts relevant keywords from text using OpenAI's language models.
- **Semantic Search:** Performs a vector-based similarity search to find related documents or entries in the database.
- **Investor Queries:** Provides answers to specific queries based on the context of a given document.

## Installation

To set up the project environment and run the server, follow these steps:

### Prerequisites

- Python 3.6+
- pip
- A valid OpenAI API key
- A valid Pinecone API key

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install dependencies:**
   ```bash
   pip install flask langchain_openai langchain_pinecone flask_cors
   ```

3. **Set environment variables:**
   ```bash
   export OPENAI_API_KEY='your-openai-api-key'
   export PINECONE_API_KEY='your-pinecone-api-key'
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

## Usage

The server starts on `http://localhost:5000`. It exposes two main API endpoints:

- **POST /search_projects**: Accepts a JSON payload with a `description` field and returns the top 3 semantically similar project descriptions.
  
  **Example Request:**
  ```json
  {
    "description": "sustainable energy solutions"
  }
  ```

- **POST /investor_query**: Accepts a JSON payload with `document` and `query` fields to answer queries based on the provided document.
  
  **Example Request:**
  ```json
  {
    "document": "This project aims to reduce carbon emissions by 40%...",
    "query": "What is the target reduction in emissions?"
  }
  ```

## Security

- Do not expose sensitive API keys in the code. Use environment variables or secure vault solutions to manage them.
- Enable CORS carefully, specific to the required domains to prevent misuse of the API from unauthorized sources.

