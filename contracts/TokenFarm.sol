// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

//stakeTokens
//unstakeTokens
//IssueTokens
//addAllowedTokens
//getEthValue

import  "@openzeppelin/contracts/access/Ownable.sol";

contract TokenFarm is Ownable {

    address[] public allowedTokens;

    function stakeTokens(uint256 _amount, address _token) public {
        //what tokens can they stake?
        //how much can they stake? 
        require(_amount > 0, "Amount must be more than 0");

    }

    function addAllowedTokens(address _token) public onlyOwner {
        allowedTokens.push(_token);
    }

    function tokenIsAllowed(address _token) public view returns (bool){
        for(uint256 tokenIndex=0; tokenIndex < allowedTokens.length; tokenIndex++) {
            if (_token == allowedTokens[tokenIndex]) {
                return true;
            }
        }
        return false;
    }

}