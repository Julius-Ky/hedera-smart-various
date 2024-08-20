import { JsonRpcProvider } from "@ethersproject/providers";
import { Wallet } from "@ethersproject/wallet";
import { ContractFactory } from "@ethersproject/contracts";
import dotenv from "dotenv";
dotenv.config();

export const deployContract = async (abi: any, evmBytecode: any) => {
  const rpcUrl = process.env.RPC_URL;
  const accountId = process.env.ACCOUNT_ID;
  const accountKey: any = process.env.ECDSA_PRIVATE_KEY;

  // initialise account
  const rpcProvider = new JsonRpcProvider(rpcUrl);
  const accountWallet = new Wallet(accountKey, rpcProvider);
  const accountAddress = accountWallet.address;
  const accountExplorerUrl = `https://hashscan.io/testnet/address/${accountAddress}`;

  // deploy smart contract
  const myContractFactory = new ContractFactory(
    abi,
    evmBytecode,
    accountWallet
  );
  const myContract = await myContractFactory.deploy();
  await myContract.deployTransaction.wait();
  const myContractAddress = myContract.address;
  const myContractExplorerUrl = `https://hashscan.io/testnet/address/${myContractAddress}`;

  return {
    accountId,
    accountAddress,
    accountExplorerUrl,
    myContractAddress,
    myContractExplorerUrl,
  };
};
