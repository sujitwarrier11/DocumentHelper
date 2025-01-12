"""Service use to upload file to vector store"""

import os
from quart import ResponseReturnValue, request, Blueprint
from quart_uploads import UploadSet
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_nomic.embeddings import NomicEmbeddings
import chromadb

blueprint = Blueprint("file", __name__)

media = UploadSet('media', default_dest=lambda app: app.instance_path)

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=300,
    chunk_overlap=50)


@blueprint.post("/file/upload")
async def upload_file() -> ResponseReturnValue:
    """Upload file and store it in vector store"""
    print("invoked")
    if 'file' not in await request.files:
        return {}, 415
    files = await request.files
    file = files['file']
    await file.save(f'./{file.filename}')
    loader = PyPDFLoader(f'./{file.filename}')
    docs = loader.load()
    splits = text_splitter.split_documents(docs)
    embedding = NomicEmbeddings(
        model="nomic-embed-text-v1.5",
        inference_mode="local"
    )
    chromadb_host = os.getenv("CHROMA_DB_HOST", "localhost")
    chromadb_port = int(os.getenv("CHROMA_DB_PORT", "8000"))
    client = chromadb.HttpClient(chromadb_host, chromadb_port)
    client.get_or_create_collection(
        "documents",
    )
    Chroma.from_documents(splits, embedding=embedding, client=client)
    return {}, 200
