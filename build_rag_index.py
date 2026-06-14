"""Build or rebuild the ChromaDB vector index from knowledge/*.md files."""

from config import ensure_openai_client
from rag import build_index, get_collection


def main() -> None:
    ensure_openai_client()
    before = get_collection().count()
    count = build_index(force_rebuild=True)
    print(f"RAG index rebuilt: {before} -> {count} chunks in {get_collection().name}")


if __name__ == "__main__":
    main()
