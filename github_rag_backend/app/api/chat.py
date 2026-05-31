from fastapi import (
    APIRouter
)

from pydantic import (
    BaseModel
)

from app.rag.retriever import (
    retrieve_chunks
)

from app.rag.generate_answer import (
    generate_answer
)

router = APIRouter()


class ChatRequest(
    BaseModel
):
    repo_name: str
    question: str


@router.post(
    "/chat"
)
async def chat(
    request: ChatRequest
):

    chunks = (
        retrieve_chunks(
            repo_name=
            request.repo_name,

            question=
            request.question,
        )
    )

    answer = (
        generate_answer(
            request.question,
            chunks,
        )
    )

    return {

        "repo_name":
        request.repo_name,

        "question":
        request.question,

        "matches":
        chunks,

        "answer":
        answer,
    }