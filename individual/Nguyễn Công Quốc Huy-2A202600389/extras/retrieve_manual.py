from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import json
from langchain_text_splitters import RecursiveCharacterTextSplitter

import os
from dotenv import load_dotenv

load_dotenv()

OPEN_API_KEY = os.getenv("OPENAI_API_KEY")


def get_embeddings():
    return OpenAIEmbeddings(model="text-embedding-3-small",
                            api_key=OPEN_API_KEY)


def build_vectorstore(chunks, embeddings):
    return FAISS.from_texts(chunks, embeddings)


def load_vectorstore(path, embeddings):
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)

def ingest_service_manual(file_path, save_path="faiss_index"):

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    docs = []

    for d in data:
        content = d["content"]
        metadata = d["metadata"]

        docs.append({
            "text": content,
            "metadata": metadata
        })

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50
    )

    chunks = []

    for d in docs:
        split_texts = splitter.split_text(d["text"])
        for chunk in split_texts:
            chunks.append(chunk)

    embeddings = get_embeddings()
    vectorstore = build_vectorstore(chunks, embeddings)

    vectorstore.save_local(save_path)

class RAGRetriever:

    def __init__(self, index_path="C:\\Users\\NCQHuy\\Desktop\\AIThucChien\\LopSang\\final\\vinfast-chatbot\\tools\\faiss_index\\"):
        self.embeddings = get_embeddings()
        self.vs = load_vectorstore(index_path, self.embeddings)

    def search(self, query, k=3):
        docs = self.vs.similarity_search(query, k=k)
        return [d.page_content for d in docs]
    
retriever = None
retriever = RAGRetriever()

from langchain_core.tools import tool

@tool
def retrieve_service_manual_rag(query: str, model: str):
    """
    Retrieve relevant service manual documents using semantic search (RAG).
    Used after identifying root cause to guide repair steps.
    """

    global retriever
    if retriever is None:
        retriever = RAGRetriever()

    docs = retriever.search(f"{query} for {model}")

    return {
        "documents": docs
    }