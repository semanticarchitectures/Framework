// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

interface IMission {
    enum MissionStatus { Created, Assigned, InProgress, Completed, Failed }
    
    struct Mission {
        uint256 id;
        string description;
        string[] requiredSkills;
        uint256 budget;
        uint256 deadline;
        address[] assignedAgents;
        MissionStatus status;
        address creator;
    }
    
    function createMission(
        string memory description,
        string[] memory requiredSkills,
        uint256 budget,
        uint256 deadline
    ) external returns (uint256);
    
    function assignAgents(uint256 missionId, address[] memory agents) external;
    function getMission(uint256 missionId) external view returns (Mission memory);
}