import codecs
import os, re
from fnmatch import fnmatch

from solcx import (
    compile_standard,
    get_solc_version_string,
    set_solc_version_pragma,
    get_solc_version,
    install_solc_pragma,
)


def compile_into_ast(src_path):
    # Convert to absolute path
    src_path = os.path.join(os.getcwd(), src_path)
    _, src_name = os.path.split(src_path)

    output_selection = {"*": {"": ["ast"]}}

    with open(src_path, "r") as f:
        src_data = f.read()
    version = re.findall(
        r"pragma solidity [^0-9]*([0-9]*\.[0-9]*\.[0-9]*).*;", src_data
    )[0]

    print(version)
    install_solc_pragma(version)
    set_solc_version_pragma(version)
    print(get_solc_version())

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
