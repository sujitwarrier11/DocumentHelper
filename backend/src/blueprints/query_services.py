import os
import chromadb
from quart import ResponseReturnValue, request, Blueprint
from chromadb.utils.embedding_functions.ollama_embedding_function import OllamaEmbeddingFunction


blueprint = Blueprint("query", __name__)


@blueprint.post("/query")
async def query() -> ResponseReturnValue:
    """query documents"""
    req = await request.get_json()
    if 'question' not in req:
        return {}, 400
    question = req['question']

    chromadb_host = os.getenv("CHROMA_DB_HOST", "localhost")
    chromadb_port = int(os.getenv("CHROMA_DB_PORT", "8000"))
    client = chromadb.HttpClient(chromadb_host, chromadb_port)
    collection = client.get_collection('documents')

    results = collection.query(
        query_texts=[question],
        n_results=1
    )
    print(results)

    prompt = """
      You are a research assistant who goes through the given context and provides factual answers to question. The below rules must be followed while answering the question:
        1) The answer must be obtained only from give context. you must not hallucinate answers.
        2) If the question is off topic the content or the context is empty, simply return the string, 'I cannot answer this question.'
        3) Think before answering and double check against the context for accuracy.

        This is the context to be used to answer the question:
        {context}
        
        This is the questin asked by the user:
        """

    return {
       "result": ""
    }, 200