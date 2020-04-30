import sys
from pprint import pprint

TRUSTED = 3
SEMI_TRUSTED = 2
CONTROLLED_UNTRUSTED = 1
UNTRUSTED = 0

integrity_levels = ["untrusted", "controlled_untrusted", "semi_trusted" "trusted"]


def analyze_ast(contract_json_ast):
    integrity_level = TRUSTED
    for doc_node in contract_json_ast["nodes"]:
        if "abstract" in doc_node:
            for node in doc_node["nodes"]:
                integrity_level = min(analyze_node(node), integrity_level)

    return integrity_levels[integrity_level]


def analyze_node(node):
    if node["nodeType"] == "VariableDeclaration":
        if node["visibility"] == "public":
            return UNTRUSTED
        elif node["visibility"] == "private":
            return TRUSTED
        else:
            print("UNKNOWN GLOBAL DEF")
            return UNTRUSTED

    elif node["nodeType"] == "FunctionDefinition":
        if (
            node["visibility"] == "private"
            or node["stateMutability"] == "pure"
            or node["stateMutability"] == "constant"
        ):
            return TRUSTED
        if node["visibility"] == "internal":
            return SEMI_TRUSTED
        if node["visibility"] == "public" or node["visibility"] == "external":
            check_body(node["body"])
            return UNTRUSTED
    elif node["nodeType"] == "EventDefinition":
        return TRUSTED
    else:
        print(node["nodeType"])
    return UNTRUSTED


def check_body(body):
    for statement in body['statements']:
        print("hello world")
        pprint(statement)
