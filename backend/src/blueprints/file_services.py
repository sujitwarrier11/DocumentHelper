"""Service use to upload file to vector store"""

import os
from quart import ResponseReturnValue, request, Blueprint
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_nomic.embeddings import NomicEmbeddings
import chromadb

blueprint = Blueprint("file", __name__)

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=300,
    chunk_overlap=50)


@blueprint.post("/file/upload")
async def upload_file() -> ResponseReturnValue:
    """Upload file and store it in vector store"""
    if 'file' not in await request.files:
        return {}, 415
    files = await request.files
    file = files['file']
    file_bytes = file.read()
    loader = PyPDFLoader(file_bytes)
    docs = loader.load()
    splits = text_splitter.split_documents(docs)
    embedding = NomicEmbeddings(
        model="nomic-embed-text-v1.5",
        inference_mode="local"
    )
    chromadb_host = os.getenv("CHROMA_DB_HOST", "localhost")
    chromadb_port = int(os.getenv("CHROMA_DB_PORT", "8000"))
    client = await chromadb.AsyncHttpClient(chromadb_host, chromadb_port)
    await client.get_or_create_collection(
        "documents",
        metadata={"hnsw:space": "cosine"}
    )
    Chroma.from_documents(splits, embedding=embedding, client=client)
    return {}, 200
