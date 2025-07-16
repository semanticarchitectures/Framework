module.exports = async ({ getNamedAccounts, deployments }) => {
    const { deploy } = deployments;
    const { deployer } = await getNamedAccounts();

    console.log("Deploying core contracts...");

    // Deploy DAOToken
    const daoToken = await deploy("DAOToken", {
        from: deployer,
        args: [
            "DAO Multi-Agent Token",
            "DMAT",
            ethers.utils.parseEther("1000000")
        ],
        log: true,
    });

    // Deploy DAOCore
    const daoCore = await deploy("DAOCore", {
        from: deployer,
        args: [],
        log: true,
    });

    console.log("Core contracts deployed successfully");
};

module.exports.tags = ["core"];