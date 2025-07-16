// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "../interfaces/IDAO.sol";

contract ReputationSystem is AccessControl {
    bytes32 public constant EVALUATOR_ROLE = keccak256("EVALUATOR_ROLE");

    IDAO public daoCore;

    struct ReputationScore {
        uint256 totalScore;
        uint256 missionsCompleted;
        uint256 missionsSuccessful;
        uint256 lastUpdated;
    }

    mapping(address => ReputationScore) public reputations;
    mapping(address => mapping(string => uint256)) public skillRatings;

    event ReputationUpdated(address indexed agent, uint256 newScore);
    event SkillRated(address indexed agent, string skill, uint256 rating);

    constructor(address _daoCore) {
        daoCore = IDAO(_daoCore);
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(EVALUATOR_ROLE, msg.sender);
    }

    function updateReputation(
        address agent,
        bool missionSuccess,
        uint256 performanceScore
    ) external onlyRole(EVALUATOR_ROLE) {
        ReputationScore storage rep = reputations[agent];
        
        rep.missionsCompleted++;
        if (missionSuccess) {
            rep.missionsSuccessful++;
        }

        // Calculate new reputation score
        uint256 successRate = (rep.missionsSuccessful * 100) / rep.missionsCompleted;
        rep.totalScore = (successRate * performanceScore) / 100;
        rep.lastUpdated = block.timestamp;

        emit ReputationUpdated(agent, rep.totalScore);
    }

    function rateSkill(
        address agent,
        string memory skill,
        uint256 rating
    ) external onlyRole(EVALUATOR_ROLE) {
        require(rating <= 100, "Rating must be 0-100");
        skillRatings[agent][skill] = rating;
        emit SkillRated(agent, skill, rating);
    }

    function getReputation(address agent) external view returns (ReputationScore memory) {
        return reputations[agent];
    }

    function getSkillRating(address agent, string memory skill) external view returns (uint256) {
        return skillRatings[agent][skill];
    }
}