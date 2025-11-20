/**
 * Deployment script for CitiTrackReport contract
 */
const hre = require("hardhat");

async function main() {
  console.log("🚀 Deploying CitiTrackReport contract...");

  // Get the contract factory
  const CitiTrackReport = await hre.ethers.getContractFactory("CitiTrackReport");
  
  // Deploy the contract
  const citiTrackReport = await CitiTrackReport.deploy();
  
  await citiTrackReport.deployed();

  console.log("✅ CitiTrackReport deployed to:", citiTrackReport.address);
  console.log("📝 Save this address to your .env file as CONTRACT_ADDRESS");
  
  // Wait for a few block confirmations
  console.log("⏳ Waiting for block confirmations...");
  await citiTrackReport.deployTransaction.wait(5);
  
  console.log("✅ Contract confirmed on blockchain");
  
  // Verify contract on PolygonScan
  if (hre.network.name !== "localhost" && hre.network.name !== "hardhat") {
    console.log("🔍 Verifying contract on PolygonScan...");
    try {
      await hre.run("verify:verify", {
        address: citiTrackReport.address,
        constructorArguments: [],
      });
      console.log("✅ Contract verified on PolygonScan");
    } catch (error) {
      console.log("❌ Verification failed:", error.message);
    }
  }
  
  // Test the contract
  console.log("\n🧪 Testing contract...");
  const tx = await citiTrackReport.anchorReport(
    "RPT-TEST-001",
    "created",
    "0x1234567890abcdef..."
  );
  await tx.wait();
  console.log("✅ Test anchor successful");
  
  const trail = await citiTrackReport.getReportTrail("RPT-TEST-001");
  console.log("📊 Retrieved trail:", trail.length, "events");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });