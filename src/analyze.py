import sys
from pprint import pprint

TRUSTED = 3
SEMI_TRUSTED = 2
CONTROLLED_UNTRUSTED = 1
UNTRUSTED = 0

integrity_levels = ["untrusted", "controlled_untrusted", "semi_trusted", "trusted"]
controlled_modifiers = set()

def analyze_ast(contract_json_ast):
    integrity_level = TRUSTED
    for doc_node in contract_json_ast["nodes"]:
        if "nodes" in doc_node:
            for node in doc_node["nodes"]:
                #print(analyze_node(node), integrity_level)
                integrity_level = min(analyze_node(node), integrity_level)

    return integrity_levels[integrity_level]


def analyze_node(node):
    if node["nodeType"] == "VariableDeclaration" or node['nodeType'] == 'StructDefinition':
        '''
        if node["visibility"] == "public":
            return UNTRUSTED
        elif node["visibility"] == "private":
            return TRUSTED
        elif node['visibility'] == 'internal':
            return SEMI_TRUSTED
        else:
            print("UNKNOWN GLOBAL DEF")
            print(node['visibility'])
            return UNTRUSTED
        '''
        return TRUSTED

    elif node["nodeType"] == "FunctionDefinition":
        if ('isConstructor' in node and node['isConstructor']) or ('kind' in node and node['kind'] == 'constructor') :
            return TRUSTED
        if (
            node["visibility"] == "private"
            or node["stateMutability"] == "pure"
            or node["stateMutability"] == "constant"
            or node["stateMutability"] == "view"
        ):
            return TRUSTED
        if node["visibility"] == "internal":
            return max(check_body(node["body"]), SEMI_TRUSTED)

        if node["visibility"] == "public" or node["visibility"] == "external":
            for modifier in node['modifiers']:
                if modifier['modifierName']['name'] in controlled_modifiers:
                    return CONTROLLED_UNTRUSTED
            return max(check_body(node["body"]), UNTRUSTED)

    elif node["nodeType"] == "EventDefinition":
        return TRUSTED
    elif node['nodeType'] == 'ModifierDefinition':
        if check_body(node['body']) == CONTROLLED_UNTRUSTED:
            controlled_modifiers.add(node['name'])
        return TRUSTED
    else:
        print(node["nodeType"])
    return TRUSTED


def check_body(body):
    # Function does not do anything
    if body is None or len(body["statements"]) == 0:
        return TRUSTED

    final_value = UNTRUSTED
    for statement in body["statements"]:
        if 'expression' in statement:
            final_value = max(check_expression(statement['expression']), final_value)

    return final_value       

def check_expression(expression):

    if expression['nodeType'] == 'MemberAccess':
        if expression['memberName'] == 'sender' and expression['expression']['name'] == 'msg':
            return CONTROLLED_UNTRUSTED

    # Assuming all non-pure/non-constant/non-view functions modify state.
    if expression['nodeType'] == 'FunctionCall' or expression['nodeType'] == 'MemberAccess':
        return check_expression(expression['expression'])
    if expression['nodeType'] == 'Identifier':

        # Assume Require secures contract
        if expression['name'] == 'require':
            return CONTROLLED_UNTRUSTED

    return UNTRUSTED
