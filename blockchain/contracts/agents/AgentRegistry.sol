// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "../interfaces/IAgent.sol";
import "../interfaces/IDAO.sol";

contract AgentRegistry is IAgent, AccessControl {
    bytes32 public constant REGISTRY_ADMIN_ROLE = keccak256("REGISTRY_ADMIN_ROLE");

    IDAO public daoCore;
    
    mapping(address => AgentInfo) public agents;
    mapping(address => bool) public isRegistered;
    address[] public agentList;

    event AgentRegistered(address indexed agent, string[] capabilities);
    event AgentDeactivated(address indexed agent);
    event AgentReactivated(address indexed agent);

    constructor(address _daoCore) {
        daoCore = IDAO(_daoCore);
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(REGISTRY_ADMIN_ROLE, msg.sender);
    }

    function registerAgent(string[] memory capabilities, uint256 stakeAmount) 
        external 
        override 
    {
        require(!isRegistered[msg.sender], "Agent already registered");
        require(capabilities.length > 0, "Must have at least one capability");

        agents[msg.sender] = AgentInfo({
            agentAddress: msg.sender,
            capabilities: capabilities,
            reputation: 50, // Starting reputation
            stakedAmount: stakeAmount,
            isActive: true
        });

        isRegistered[msg.sender] = true;
        agentList.push(msg.sender);

        emit AgentRegistered(msg.sender, capabilities);
    }

    function getAgentInfo(address agent) 
        external 
        view 
        override 
        returns (AgentInfo memory) 
    {
        require(isRegistered[agent], "Agent not registered");
        return agents[agent];
    }

    function updateReputation(address agent, int256 change) 
        external 
        override 
        onlyRole(REGISTRY_ADMIN_ROLE) 
    {
        require(isRegistered[agent], "Agent not registered");
        
        if (change > 0) {
            agents[agent].reputation += uint256(change);
        } else {
            uint256 decrease = uint256(-change);
            if (decrease >= agents[agent].reputation) {
                agents[agent].reputation = 0;
            } else {
                agents[agent].reputation -= decrease;
            }
        }
    }

    function deactivateAgent(address agent) external onlyRole(REGISTRY_ADMIN_ROLE) {
        require(isRegistered[agent], "Agent not registered");
        agents[agent].isActive = false;
        emit AgentDeactivated(agent);
    }

    function getActiveAgents() external view returns (address[] memory) {
        uint256 activeCount = 0;
        for (uint256 i = 0; i < agentList.length; i++) {
            if (agents[agentList[i]].isActive) {
                activeCount++;
            }
        }

        address[] memory activeAgents = new address[](activeCount);
        uint256 index = 0;
        for (uint256 i = 0; i < agentList.length; i++) {
            if (agents[agentList[i]].isActive) {
                activeAgents[index] = agentList[i];
                index++;
            }
        }

        return activeAgents;
    }
}