from pydantic import (
    BaseModel
)


class RepoRequest(
    BaseModel
):
    repo_url: str


class ChatRequest(
    BaseModel
):
    repo_name: str
    question: str


class SearchResult(
    BaseModel
):
    repo_name: str
    file_name: str
    path: str
    node_type: str
    name: str
    content: str