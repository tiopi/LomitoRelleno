import codecs
import os, re
from fnmatch import fnmatch
import json

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

    output_selection = {"*": {"": ["ast"]}}

    if os.path.isdir(src_path):
        # Multiple file contract
        src_data = {}
        first = True
        for filename in os.listdir(src_path):
            print(filename)
            src_data[filename] = {"urls": [os.path.join(src_path, filename)]}
            if first:
                with open(os.path.join(src_path, filename), "r") as f:
                    file_data = f.read()
                    version = re.findall(
                        r"pragma solidity [^0-9]*([0-9]*\.[0-9]*\.[0-9]*).*;", file_data
                    )[0]
                first = False
    else:
        # Single file
        with open(src_path, "r") as f:
            src_data = f.read()
        _, src_name = os.path.split(src_path)
        src_files = {src_name: {"urls": [src_path]}}
        version = re.findall(
            r"pragma solidity [^0-9]*([0-9]*\.[0-9]*\.[0-9]*).*;", src_data
        )[0]

    install_solc_pragma(version)
    set_solc_version_pragma(version)

    compiler_input = {
        "language": "Solidity",
        "sources": src_data,
        "settings": {"outputSelection": output_selection},
    }

    compile_output = compile_standard(compiler_input, allow_paths="/")
    ast = compile_output["sources"][os.path.basename(src_path)]["ast"]

    with open(src_path, "rb") as file:
        ast["source"] = codecs.utf_8_decode(file.read())[0]

    ast["_solc_version"] = get_solc_version_string()

    return ast
