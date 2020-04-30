from utils import get_contract_from_blockchain
from compiler import compile_into_ast
from analyze import analyze_ast
import json

if __name__ == "__main__":
    # src_path, _ = get_contract_from_blockchain("0x61935CbDd02287B511119DDb11Aeb42F1593b7EF")
    # src_path, _ = get_contract_from_blockchain("0x5F098176B4f96207b3dc7b257175208112147243")
    # src_path, _ = get_contract_from_blockchain("0xC39D185eE1256E10D5010722D359ec87301eb647")
    src_path = "contracts/contract_0x61935CbDd02287B511119DDb11Aeb42F1593b7EF"
    ast = compile_into_ast(src_path)
    # analyze_ast(ast)
