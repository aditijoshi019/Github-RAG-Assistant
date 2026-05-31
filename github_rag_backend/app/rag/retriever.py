from app.embeddings.embed import (
    create_embedding
)

from app.vectorstore.qdrant_store import (
    search_chunks
)


def retrieve_chunks(
    repo_name: str,
    question: str
):

    query_vector = (
        create_embedding(
            question
        )
    )

    results = (
        search_chunks(
            repo_name=
            repo_name,

            vector=
            query_vector,

            limit=5,
        )
    )

    chunks = []

    for item in results:

        chunks.append(
            item.payload
        )

    return chunks