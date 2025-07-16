// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "../interfaces/IDAO.sol";

contract DAOTreasury is AccessControl {
    bytes32 public constant TREASURER_ROLE = keccak256("TREASURER_ROLE");
    bytes32 public constant MISSION_ROLE = keccak256("MISSION_ROLE");

    IDAO public daoCore;
    IERC20 public daoToken;

    mapping(uint256 => uint256) public missionBudgets;
    mapping(address => uint256) public agentRewards;

    event FundsAllocated(uint256 indexed missionId, uint256 amount);
    event RewardDistributed(address indexed agent, uint256 amount);
    event TreasuryDeposit(address indexed from, uint256 amount);

    constructor(address _daoCore, address _daoToken) {
        daoCore = IDAO(_daoCore);
        daoToken = IERC20(_daoToken);
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(TREASURER_ROLE, msg.sender);
    }

    function allocateMissionBudget(uint256 missionId, uint256 amount) 
        external 
        onlyRole(MISSION_ROLE) 
    {
        require(daoToken.balanceOf(address(this)) >= amount, "Insufficient treasury funds");
        missionBudgets[missionId] = amount;
        emit FundsAllocated(missionId, amount);
    }

    function distributeReward(address agent, uint256 amount) 
        external 
        onlyRole(MISSION_ROLE) 
    {
        require(daoToken.transfer(agent, amount), "Transfer failed");
        agentRewards[agent] += amount;
        emit RewardDistributed(agent, amount);
    }

    function deposit(uint256 amount) external {
        require(daoToken.transferFrom(msg.sender, address(this), amount), "Transfer failed");
        emit TreasuryDeposit(msg.sender, amount);
    }

    function getBalance() external view returns (uint256) {
        return daoToken.balanceOf(address(this));
    }
}