from utils import get_contract_from_blockchain

if __name__ == "__main__":
	src = get_contract_from_blockchain("0x61935CbDd02287B511119DDb11Aeb42F1593b7Ef")
	print(len(src))
	print(src[0].keys())