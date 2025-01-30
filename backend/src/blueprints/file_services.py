"""Service use to upload file to vector store"""

import os
from quart import ResponseReturnValue, request, Blueprint
from quart_uploads import UploadSet
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pypdf import PdfReader

import chromadb
import uuid

blueprint = Blueprint("file", __name__)

media = UploadSet("media", default_dest=lambda app: app.instance_path)

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=300, chunk_overlap=50
)


@blueprint.post("/file/upload")
async def upload_file() -> ResponseReturnValue:
    """Upload file and store it in vector store"""
    print("invoked")
    if "file" not in await request.files:
        return {}, 415
    files = await request.files
    file = files["file"]
    extension = file.filename.split(".")[-1]
    new_filename = str(uuid.uuid4())
    print(extension)
    await file.save(f"./{new_filename}.{extension}")
    loader = PdfReader(f"./{new_filename}.{extension}")
    print(len(loader.pages))
    pages = [page.extract_text() for page in loader.pages]
    splits = [text_splitter.split_text(page) for page in pages]
    split_docs: list[str] = []

    for split in splits:
        split_docs = [*split_docs, *split]

    chromadb_host = os.getenv("CHROMA_DB_HOST", "localhost")
    chromadb_port = int(os.getenv("CHROMA_DB_PORT", "8000"))
    client = chromadb.HttpClient(chromadb_host, chromadb_port)
    collection = client.get_or_create_collection(
        "documents",
    )

    # store each document in a vector embedding database
    for i, d in enumerate(split_docs):
        collection.add(ids=[str(uuid.uuid4())], documents=[d])
    return {}, 200
