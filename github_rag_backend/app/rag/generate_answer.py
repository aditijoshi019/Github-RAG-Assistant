def generate_answer(
    question,
    chunks
):

    if not chunks:

        return (
            "No relevant code found."
        )

    lines = []

    for chunk in chunks:

        lines.append(
            f"""
FILE:
{chunk["path"]}

TYPE:
{chunk["node_type"]}

NAME:
{chunk["name"]}

CONTENT:
{chunk["content"]}
"""
        )

    context = "\n".join(
        lines
    )

    return (
        f"""
Question:
{question}

Relevant code:

{context}
"""
    )