from etherscan.contracts import Contract
import json

contract_dir = "contracts"

# Returns path to file with saved source code and the sourcecode object
def get_contract_from_blockchain(address):
	key = get_api_key()
	api = Contract(address=address, api_key=key)
	sourcecode = api.get_sourcecode()

	assert len(sourcecode) == 1, f"no results found for {address}"
	assert len(sourcecode[0]['SourceCode']) > 0,  f"no sourcecode found for {address}"

	src_path = f"{contract_dir}/contract_{address}.sol"
	with open(src_path, "w") as c_file:
		c_file.write(sourcecode[0]['SourceCode'])

	return src_path, sourcecode[0]


def get_api_key():
	try:
		with open("api_key.secret", 'r') as kf:
			return kf.read()
	except Exception as e:
		raise Exception("ERROR: api_key.secret not found. Get a API key from https://etherscan.io/myapikey")