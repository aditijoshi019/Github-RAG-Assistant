import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")
MAX_TOKENS = 300


def token_count(text):
    return len(encoding.encode(text))


def chunk_text(content):
    if not content:
        return []

    words = content.split()

    chunks = []
    current_chunk = []
    current_tokens = 0

    for word in words:
        word_tokens = token_count(word)

        if current_tokens + word_tokens > MAX_TOKENS:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_tokens = word_tokens
        else:
            current_chunk.append(word)
            current_tokens += word_tokens

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def build_semantic_chunks(parsed_files):
    semantic_chunks = []

    for file in parsed_files:

        # safer lookup
        file_type = file.get("type")

        # if missing, skip
        if not file_type:
            print("Skipping file missing type:", file)
            continue

        if file_type == "code":

            nodes = file.get("nodes", [])

            for node in nodes:

                pieces = chunk_text(
                    node.get("content", "")
                )

                for piece in pieces:
                    semantic_chunks.append(
                        {
                            "file_name": file["file_name"],
                            "path": file["path"],
                            "node_type": node.get("type"),
                            "name": node.get("name"),
                            "content": piece,
                        }
                    )

        elif file_type == "text":

            pieces = chunk_text(
                file.get("content", "")
            )

            for piece in pieces:
                semantic_chunks.append(
                    {
                        "file_name": file["file_name"],
                        "path": file["path"],
                        "node_type": "text",
                        "name": file["file_name"],
                        "content": piece,
                    }
                )

    return semantic_chunks