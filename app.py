from flask import Flask, request, jsonify
import os
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from flask_cors import CORS  # Import CORS

app = Flask(_name_)
CORS(app)  # Enable CORS for all domains on all routes

# Set environment variables
os.environ['OPENAI_API_KEY'] = ''
os.environ['PINECONE_API_KEY'] = ''

# Initialize OpenAI LLM
llm = OpenAI(openai_api_key=os.environ['OPENAI_API_KEY'])

# Pinecone index name
index_name = "hackbangalore-rag-trial-01"

# Initialize Pinecone vector store
vectorstore = PineconeVectorStore(index_name=index_name, embedding=OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY']))

def extract_keywords_using_chatgpt(text):
    """
    Sends a request to ChatGPT to extract keywords from the provided text.

    :param text: The text from which keywords need to be extracted.
    """
    try:
        # Invoke the LLM to get the response, which is expected to be directly the keyword string
        response = llm.invoke(
            "Extract the main keywords from the following text and provide them as a comma-separated list. do not give more than 10 keywords Please prefix the keywords with 'Keywords:'. the text to extract keyword is, " + text
        )
        print("Response from ChatGPT:", response)  # Debug: Print the full response to verify its structure
        print("Type of response:", type(response))
        print("Content of response:", response)

        # Check if the response is directly usable
        # strip /n and /r from the response
        response = response.replace('\n', '').replace('\r', '')
        if isinstance(response, str) and response.startswith('Keywords:'):
            print("Response is directly usable")
            keywords = response[len('Keywords:'):].strip()
            return [keyword.strip() for keyword in keywords.split(',')]
        elif isinstance(response, dict) and 'text' in response:
            output = response['text'].strip()
            if output.startswith('Keywords:'):
                keywords = output[len('Keywords:'):].strip()
                return [keyword.strip() for keyword in keywords.split(',')]
        else:
            print("Unexpected response structure or no keywords prefix found")
            return []
    except Exception as e:
        print(f"Error processing response: {e}")
        return []

@app.route('/search_projects', methods=['POST'])
def search_projects():
    try:
        print("Request received")
        data = request.get_json()
        description = data.get('description', '')
        print(f"Description: {description}")
        
        # Extract keywords relevant to the description
        keywords = extract_keywords_using_chatgpt(description)
        
        # Perform a similarity search using the vector store with extracted keywords
        search_query = ' '.join(keywords)
        print(f"Search query: {search_query}")
        search_result = vectorstore.similarity_search(search_query)
        
        # Return the top 3 results, if more than 3 exist
        top_results = search_result[:3] if len(search_result) > 3 else search_result
        
        if top_results:
            response_data = [{"similarity_match": result.page_content} for result in top_results]
            return jsonify(response_data), 200
        else:
            return jsonify({'message': 'No results found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/investor_query', methods=['POST'])
def investor_query():
    try:
        data = request.get_json()
        document = data.get('document', '')
        query = data.get('query', '')
        
        # Ensure both document and query are provided
        if not document or not query:
            return jsonify({'error': 'Both document and query must be provided'}), 400

        # Create a prompt for the LLM
        prompt = f"Given the following document: {document}. Answer the following query within the context of this document only: {query}"
        
        # Invoke the LLM to get the response
        response = llm.invoke(prompt)
        return jsonify({'response': response}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if _name_ == '_main_':
    app.run(debug=True)
