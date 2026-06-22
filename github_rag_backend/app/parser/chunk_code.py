import tiktoken

encoding = (
    tiktoken.get_encoding(
        "cl100k_base"
    )
)

MAX_TOKENS = 500


def token_count(text):

    return len(
        encoding.encode(
            text
        )
    )


def split_tokens(
    text,
    overlap=50,
):

    tokens = (
        encoding.encode(
            text
        )
    )

    chunks = []

    start = 0

    while (
        start
        < len(tokens)
    ):

        end = (
            start
            + MAX_TOKENS
        )

        piece = (
            encoding.decode(
                tokens[
                    start:end
                ]
            )
        )

        chunks.append(
            piece
        )

        start += (
            MAX_TOKENS
            - overlap
        )

    return chunks


def build_semantic_chunks(
    parsed_files,
):

    semantic_chunks = []

    for file in parsed_files:

        if (
            file["type"]
            == "code"
        ):

            for node in file[
                "nodes"
            ]:

                pieces = (
                    split_tokens(
                        node[
                            "content"
                        ]
                    )
                )

                for piece in pieces:

                    semantic_chunks.append(
                        {
                            "file_name":
                            file[
                                "file_name"
                            ],

                            "path":
                            file[
                                "path"
                            ],

                            "node_type":
                            node[
                                "type"
                            ],

                            "name":
                            node[
                                "name"
                            ],

                            "content":
                            piece,
                        }
                    )

        elif (
            file["type"]
            == "text"
        ):

            pieces = (
                split_tokens(
                    file[
                        "content"
                    ]
                )
            )

            for piece in pieces:

                semantic_chunks.append(
                    {
                        "file_name":
                        file[
                            "file_name"
                        ],

                        "path":
                        file[
                            "path"
                        ],

                        "node_type":
                        "text",

                        "name":
                        file[
                            "file_name"
                        ],

                        "content":
                        piece,
                    }
                )

    return semantic_chunks