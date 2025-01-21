// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.0;  

contract UserProfileManager {  

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


    // Function to create a user profile page 
    // With an event that shows up on_sucess 
    function create_User_Profile( string memory _ipfsHash  , string memory _pid , string memory _gender , string  memory _timestamp )public{
userListings.push(userProfile({ 
    ipfsHash:_ipfsHash,
    accountHolder : address(0) , 
    personalID:_pid ,
    personalGender : _gender ,
    accountTimeline : _timestamp 
}));
    }

    // Function To Print All User Profiles 
    // Returning this list should come from ipfs  in the future 

   
   function print_Clientelle_Profiles() public view returns (userProfile[] memory ){ 
   userProfile[] memory userArray = new userProfile[](userListings.length);

  for (uint i = 0; i < userListings.length; i++) {
    userArray[i] = userListings[i];
  }

  return userArray;
}


    // Get the total number of entries / clients in the UserListings storage 
    // Retrives the index of elements present in the array 
    function print_Clientelle_Quota() public view returns(uint256) { 
        return userListings.length ;
    }







// End of contract

}

