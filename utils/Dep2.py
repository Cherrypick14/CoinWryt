from solcx import compile_standard, install_solc
import json , os 
from web3 import Web3


with open("interface.sol", "r") as file:
    contact_list_file = file.read()

install_solc("0.8.0")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"interface.sol": {"content": contact_list_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": [
                        "abi",
                        "metadata",
                        "evm.bytecode",
                        "evm.bytecode.sourceMap",
                    ]  # output needed to interact with and deploy contract
                }
            }
        },
    },
    solc_version="0.8.0",
)

with open("compiler_output.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["interface.sol"]["UserProfileManager"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = json.loads(
    compiled_sol["contracts"]["interface.sol"]["UserProfileManager"]["metadata"]
)["output"]["abi"]

# For connecting to ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chain_id = 1337
address = "0xa563Bb09b3505669DCd401Ad8DB700FD490aBc44"
private_key = (
    "0x44094d201fdbc7e463433797ba302eb6a8b33493ba3f4bd1d05b0f407031fcb5"
)  # leaving the private key like this is very insecure if you are working on real world project

# Create the contract in Python
UserProfileManager = w3.eth.contract(abi=abi, bytecode=bytecode)
print(abi)
# Get the latest transaction
nonce = w3.eth.get_transaction_count(address)
# build transaction
transaction = UserProfileManager.constructor().build_transaction(
    {"chainId": chain_id, "gasPrice": w3.eth.gas_price, "from": address, "nonce": nonce}
)
# Sign the transaction
sign_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract!")
# Send the transaction
transaction_hash = w3.eth.send_raw_transaction(sign_transaction.raw_transaction)
# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
print(f"Done! Contract deployed to {transaction_receipt.contractAddress}")

contact_list = w3.eth.contract(address=transaction_receipt.contractAddress, abi=abi)


store_contact = contact_list.functions
