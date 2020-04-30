import sys
from compile_ast import compile_ast
from pprint import pprint

TRUSTED = 3
SEMI_TRUSTED = 2
CONTROLLED_UNTRUSTED = 1 
UNTRUSTED = 0

integrity_levels = ["untrusted", "controlled_untrusted", "semi_trusted" "trusted"]

def analyze_json(contract_json_ast):
    integrity_level = 3
    for doc_node in contract_json_ast['nodes']:
        if "abstract" in doc_node:
            for node in doc_node['nodes']:
                integrity_level = min(analyze_node(node), integrity_level)
    
def analyze_node(node):
    if node['nodeType'] == "VariableDeclaration":
        if node['visibility'] == "public":
            return UNTRUSTED
        elif node['visibility'] == "private":
            return TRUSTED
        else:
            print("UNKNOWN GLOBAL DEF")
            return UNTRUSTED

    elif node['nodeType'] == "FunctionDefinition":
        if node['visibility'] == 'private' or node['stateMutability'] == 'pure' or node['stateMutability'] == "constant":
            return TRUSTED
        if node['visibility'] == 'internal':
            return SEMI_TRUSTED
        if node["visibility"] == "public" or node['visibility'] == 'external':
            check_body(node['body'])
            return UNTRUSTED
        return 0

def check_body(body):
    for statement in body['statements']:
        print("hello world")
        pprint(statement)

analyze_json(compile_ast(sys.argv[1]))
