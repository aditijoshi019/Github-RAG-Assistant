from sentence_transformers import (
    SentenceTransformer
)

# lightweight model
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def create_embedding(
    text: str
):

    if not text:
        return []

    vector = model.encode(
        text
    )

    return vector.tolist()


def embed_chunks(
    chunks
):

    embedded_chunks = []

    for chunk in chunks:

        content = chunk.get(
            "content",
            ""
        )

        vector = create_embedding(
            content
        )

        embedded_chunks.append(
            {
                **chunk,
                "embedding":
                vector
            }
        )

    return embedded_chunks