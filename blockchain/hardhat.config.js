require("@nomicfoundation/hardhat-toolbox");
require("hardhat-deploy");
require("@nomiclabs/hardhat-ethers");

module.exports = {
  solidity: {
    version: "0.8.19",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200
      }
    }
  },
  networks: {
    hardhat: {
      chainId: 1337
    },
    hedera_testnet: {
      url: "https://testnet.hashio.io/api",
      chainId: 296
    }
  },
  namedAccounts: {
    deployer: 0,
    daoFounder: 1
  }
};