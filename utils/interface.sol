// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.0 ;
contract UserProfileManager {  
     address private ownerAccount ; 


    

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

     // Migration to an actual address 
    // Reveals Owner Address Logs
    event obtain_Owner_Address(address indexed oldOwner, address indexed newOwner);


    constructor(){
        ownerAccount = msg.sender; // 'msg.sender' is sender of current call, contract deployer for a constructor
        emit obtain_Owner_Address(address(0), ownerAccount);
    }


    // On-Sucess Create Event  - Called when data is successfully pushed to the struct - userProfile in array userListings
    // Where will account come from as its previously internally owned inside create_user_Profile , havent checked @ 16:23 21st>  #cheryll 
    event on_Create_Success(address indexed account  , string ipfsHash , string pid , string gender , string timestamp ); 


    // Function to push user profile data to our struct inside array
    // With an event that shows up on_sucess 
    // @20:35 / Tuesday - We had to remove the ISowner modifier to allow contract executions 
    //currently imolementing it raises a contractLogicError + Reverting  
    function create_User_Profile( string memory _ipfsHash  , string memory _pid , string memory _gender , string  memory _timestamp )public {
userListings.push(userProfile({ 
    ipfsHash:_ipfsHash,
    accountHolder : msg.sender , 
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


contract article_Dispensary {

struct Articles {
  uint256 articleID ;
  string articleName ;
  string author ;
  string publisher ; 
  string version ; 
  string genre  ;
  string serial ; 
  // add or  re-arrange more fields here  
}

}


contract Escrow {  
    address public buyer;  
    address public seller;  
    address public arbiter; // Fallback for disputes  
    uint256 public amount; // Total amount in escrow  
    uint256 public releaseTime; // Time limit for payment  
    bool public isComplete;  

    enum State { AWAITING_PAYMENT, FUNDED, COMPLETE, DISPUTED }  
    State public state;  

    event PaymentReceived(address payer, uint256 amount);  
    event PaymentReleased(address payee, uint256 amount);  
    event DisputeOpened(address disputer);  
    event DisputeResolved(address winner);  

    modifier onlyBuyer() {  
        require(msg.sender == buyer, "Only the buyer can call this function");  
        _;  
    }  

    modifier onlySeller() {  
        require(msg.sender == seller, "Only the seller can call this function");  
        _;  
    }  

    modifier onlyArbiter() {  
        require(msg.sender == arbiter, "Only the arbiter can call this function");  
        _;  
    }  

    modifier inState(State _state) {  
        require(state == _state, "Invalid contract state");  
        _;  
    }  

    constructor(address _seller, address _arbiter) {  
        buyer = msg.sender;  
        seller = _seller;  
        arbiter = _arbiter;  
        state = State.AWAITING_PAYMENT;  
        isComplete = false;  
    }  

    function fund() external payable onlyBuyer inState(State.AWAITING_PAYMENT) {  
        require(msg.value > 0, "Must send some ether");  
        amount += msg.value;  
        state = State.FUNDED;  

        emit PaymentReceived(msg.sender, msg.value);  
    }  

    function releasePayment() external onlyBuyer inState(State.FUNDED) {  
        require(!isComplete, "Payment already released.");  
        require(amount > 0, "No funds to release");  

        (bool success, ) = seller.call{value: amount}("");  
        require(success, "Failed to send Ether");  

        isComplete = true;  
        state = State.COMPLETE;  

        emit PaymentReleased(seller, amount);  
    }  

    function openDispute() external inState(State.FUNDED) {  
        require(msg.sender == buyer || msg.sender == seller, "Only buyer or seller can open a dispute");  
        state = State.DISPUTED;  

        emit DisputeOpened(msg.sender);  
    }  

    function resolveDispute(address winner) external onlyArbiter inState(State.DISPUTED) {  
        require(winner == buyer || winner == seller, "Winner must be buyer or seller");  

        uint256 finalAmount = amount;  
        amount = 0; // Avoid re-entrancy  

        (bool success, ) = winner.call{value: finalAmount}("");  
        require(success, "Failed to send Ether");  

        isComplete = true;  
        state = State.COMPLETE;  

        emit DisputeResolved(winner);  
    }  

    function getContractState() external view returns (State) {  
        return state;  
    }  

    receive() external payable {  
        fund();  
    }  
}  