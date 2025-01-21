// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.0;  
import "hardhat/console.sol";

contract UserProfileManager {  
     address private ownerAccount ; 

     receive() external payable {}

    

    // A struct which will hold our user's information 
    struct userProfile {  
        // IPFS hash for :this: user profile 
        // This ID will be used to track the data in this structure once stored on IPFS 
        // Loosing this hash == loosing user data  
        // Consider Apdating this hash on data modification "future" 
        string ipfsHash;
        // Account Owner Address 
        address accountHolder ;    
        //A uniquely generated set of numbers for tracking articles belonging to a particular user
        // Can also be used for tracking transaction data on ipfs once this user is paid by our system
        string personalID ; //  Avoided ref articles with :owner: to protect wallet id . 
        // User Gender Specific Details 
        string personalGender ;
        // Account Creation Timestamp
        string accountTimeline ; 
    }  

    // Since Will Have More Than One User  We need to have an array of structs 
    userProfile[] public userListings ;
    // Mapping for Address to UserProfile 
    mapping(address => userProfile) private userProfiles;  

    // modifier to check if caller is owner
    modifier isOwner() {
        // If the first argument of 'require' evaluates to 'false', execution terminates and all
        // changes to the state and to Ether balances are reverted.
        // This used to consume all gas in old EVM versions, but not anymore.
        // It is often a good idea to use 'require' to check if functions are called correctly.
        // As a second argument, you can also provide an explanation about what went wrong.
        require(msg.sender == ownerAccount , "Caller is not owner");
        _;
    }

    event obtain_Owner_Address(address indexed oldOwner, address indexed newOwner);


    constructor(){
        console.log("Owner contract deployed by:", msg.sender);
        ownerAccount = msg.sender; // 'msg.sender' is sender of current call, contract deployer for a constructor
        emit obtain_Owner_Address(address(0), ownerAccount);
    }


    // On-Sucess Create Event  - Called when data is successfully pushed to the struct - userProfile in array userListings
    // Where will account come from as its previously internally owned inside create_user_Profile , havent checked @ 16:23 21st>  #cheryll 
    event on_Create_Success(address indexed account  , string ipfsHash , string pid , string gender , string timestamp ); 


    // Function to push user profile data to our struct inside array
    // With an event that shows up on_sucess 
    function create_User_Profile( string memory _ipfsHash  , string memory _pid , string memory _gender , string  memory _timestamp )public isOwner{
userListings.push(userProfile({ 
    ipfsHash:_ipfsHash,
    accountHolder : address(0) , 
    personalID:_pid ,
    personalGender : _gender ,
    accountTimeline : _timestamp 
}));
 // Notifies On-Successfull Profile Creation 
    // Msg.sender carries the id of the person in question 
    emit on_Create_Success(msg.sender , _ipfsHash , _pid , _gender , _timestamp);
    // End of Function create_User_Profile 
    }

  

    // Function To Print All User Profiles 
    // Returning this list should come from ipfs  in the future 
   function print_Clientelle_Profiles() public view returns (userProfile[] memory ){ 
   userProfile[] memory userArray = new userProfile[](userListings.length);
   for (uint i = 0; i < userListings.length; i++) {
        userArray[i] = userListings[i];
    }
  // Lets return a struct at each iteration 
    return userArray;
    }


    // Get the total number of entries / clients in the UserListings storage 
    // Retrives the index of elements present in the array 
    function print_Clientelle_Quota() public view returns(uint256) { 
    // Returns the Length() of userListings array which hold UserProfiles 
        return userListings.length ;
    }


// End of contract

}

