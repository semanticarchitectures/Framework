const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("DAOCore", function () {
    let daoCore;
    let owner, addr1, addr2;

    beforeEach(async function () {
        [owner, addr1, addr2] = await ethers.getSigners();
        
        const DAOCore = await ethers.getContractFactory("DAOCore");
        daoCore = await DAOCore.deploy();
        await daoCore.deployed();
    });

    describe("Deployment", function () {
        it("Should set the right owner", async function () {
            expect(await daoCore.hasRole(await daoCore.DEFAULT_ADMIN_ROLE(), owner.address)).to.be.true;
        });

        it("Should initialize default parameters", async function () {
            expect(await daoCore.getSystemParameter("minimumStake")).to.equal(ethers.utils.parseEther("1000"));
            expect(await daoCore.getSystemParameter("votingPeriod")).to.equal(7 * 24 * 60 * 60); // 7 days
        });
    });

    describe("Contract Management", function () {
        it("Should allow admin to update contracts", async function () {
            await daoCore.updateContract("TestContract", addr1.address);
            expect(await daoCore.getContract("TestContract")).to.equal(addr1.address);
            expect(await daoCore.isAuthorizedContract(addr1.address)).to.be.true;
        });

        it("Should emit ContractUpdated event", async function () {
            await expect(daoCore.updateContract("TestContract", addr1.address))
                .to.emit(daoCore, "ContractUpdated")
                .withArgs("TestContract", addr1.address);
        });
    });

    describe("System Parameters", function () {
        it("Should allow admin to set system parameters", async function () {
            await daoCore.setSystemParameter("testParam", 12345);
            expect(await daoCore.getSystemParameter("testParam")).to.equal(12345);
        });

        it("Should emit SystemParameterChanged event", async function () {
            await expect(daoCore.setSystemParameter("testParam", 12345))
                .to.emit(daoCore, "SystemParameterChanged")
                .withArgs("testParam", 12345);
        });
    });
});