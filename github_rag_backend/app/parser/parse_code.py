import os
from pathlib import Path

from app.parser.tree_parser import (
    parse_with_tree_sitter,
)

from app.parser.generic_parser import (
    parse_generic,
)


CODE_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
}


TEXT_EXTENSIONS = {
    ".md",
    ".txt",
    ".yaml",
    ".yml",
    ".json",
    ".toml",
}


def parse_repository(
    repo_path,
):

    parsed_files = []

    for root, dirs, files in os.walk(
        repo_path
    ):

        dirs[:] = [
            d
            for d in dirs
            if d
            not in {
                ".git",
                "__pycache__",
                "node_modules",
                ".venv",
                "venv",
            }
        ]

        for file_name in files:

            file_path = os.path.join(
                root,
                file_name,
            )

            ext = Path(
                file_name
            ).suffix.lower()

            try:

                with open(
                    file_path,
                    "r",
                    encoding="utf8",
                    errors="ignore",
                ) as f:

                    content = (
                        f.read()
                    )

            except Exception:
                continue

            relative_path = os.path.relpath(
                file_path,
                repo_path,
            )

            # CODE FILES
            if ext in CODE_EXTENSIONS:

                print(
                    "CODE FILE:",
                    relative_path,
                )

                nodes = (
                    parse_with_tree_sitter(
                        content,
                        ext,
                    )
                )

                print(
                    "NODES:",
                    len(nodes),
                )

                parsed_files.append(
                    {
                        "type":
                        "code",

                        "file_name":
                        file_name,

                        "path":
                        relative_path,

                        "nodes":
                        nodes,
                    }
                )

            # TEXT FILES
            elif (
                ext in TEXT_EXTENSIONS
                or file_name.startswith(
                    "."
                )
            ):

                parsed_files.append(
                    {
                        "type":
                        "text",

                        "file_name":
                        file_name,

                        "path":
                        relative_path,

                        "content":
                        parse_generic(
                            content
                        ),
                    }
                )

    return parsed_files