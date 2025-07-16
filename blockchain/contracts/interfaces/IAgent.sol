// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

interface IAgent {
    struct AgentInfo {
        address agentAddress;
        string[] capabilities;
        uint256 reputation;
        uint256 stakedAmount;
        bool isActive;
    }
    
    function registerAgent(string[] memory capabilities, uint256 stakeAmount) external;
    function getAgentInfo(address agent) external view returns (AgentInfo memory);
    function updateReputation(address agent, int256 change) external;
}