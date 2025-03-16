from flask import Flask, jsonify, request  
from web3 import Web3  

app = Flask(__name__)  

# Connect to Ethereum node (replace with your node's URL)  
infura_url = 'https://sepolia.infura.io/v3/2ce9cff1cb334d35a7d31c2020fee2a6'  
web3 = Web3(Web3.HTTPProvider(infura_url))  

# Ensure we are connected to the Ethereum network  
if not web3.is_connected():  
    print("Failed to connect to Ethereum network")  
    exit()  

# Private key and wallet address setup  
sender_address = '0xd48e84bDA5351D516b9cd9361FEA27b086A93188'  # Replace this with your sender address  
private_key = 'd60797b8b67ebbf7826047bf5f38b70999bd32e1296c837fb4b78c773a71fae4'           # Never expose this in production  
receiver_address = ''    # Replace with actual receiver address  

@app.route('/send_ether', methods=['POST'])  
def send_ether():  
    try:  
        # Get the next nonce  
        nonce = web3.eth.get_transaction_count(sender_address)  

        # Define transaction parameters  
        transaction = {  
            'to': receiver_address,  
            'value': web3.to_wei(0.001, 'ether'),  # Amount to send in Wei  
            'gas': 2000000,  # Estimate gas limit  
            'gasPrice': web3.to_wei('50', 'gwei'),  # Adjust as needed  
            'nonce': nonce,  
            'chainId': 1  # Mainnet ID  
        }  

        # Sign the transaction  
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)  

        # Send the transaction  
        txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)  

        # Return transaction hash  
        return jsonify({'status': 'success', 'transaction_hash': web3.toHex(txn_hash)})  
    
    except Exception as e:  
        return jsonify({'status': 'error', 'message': str(e)})  

if __name__ == '__main__':  
    app.run(debug=True)  