const Web3 = require('web3');

const contractABI = [{'inputs': [], 'stateMutability': 'nonpayable', 'type': 'constructor'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'oldOwner', 'type': 'address'}, {'indexed': True, 'internalType': 'address', 'name': 'newOwner', 'type': 'address'}], 'name': 'obtain_Owner_Address', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'account', 'type': 'address'}, {'indexed': False, 'internalType': 'string', 'name': 'ipfsHash', 'type': 'string'}, {'indexed': False, 'internalType': 'string', 'name': 'pid', 'type': 'string'}, {'indexed': False, 'internalType': 'string', 'name': 'gender', 'type': 'string'}, {'indexed': False, 'internalType': 'string', 'name': 'timestamp', 'type': 'string'}], 'name': 'on_Create_Success', 'type': 'event'}, {'inputs': [{'internalType': 'string', 'name': '_ipfsHash', 'type': 'string'}, {'internalType': 'string', 'name': '_pid', 'type': 'string'}, {'internalType': 'string', 'name': '_gender', 'type': 'string'}, {'internalType': 'string', 'name': '_timestamp', 'type': 'string'}], 'name': 'create_User_Profile', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'print_Clientelle_Profiles', 'outputs': [{'components': [{'internalType': 'string', 'name': 'ipfsHash', 'type': 'string'}, {'internalType': 'address', 'name': 'accountHolder', 'type': 'address'}, {'internalType': 'string', 'name': 'personalID', 'type': 'string'}, {'internalType': 'string', 'name': 'personalGender', 'type': 'string'}, {'internalType': 'string', 'name': 'accountTimeline', 'type': 'string'}], 'internalType': 'struct UserProfileManager.userProfile[]', 'name': '', 'type': 'tuple[]'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'print_Clientelle_Quota', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'name': 'userListings', 'outputs': [{'internalType': 'string', 'name': 'ipfsHash', 'type': 'string'}, {'internalType': 'address', 'name': 'accountHolder', 'type': 'address'}, {'internalType': 'string', 'name': 'personalID', 'type': 'string'}, {'internalType': 'string', 'name': 'personalGender', 'type': 'string'}, {'internalType': 'string', 'name': 'accountTimeline', 'type': 'string'}], 'stateMutability': 'view', 'type': 'function'}]; 

const contractAddress = "0x59fc15e9d092e60D06952B7eC9e5EBbD1C2C4733"; // Your deployed contract address


const provider = new Web3.providers.HttpProvider('https://mainnet.infura.io/v3/2ce9cff1cb334d35a7d31c2020fee2a6'); 

const web3 = new Web3(provider);



const UserProfileManagement = new web3.eth.Contract(contractABI, contractAddress);



async function getContractValue() {

  const value = await UserProfileManagement.methods.printClientelleQuota$g().call();

  console.log('Contract value:', value);

}



getContractValue(); 
