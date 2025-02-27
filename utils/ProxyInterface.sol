// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.0;  

contract UserProxy {  
    address public implementation;  

    constructor(address _implementation) {  
        implementation = _implementation;  
    }  

    // Fallback function to delegate calls to the implementation contract  
    fallback() external {  
        address impl = implementation;  
        require(impl != address(0), "Implementation contract not set");  
        assembly {  
            // Forward the call to the implementation contract  
            calldatacopy(0, 0, calldatasize())  
            let result := delegatecall(gas(), impl, 0, calldatasize(), 0, 0)  
            returndatacopy(0, 0, returndatasize())  
            switch result  
                case 0 { revert(0, returndatasize()) }  
                default { return(0, returndatasize()) }  
        }  
    }  

    // Function to upgrade the implementation contract  
    function upgradeImplementation(address newImplementation) external {  
        // Typically, you'd want to have access control here  
        implementation = newImplementation;  
    }  
}  