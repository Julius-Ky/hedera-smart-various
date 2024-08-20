const {
  Hbar,
  Client,
  PrivateKey,
  AccountCreateTransaction,
  FileCreateTransaction,
} = require("@hashgraph/sdk");
require("dotenv").config();

export const createFile = async (fileContent: any) => {
  const myAccountId = process.env.ACCOUNT_ID;
  const myPrivateKey = process.env.PRIVATE_KEY;

  // If we weren't able to grab it, we should throw a new error
  if (myAccountId == null || myPrivateKey == null) {
    throw new Error(
      "Environment variables myAccountId and myPrivateKey must be present"
    );
  }

  // Create your connection to the Hedera Network
  const client = Client.forTestnet();
  client.setOperator(myAccountId, myPrivateKey);

  //Set the default maximum transaction fee (in Hbar)
  client.setDefaultMaxTransactionFee(new Hbar(100));

  //Set the maximum payment for queries (in Hbar)
  client.setDefaultMaxQueryPayment(new Hbar(50));

  // Create new keys
  const newAccountPrivateKey = PrivateKey.generateED25519();
  const newAccountPublicKey = newAccountPrivateKey.publicKey;

  // Create a new account with 1,000 tinybar starting balance
  const newAccount = await new AccountCreateTransaction()
    .setKey(newAccountPublicKey)
    .setInitialBalance(Hbar.fromTinybars(1000))
    .execute(client);

  // Get the new account ID
  const getReceipt = await newAccount.getReceipt(client);
  const newAccountId = getReceipt.accountId;

  console.log("\nNew account ID: " + newAccountId);

  //Create the transaction
  const transaction = await new FileCreateTransaction()
    .setKeys([newAccountPublicKey]) //A different key then the client operator key
    .setContents(fileContent)
    .setMaxTransactionFee(new Hbar(2))
    .freezeWith(client);

  //Sign with the file private key
  const signTx = await transaction.sign(newAccountPrivateKey);

  //Sign with the client operator private key and submit to a Hedera network
  const submitTx = await signTx.execute(client);

  //Request the receipt
  const receipt = await submitTx.getReceipt(client);

  //Get the file ID
  const newFileId = receipt.fileId;

  console.log("The new file ID is: " + newFileId);
  return newFileId.toString();
};
