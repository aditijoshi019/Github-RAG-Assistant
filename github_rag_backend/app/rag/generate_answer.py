import os

from dotenv import load_dotenv

from groq import Groq


load_dotenv()


client = Groq(
    api_key=os.getenv(
        "GROQ_API_KEY"
    )
)


def generate_answer(
    question: str,
    chunks
):

    if not chunks:

        return (
            "No relevant code found."
        )

    context_parts = []

    for chunk in chunks:

        context_parts.append(

            f"""
File: {chunk.get('path', '')}

Type: {chunk.get('node_type', '')}

Code:
{chunk.get('content', '')}
"""
        )

    context = "\n\n".join(
        context_parts
    )

    prompt = f"""
You are a senior software engineer.

Answer ONLY from the repository context.

If the answer cannot be found,
say:
"I could not find that in the repository."

Question:
{question}

Repository Context:
{context}
"""

    try:

        response = (
            client.chat.completions.create(

                model=
                "llama-3.3-70b-versatile",

                messages=[
                    {
                        "role":
                        "system",

                        "content":
                        "You are an expert software engineer."
                    },

                    {
                        "role":
                        "user",

                        "content":
                        prompt
                    }
                ],

                temperature=0.2,
            )
        )

        return (
            response
            .choices[0]
            .message
            .content
        )

    except Exception as e:

        return (
            f"LLM Error: {str(e)}"
        )