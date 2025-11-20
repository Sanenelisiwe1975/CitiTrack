/**
 * Verification script for deployed contract
 */
const hre = require("hardhat");

async function main() {
  const contractAddress = process.env.CONTRACT_ADDRESS;
  
  if (!contractAddress) {
    console.error("❌ CONTRACT_ADDRESS not set in environment");
    process.exit(1);
  }

  console.log("🔍 Verifying contract at:", contractAddress);

  try {
    await hre.run("verify:verify", {
      address: contractAddress,
      constructorArguments: [],
    });
    
    console.log("✅ Contract verified successfully");
  } catch (error) {
    if (error.message.includes("Already Verified")) {
      console.log("ℹ️  Contract already verified");
    } else {
      console.error("❌ Verification failed:", error.message);
      process.exit(1);
    }
  }
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });