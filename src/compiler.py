import codecs
import os
from fnmatch import fnmatch

from solc import compile_standard, get_solc_version_string
from solc.main import strip_zeroes_from_month_and_day


def compile_into_ast(src_path):
    # Convert to absolute path
    src_path = os.path.join(os.getcwd(), src_path)
    _, src_name = os.path.split(src_path)

    output_selection = {"*": {"": ["ast"]}}

    compiler_input = {
        "language": "Solidity",
        "sources": {src_name: {"urls": [src_path]}},
        "settings": {"outputSelection": output_selection},
    }

    compile_output = compile_standard(compiler_input, allow_paths="/")
    ast = compile_output["sources"][os.path.basename(src_path)]["ast"]

    with open(src_path, "rb") as file:
        ast["source"] = codecs.utf_8_decode(file.read())[0]

    ast["_solc_version"] = get_solc_version_string()

    return ast
