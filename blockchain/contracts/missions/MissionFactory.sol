// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "../interfaces/IMission.sol";
import "../interfaces/IDAO.sol";

contract MissionFactory is IMission, AccessControl {
    bytes32 public constant MISSION_CREATOR_ROLE = keccak256("MISSION_CREATOR_ROLE");

    IDAO public daoCore;
    
    uint256 private nextMissionId = 1;
    mapping(uint256 => Mission) public missions;
    mapping(address => uint256[]) public creatorMissions;

    event MissionCreated(uint256 indexed missionId, address indexed creator, uint256 budget);

    constructor(address _daoCore) {
        daoCore = IDAO(_daoCore);
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(MISSION_CREATOR_ROLE, msg.sender);
    }

    function createMission(
        string memory description,
        string[] memory requiredSkills,
        uint256 budget,
        uint256 deadline
    ) external override onlyRole(MISSION_CREATOR_ROLE) returns (uint256) {
        require(bytes(description).length > 0, "Description cannot be empty");
        require(requiredSkills.length > 0, "Must specify required skills");
        require(budget > 0, "Budget must be greater than 0");
        require(deadline > block.timestamp, "Deadline must be in the future");

        uint256 missionId = nextMissionId++;
        
        missions[missionId] = Mission({
            id: missionId,
            description: description,
            requiredSkills: requiredSkills,
            budget: budget,
            deadline: deadline,
            assignedAgents: new address[](0),
            status: MissionStatus.Created,
            creator: msg.sender
        });

        creatorMissions[msg.sender].push(missionId);

        emit MissionCreated(missionId, msg.sender, budget);
        return missionId;
    }

    function assignAgents(uint256 missionId, address[] memory agents) 
        external 
        override 
        onlyRole(MISSION_CREATOR_ROLE) 
    {
        require(missions[missionId].id != 0, "Mission does not exist");
        require(missions[missionId].status == MissionStatus.Created, "Mission already assigned");
        
        missions[missionId].assignedAgents = agents;
        missions[missionId].status = MissionStatus.Assigned;
    }

    function getMission(uint256 missionId) 
        external 
        view 
        override 
        returns (Mission memory) 
    {
        require(missions[missionId].id != 0, "Mission does not exist");
        return missions[missionId];
    }

    function updateMissionStatus(uint256 missionId, MissionStatus newStatus) 
        external 
        onlyRole(MISSION_CREATOR_ROLE) 
    {
        require(missions[missionId].id != 0, "Mission does not exist");
        missions[missionId].status = newStatus;
    }

    function getMissionsByCreator(address creator) external view returns (uint256[] memory) {
        return creatorMissions[creator];
    }
}