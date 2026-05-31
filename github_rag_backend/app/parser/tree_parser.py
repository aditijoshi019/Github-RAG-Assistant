from tree_sitter import (
    Parser,
    Language,
)

from tree_sitter_python import (
    language as py_lang,
)

from tree_sitter_javascript import (
    language as js_lang,
)

from tree_sitter_typescript import (
    language_typescript,
)


def get_language(ext):

    if ext == ".py":
        return Language(
            py_lang()
        )

    elif ext in {
        ".js",
        ".jsx",
    }:
        return Language(
            js_lang()
        )

    elif ext in {
        ".ts",
        ".tsx",
    }:
        return Language(
            language_typescript()
        )

    return None


def get_parser(ext):

    language = get_language(
        ext
    )

    if not language:
        return None

    parser = Parser()

    parser.language = (
        language
    )

    return parser


def walk_tree(
    node,
    content,
    nodes,
):

    if node.type in {
        "function_definition",
        "function_declaration",
        "method_definition",
    }:

        name_node = (
            node.child_by_field_name(
                "name"
            )
        )

        nodes.append(
            {
                "type":
                "function",

                "name":
                name_node.text.decode(
                    "utf8"
                )
                if name_node
                else "unknown",

                "content":
                content[
                    node.start_byte:
                    node.end_byte
                ],
            }
        )

    elif node.type in {
        "class_definition",
        "class_declaration",
    }:

        name_node = (
            node.child_by_field_name(
                "name"
            )
        )

        nodes.append(
            {
                "type":
                "class",

                "name":
                name_node.text.decode(
                    "utf8"
                )
                if name_node
                else "unknown",

                "content":
                content[
                    node.start_byte:
                    node.end_byte
                ],
            }
        )

    elif "import" in node.type:

        nodes.append(
            {
                "type":
                "import",

                "name":
                "import",

                "content":
                content[
                    node.start_byte:
                    node.end_byte
                ],
            }
        )

    for child in node.children:

        walk_tree(
            child,
            content,
            nodes,
        )


def parse_with_tree_sitter(
    content,
    ext,
):

    parser = get_parser(
        ext
    )

    if not parser:
        return []

    tree = parser.parse(
        bytes(
            content,
            "utf8",
        )
    )

    nodes = []

    walk_tree(
        tree.root_node,
        content,
        nodes,
    )

    return nodes