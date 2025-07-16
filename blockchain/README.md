# Blockchain Infrastructure

This directory contains all blockchain-related code for the DAO Multi-Agent Organization, including smart contracts, deployment scripts, and testing infrastructure.

## Structure

- `contracts/` - Solidity smart contracts
- `scripts/` - Deployment and utility scripts
- `test/` - Contract tests
- `tasks/` - Custom Hardhat tasks
- `deploy/` - Deployment configurations
- `typechain-types/` - Generated TypeScript types

# This creates a complete blockchain infrastructure with:

- Smart Contracts: Core DAO functionality, governance, agent management, and mission system
- Interfaces: Clean contract interfaces for modularity
- Deployment Scripts: Automated deployment with proper configuration
- Testing: Unit tests for core functionality
- Hardhat Configuration: Ready for Hedera testnet deployment

The structure follows your architecture docs and integrates with your existing simulation code. You can now run:

- npm install to install dependencies
- npx hardhat compile to compile contracts
- npx hardhat test to run tests
- npx hardhat deploy --network hedera_testnet to deploy