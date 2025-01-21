// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;
contract interface {
  
// Our Default initilization constructor 
// For values that are critical at start time  // on_page_ready => js 
  constructor() public {
  }

  uint public videoCount = 0;
  string public name = "DVideo";
  mapping(uint => Video) public videos;



}


