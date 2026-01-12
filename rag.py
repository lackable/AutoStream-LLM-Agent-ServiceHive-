import json
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from llm import get_llm

VECTOR_STORE = None


def load_documents():
    with open("knowledge_base.json", "r") as f:
        data = json.load(f)

    docs = []
    for section, content in data.items():
        docs.append(
            Document(
                page_content=json.dumps(content),
                metadata={"section": section}
            )
        )
    return docs


def build_vector_store():
    global VECTOR_STORE

    docs = load_documents()

    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001"
    )

    VECTOR_STORE = FAISS.from_documents(docs, embeddings)


def query_rag(query: str) -> str:
    if VECTOR_STORE is None:
        build_vector_store()

    retriever = VECTOR_STORE.as_retriever()
    docs = retriever.invoke(query)


    context = "\n".join(d.page_content for d in docs)

    llm = get_llm()

    prompt = f"""
You are a helpful assistant for AutoStream.
Answer the question using ONLY the context below.

Context:
{context}

Question:
{query}
"""

    response = llm.invoke(prompt)
    return response.content
