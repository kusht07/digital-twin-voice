"""ChromaDB-backed RAG: chunk knowledge files, embed, retrieve."""

from __future__ import annotations

import uuid
from pathlib import Path

import chromadb

import config
from chunking import chunk_text

ROOT = Path(__file__).parent
KNOWLEDGE_DIR = ROOT / "knowledge"
COLLECTION_NAME = "kush_memo"

DOCUMENTS = [
    {"file": "identity.md", "source": "Identity and Personal Context"},
    {"file": "career.md", "source": "Career History"},
    {"file": "technical.md", "source": "Technical Stack"},
]

_chroma_client: chromadb.ClientAPI | None = None
_collection: chromadb.Collection | None = None


def _get_chroma_client() -> chromadb.ClientAPI:
    global _chroma_client
    if _chroma_client is None:
        config.CHROMA_PATH.mkdir(parents=True, exist_ok=True)
        _chroma_client = chromadb.PersistentClient(path=str(config.CHROMA_PATH))
    return _chroma_client


def get_collection() -> chromadb.Collection:
    global _collection
    if _collection is None:
        _collection = _get_chroma_client().get_or_create_collection(COLLECTION_NAME)
    return _collection


def _load_documents() -> list[dict[str, str]]:
    docs: list[dict[str, str]] = []
    for spec in DOCUMENTS:
        path = KNOWLEDGE_DIR / spec["file"]
        if not path.is_file():
            raise FileNotFoundError(f"Knowledge file not found: {path}")
        docs.append({"text": path.read_text(encoding="utf-8"), "source": spec["source"]})
    return docs


def _chunk_documents(documents: list[dict[str, str]]) -> tuple[list[str], list[str], list[dict]]:
    chunks: list[str] = []
    ids: list[str] = []
    metadatas: list[dict] = []

    for doc in documents:
        doc_chunks = chunk_text(
            doc["text"],
            chunk_size=config.RAG_CHUNK_SIZE,
            overlap=config.RAG_CHUNK_OVERLAP,
        )
        ids.extend(str(uuid.uuid4()) for _ in doc_chunks)
        metadatas.extend(
            {"source": doc["source"], "chunk_index": i} for i in range(len(doc_chunks))
        )
        chunks.extend(doc_chunks)

    return chunks, ids, metadatas


def embed_texts(texts: list[str]) -> list[list[float]]:
    client = config.ensure_openai_client()
    response = client.embeddings.create(
        input=texts,
        model=config.EMBEDDING_MODEL,
    )
    return [item.embedding for item in response.data]


def build_index(*, force_rebuild: bool = False) -> int:
    """Index knowledge files into ChromaDB. Returns number of chunks stored."""
    config.ensure_openai_client()
    collection = get_collection()

    if force_rebuild:
        existing = collection.get()["ids"]
        if existing:
            collection.delete(ids=existing)

    if collection.count() > 0 and not force_rebuild:
        return collection.count()

    documents = _load_documents()
    chunks, ids, metadatas = _chunk_documents(documents)
    if not chunks:
        return 0

    embeddings = embed_texts(chunks)
    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
    )
    return len(chunks)


def ensure_index() -> None:
    """Build the vector index when the collection is empty."""
    if get_collection().count() == 0:
        count = build_index()
        print(f"Built RAG index with {count} chunks.")


def retrieve(query: str, n_results: int | None = None) -> tuple[str, list[dict]]:
    """Return joined context text and retrieval metadata for a user query."""
    config.ensure_openai_client()
    collection = get_collection()
    if collection.count() == 0:
        return "", []

    n = n_results if n_results is not None else config.RAG_N_RESULTS
    query_embedding = embed_texts([query])[0]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(n, collection.count()),
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    context = "\n\n".join(documents)
    return context, metadatas
