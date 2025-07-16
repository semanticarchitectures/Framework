// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "../interfaces/IDAO.sol";

contract DAOCore is IDAO, AccessControl, Pausable {
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant GOVERNOR_ROLE = keccak256("GOVERNOR_ROLE");

    mapping(string => address) public contracts;
    mapping(address => bool) public authorizedContracts;
    mapping(string => uint256) public systemParameters;

    event ContractUpdated(string indexed name, address indexed newAddress);
    event SystemParameterChanged(string indexed parameter, uint256 newValue);
    event ContractAuthorized(address indexed contractAddr, bool authorized);

    constructor() {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(ADMIN_ROLE, msg.sender);
        
        // Initialize default parameters
        systemParameters["minimumStake"] = 1000 * 10**18; // 1000 tokens
        systemParameters["votingPeriod"] = 7 days;
        systemParameters["executionDelay"] = 2 days;
    }

    function isAuthorizedContract(address contractAddr) external view override returns (bool) {
        return authorizedContracts[contractAddr];
    }

    function getContract(string memory name) external view override returns (address) {
        return contracts[name];
    }

    function updateContract(string memory name, address newAddress) 
        external 
        override 
        onlyRole(ADMIN_ROLE) 
    {
        contracts[name] = newAddress;
        authorizedContracts[newAddress] = true;
        emit ContractUpdated(name, newAddress);
    }

    function getSystemParameter(string memory parameter) 
        external 
        view 
        override 
        returns (uint256) 
    {
        return systemParameters[parameter];
    }

    function setSystemParameter(string memory parameter, uint256 value) 
        external 
        onlyRole(ADMIN_ROLE) 
    {
        systemParameters[parameter] = value;
        emit SystemParameterChanged(parameter, value);
    }

    function pause() external onlyRole(ADMIN_ROLE) {
        _pause();
    }

    function unpause() external onlyRole(ADMIN_ROLE) {
        _unpause();
    }
}