from fastapi import APIRouter
from pydantic import BaseModel

from app.github.fetch_repo import clone_repo
from app.parser.parse_code import parse_repository
from app.parser.chunk_code import build_semantic_chunks

from app.embeddings.embed import (
    embed_chunks
)

from app.vectorstore.qdrant_store import (
    store_chunks
)

import os


router = APIRouter()


class RepoRequest(
    BaseModel
):
    repo_url: str


@router.post(
    "/analyze"
)
async def analyze_repo(
    request: RepoRequest
):

    # clone repo
    repo_path = clone_repo(
        request.repo_url
    )

    # extract repo name
    repo_name = os.path.basename(
        repo_path
    )

    # parse files
    parsed_files = (
        parse_repository(
            repo_path
        )
    )

    # build chunks
    chunks = (
        build_semantic_chunks(
            parsed_files
        )
    )

    # attach repo name
    for chunk in chunks:

        chunk[
            "repo_name"
        ] = repo_name


        print(
    "AFTER ASSIGN:",
    chunks[0]
)

    # embeddings
    embedded_chunks = (
        embed_chunks(
            chunks
        )
    )


    print(
    "AFTER EMBED:",
    embedded_chunks[0]
)

    # store in qdrant
    store_chunks(
        embedded_chunks
    )

    # prefer code chunks
    code_chunks = []

    for chunk in embedded_chunks:

        if (
            chunk.get(
                "node_type"
            )
            != "text"
        ):

            code_chunks.append(
                chunk
            )

    # sample output
    sample_chunks = (
        code_chunks[:10]
        if code_chunks
        else embedded_chunks[:10]
    )

    return {

        "message":
        "Parsing + chunking + embedding + qdrant completed",

        "repo_name":
        repo_name,

        "repo_path":
        repo_path,

        "parsed_files":
        len(
            parsed_files
        ),

        "total_chunks":
        len(
            chunks
        ),

        "embedded_chunks":
        len(
            embedded_chunks
        ),

        "sample_chunks":
        sample_chunks,
    }