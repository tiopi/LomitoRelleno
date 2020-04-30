from utils import get_contract_from_blockchain
from compiler import compile_into_ast
from analyze import analyze_ast
import argparse
import json


parser = argparse.ArgumentParser(description="Analyze Tacos")
parser.add_argument("--get-file", help="Use a local file path to analyze")
parser.add_argument("--get-from-hash", help="Use a contract from etherscan.io")

args = parser.parse_args()

if __name__ == "__main__":
    # src_path, _ = get_contract_from_blockchain("0x61935CbDd02287B511119DDb11Aeb42F1593b7EF")
    # src = get_contract_from_blockchain("0x5F098176B4f96207b3dc7b257175208112147243")
    if args.get_from_hash:
        print(args)
        src_path, _ = get_contract_from_blockchain(args.get_from_hash)
    else:
        src_path = args.get_file

    ast = compile_into_ast(src_path)

    print(analyze_ast(ast))
