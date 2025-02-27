// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.0;  

contract UserStorage {  
    struct User {  
        uint256 id;  
        string name;  
        string email;  
        bool exists;  
    }  

    mapping(uint256 => User) public users;  
    uint256 public nextUserId;  

    // Function to store user data  
    function _createUser(string memory name, string memory email) internal returns (uint256) {  
        users[nextUserId] = User(nextUserId, name, email, true);  
        return nextUserId++;  
    }  

    // Function to update user data  
    function _updateUser(uint256 id, string memory name, string memory email) internal {  
        User storage user = users[id];  
        user.name = name;  
        user.email = email;  
    }  

    // Function to get user details  
    function _getUser(uint256 id) internal view returns (User memory) {  
        return users[id];  
    }  

    // Function to check if user exists  
    function _userExists(uint256 id) internal view returns (bool) {  
        return users[id].exists;  
    }  
}  