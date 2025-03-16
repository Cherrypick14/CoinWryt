from web3 import Web3  

# Connect to an Ethereum node  
infura_url = 'https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'  
web3 = Web3(Web3.HTTPProvider(infura_url))  

# Check if connected  
if not web3.isConnected():  
    print("Failed to connect to Ethereum network")  
    exit()  

# Set up wallet addresses and private key  
sender_address = '0xYourSenderAddress'  
receiver_address = '0xReceiverAddress'  
private_key = 'YourPrivateKey'  # Keep this safe  

# Define transaction parameters  
nonce = web3.eth.getTransactionCount(sender_address)  
value = web3.toWei(0.01, 'ether')  # Amount to send in Wei  
transaction = {  
    'to': receiver_address,  
    'value': value,  
    'gas': 2000000,  # Estimate gas limit  
    'gasPrice': web3.toWei('50', 'gwei'),  # Gas price in Gwei  
    'nonce': nonce,  
    'chainId': 1  # Mainnet ID  
}  

# Sign the transaction  
signed_txn = web3.eth.account.signTransaction(transaction, private_key)  

# Send the transaction  
txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)  

print(f"Transaction sent! Hash: {web3.toHex(txn_hash)}")  