// Setup: npm install alchemy-sdk
import { Alchemy, Network } from "alchemy-sdk";

const config = {
  apiKey: "DDEUdTIi3FXhHcYRDTff8jVeSiz3dZwC",
  network: Network.ETH_MAINNET,
};
const alchemy = new Alchemy(config);

// Fetch all the NFTs owned by elanhalpern.eth
const main = async () => {
  // Get all NFTs
  const nfts = await alchemy.nft.getNftsForOwner("flurdao.eth");
  // Print NFTs
  console.log(nfts);
};

//myObj["Space Name"];
// Execute the code
const runMain = async () => {
  try {
    await main();
    process.exit(0);
  } catch (error) {
    console.log(error);
    process.exit(1);
  }
};

runMain();