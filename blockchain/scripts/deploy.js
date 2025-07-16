const { ethers } = require("hardhat");

async function main() {
    console.log("Deploying DAO Multi-Agent Organization contracts...");

    // Get signers
    const [deployer, daoFounder] = await ethers.getSigners();
    console.log("Deploying with account:", deployer.address);
    console.log("DAO Founder:", daoFounder.address);

    // Deploy DAOToken
    const DAOToken = await ethers.getContractFactory("DAOToken");
    const daoToken = await DAOToken.deploy(
        "DAO Multi-Agent Token",
        "DMAT",
        ethers.utils.parseEther("1000000") // 1M tokens
    );
    await daoToken.deployed();
    console.log("DAOToken deployed to:", daoToken.address);

    // Deploy DAOCore
    const DAOCore = await ethers.getContractFactory("DAOCore");
    const daoCore = await DAOCore.deploy();
    await daoCore.deployed();
    console.log("DAOCore deployed to:", daoCore.address);

    // Deploy DAOGovernor
    const DAOGovernor = await ethers.getContractFactory("DAOGovernor");
    const daoGovernor = await DAOGovernor.deploy(daoToken.address);
    await daoGovernor.deployed();
    console.log("DAOGovernor deployed to:", daoGovernor.address);

    // Deploy other contracts
    const DAOTreasury = await ethers.getContractFactory("DAOTreasury");
    const daoTreasury = await DAOTreasury.deploy(daoCore.address, daoToken.address);
    await daoTreasury.deployed();
    console.log("DAOTreasury deployed to:", daoTreasury.address);

    const AgentRegistry = await ethers.getContractFactory("AgentRegistry");
    const agentRegistry = await AgentRegistry.deploy(daoCore.address);
    await agentRegistry.deployed();
    console.log("AgentRegistry deployed to:", agentRegistry.address);

    const MissionFactory = await ethers.getContractFactory("MissionFactory");
    const missionFactory = await MissionFactory.deploy(daoCore.address);
    await missionFactory.deployed();
    console.log("MissionFactory deployed to:", missionFactory.address);

    // Update DAOCore with contract addresses
    await daoCore.updateContract("DAOGovernor", daoGovernor.address);
    await daoCore.updateContract("DAOTreasury", daoTreasury.address);
    await daoCore.updateContract("AgentRegistry", agentRegistry.address);
    await daoCore.updateContract("MissionFactory", missionFactory.address);

    console.log("\nDeployment completed successfully!");
    
    // Save deployment info
    const deploymentInfo = {
        network: hre.network.name,
        deployer: deployer.address,
        contracts: {
            DAOToken: daoToken.address,
            DAOCore: daoCore.address,
            DAOGovernor: daoGovernor.address,
            DAOTreasury: daoTreasury.address,
            AgentRegistry: agentRegistry.address,
            MissionFactory: missionFactory.address
        }
    };

    console.log("\nDeployment Summary:");
    console.log(JSON.stringify(deploymentInfo, null, 2));
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });