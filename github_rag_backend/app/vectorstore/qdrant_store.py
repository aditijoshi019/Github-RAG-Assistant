from qdrant_client import (
    QdrantClient
)

from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)

client = QdrantClient(
    host="localhost",
    port=6333,
)

COLLECTION_NAME = (
    "repo_chunks"
)


def create_collection():

    collections = (
        client.get_collections()
    )

    names = [
        c.name
        for c in collections.collections
    ]

    if (
        COLLECTION_NAME
        not in names
    ):

        client.create_collection(

            collection_name=
            COLLECTION_NAME,

            vectors_config=
            VectorParams(
                size=384,
                distance=
                Distance.COSINE,
            ),
        )


def store_chunks(
    embedded_chunks
):

    create_collection()

    points = []

    for index, chunk in enumerate(
        embedded_chunks
    ):
        
        print(
        "STORING:",
        chunk.get(
            "repo_name"
        )
    )


        vector = chunk.get(
            "embedding",
            []
        )

        if not vector:
            continue

        point = PointStruct(

            id=index,

            vector=vector,

            payload={

                "repo_name":
                chunk.get(
                    "repo_name",
                    ""
                ),

                "content":
                chunk.get(
                    "content",
                    ""
                ),

                "path":
                chunk.get(
                    "path",
                    ""
                ),

                "file_name":
                chunk.get(
                    "file_name",
                    ""
                ),

                "node_type":
                chunk.get(
                    "node_type",
                    ""
                ),

                "name":
                chunk.get(
                    "name",
                    ""
                ),
            }
        )

        points.append(
            point
        )

    if points:

        client.upsert(

            collection_name=
            COLLECTION_NAME,

            points=points,
        )


def search_chunks(
    repo_name: str,
    vector,
    limit=5
):

    results = client.search(

        collection_name=
        COLLECTION_NAME,

        query_vector=
        vector,

        limit=
        limit,

        query_filter=
        Filter(
            must=[
                FieldCondition(

                    key=
                    "repo_name",

                    match=
                    MatchValue(
                        value=
                        repo_name
                    ),
                )
            ]
        ),
    )

    return results