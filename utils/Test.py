from Dep2 import transaction_receipt , transaction_hash ,w3 , abi , address  , chain_id , transaction , nonce , private_key
import os 


import json , os 
from web3 import Web3



address = "0xa563Bb09b3505669DCd401Ad8DB700FD490aBc44"
contact_list = w3.eth.contract(address=transaction_receipt.contractAddress, abi=abi)

store_contact = contact_list.functions



def Add_User_Context(name,phone,ipfs,id):
    store_contact = contact_list.functions.create_User_Profile( Name , Phone , Ipfs , ID).build_transaction({"chainId": chain_id, "from": transaction_receipt.contractAddress, "gasPrice": w3.eth.gas_price, "nonce": nonce + 1})
    
    sign_store_contact = w3.eth.account.sign_transaction(store_contact, private_key=private_key )
    send_store_contact = w3.eth.send_raw_transaction(sign_store_contact.raw_transaction)
 
    contact_list.functions.print_Clientelle_Profiles().call()

    contact_list.functions.print

    print(address)


Name="Clyde Javis"
Phone= "0741371429" 
Ipfs = "#345JDK$334" 
ID =  "3245"
Add_User_Context(Name , Phone ,Ipfs , ID )