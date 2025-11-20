const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("CitiTrackReport", function () {
  let CitiTrackReport;
  let citiTrack;
  let owner;
  let addr1;

  beforeEach(async function () {
    CitiTrackReport = await ethers.getContractFactory("CitiTrackReport");
    [owner, addr1] = await ethers.getSigners();
    citiTrack = await CitiTrackReport.deploy();
    await citiTrack.deployed();
  });

  describe("Deployment", function () {
    it("Should deploy successfully", async function () {
      expect(citiTrack.address).to.not.be.undefined;
    });
  });

  describe("Anchoring Reports", function () {
    it("Should anchor a report", async function () {
      const reportId = "RPT-2024-001";
      const eventType = "created";
      const dataHash = "0x1234567890abcdef";

      await citiTrack.anchorReport(reportId, eventType, dataHash);

      const trail = await citiTrack.getReportTrail(reportId);
      expect(trail.length).to.equal(1);
      expect(trail[0].reportId).to.equal(reportId);
      expect(trail[0].eventType).to.equal(eventType);
      expect(trail[0].dataHash).to.equal(dataHash);
    });

    it("Should emit ReportAnchored event", async function () {
      const reportId = "RPT-2024-002";
      const eventType = "created";
      const dataHash = "0xabcdef1234567890";

      await expect(citiTrack.anchorReport(reportId, eventType, dataHash))
        .to.emit(citiTrack, "ReportAnchored")
        .withArgs(reportId, eventType, (await ethers.provider.getBlock()).timestamp + 1, dataHash);
    });

    it("Should support multiple events for same report", async function () {
      const reportId = "RPT-2024-003";

      await citiTrack.anchorReport(reportId, "created", "0x111");
      await citiTrack.anchorReport(reportId, "verified", "0x222");
      await citiTrack.anchorReport(reportId, "resolved", "0x333");

      const trail = await citiTrack.getReportTrail(reportId);
      expect(trail.length).to.equal(3);
    });
  });

  describe("Querying Reports", function () {
    it("Should return correct event count", async function () {
      const reportId = "RPT-2024-004";

      await citiTrack.anchorReport(reportId, "created", "0x111");
      await citiTrack.anchorReport(reportId, "verified", "0x222");

      const count = await citiTrack.getEventCount(reportId);
      expect(count).to.equal(2);
    });

    it("Should verify if report is anchored", async function () {
      const reportId = "RPT-2024-005";

      expect(await citiTrack.isReportAnchored(reportId)).to.be.false;

      await citiTrack.anchorReport(reportId, "created", "0x111");

      expect(await citiTrack.isReportAnchored(reportId)).to.be.true;
    });

    it("Should return empty array for non-existent report", async function () {
      const trail = await citiTrack.getReportTrail("NON-EXISTENT");
      expect(trail.length).to.equal(0);
    });
  });

  describe("Timestamp Verification", function () {
    it("Should record correct timestamp", async function () {
      const reportId = "RPT-2024-006";
      
      const tx = await citiTrack.anchorReport(reportId, "created", "0x111");
      const receipt = await tx.wait();
      const block = await ethers.provider.getBlock(receipt.blockNumber);

      const trail = await citiTrack.getReportTrail(reportId);
      expect(trail[0].timestamp).to.equal(block.timestamp);
    });
  });
});