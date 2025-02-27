// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.0;  

import "./Houseman.sol";  

contract Escrow is UserStorage {  
    enum EscrowStatus { Pending, Completed, Canceled }  

    struct EscrowTransaction {  
        uint256 id;  
        address buyer;  
        address seller;  
        uint256 amount;  
        EscrowStatus status;  
    }  

    mapping(uint256 => EscrowTransaction) public escrows;  
    uint256 public nextEscrowId;  

    event EscrowCreated(uint256 indexed id, address indexed buyer, address indexed seller, uint256 amount);  
    event EscrowCompleted(uint256 indexed id);  
    event EscrowCanceled(uint256 indexed id);  

    // Create a new escrow transaction  
    function createEscrow(uint256 sellerId) external payable {  
        require(msg.value > 0, "Must send some ether");  
        require(_userExists(sellerId), "Seller does not exist");  

        // Retrieve the seller's address based on the user ID  
        address sellerAddress = users[sellerId].exists ? address(this) : address(0);  
        require(sellerAddress != address(0), "Invalid seller address");  

        escrows[nextEscrowId] = EscrowTransaction(nextEscrowId, msg.sender, sellerAddress, msg.value, EscrowStatus.Pending);  
        
        emit EscrowCreated(nextEscrowId, msg.sender, sellerAddress, msg.value);  
        nextEscrowId++;  
    }  

    // Complete the escrow transaction  
    function completeEscrow(uint256 escrowId) external {  
        EscrowTransaction storage escrow = escrows[escrowId];  
        require(escrow.status == EscrowStatus.Pending, "Escrow not pending");  
        require(msg.sender == escrow.seller, "Only seller can complete the escrow");  

        // Transfer funds to the seller  
        payable(escrow.seller).transfer(escrow.amount);  
        escrow.status = EscrowStatus.Completed;  

        emit EscrowCompleted(escrowId);  
    }  

    // Cancel the escrow transaction  
    function cancelEscrow(uint256 escrowId) external {  
        EscrowTransaction storage escrow = escrows[escrowId];  
        require(escrow.status == EscrowStatus.Pending, "Escrow not pending");  
        require(msg.sender == escrow.buyer, "Only buyer can cancel the escrow");  

        // Refund the buyer  
        payable(escrow.buyer).transfer(escrow.amount);  
        escrow.status = EscrowStatus.Canceled;  

        emit EscrowCanceled(escrowId);  
    }  

    // Get escrow transaction details  
    function getEscrow(uint256 escrowId) external view returns (EscrowTransaction memory) {  
        return escrows[escrowId];  
    }  
}  