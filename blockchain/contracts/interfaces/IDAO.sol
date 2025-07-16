// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

interface IDAO {
    function isAuthorizedContract(address contractAddr) external view returns (bool);
    function getContract(string memory name) external view returns (address);
    function updateContract(string memory name, address newAddress) external;
    function getSystemParameter(string memory parameter) external view returns (uint256);
}