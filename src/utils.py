from etherscan.contracts import Contract

def get_contract_from_blockchain(address):
	key = get_api_key()
	api = Contract(address=address, api_key=key)
	sourcecode = api.get_sourcecode()
	return sourcecode


def get_api_key():
	try:
		with open("api_key.secret", 'r') as kf:
			return kf.read()
	except Exception as e:
		raise Exception("ERROR: api_key.secret not found. Get a API key from https://etherscan.io/myapikey")