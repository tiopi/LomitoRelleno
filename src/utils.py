from etherscan.contracts import Contract
import json
import os

contract_dir = "contracts"

# Returns path to file with saved source code and the sourcecode object
def get_contract_from_blockchain(address):
    key = get_api_key()
    api = Contract(address=address, api_key=key)
    sourcecode = api.get_sourcecode()

    assert len(sourcecode) == 1, f"no results found for {address}"
    assert len(sourcecode[0]["SourceCode"]) > 0, f"no sourcecode found for {address}"

    if sourcecode[0]["SourceCode"][0] == "{":
        # Multiple files
        file_mapping = {}
        src_path = f"{contract_dir}/contract_{address}/"
        if not os.path.exists(src_path):
            os.makedirs(src_path)
        src = sourcecode[0]["SourceCode"][1:-1]
        src = json.loads(src)
        for filepath, file in src["sources"].items():
            filename = os.path.basename(filepath)
            file_mapping[filepath] = filename
            with open(f"{src_path}{filename}", "w") as f:
                f.write(file["content"])
        # save the mappings
        with open(os.path.join(src_path, ".mapping"), "w+") as f:
            f.write(json.dumps(file_mapping))
    else:
        # Multiple files
        src_path = f"{contract_dir}/contract_{address}.sol"
        with open(src_path, "w") as c_file:
            c_file.write(sourcecode[0]["SourceCode"])

    return src_path, sourcecode[0]


def get_api_key():
    try:
        with open("api_key.secret", "r") as kf:
            return kf.read()
    except Exception as e:
        raise Exception(
            "ERROR: api_key.secret not found. Get a API key from https://etherscan.io/myapikey"
        )
