const {
  Hbar,
  Client,
  PrivateKey,
  AccountCreateTransaction,
  TopicCreateTransaction,
  TopicMessageSubmitTransaction,
} = require("@hashgraph/sdk");
require("dotenv").config();

const myAccountId = process.env.ACCOUNT_ID;
const myPrivateKey = process.env.PRIVATE_KEY;

export const sendMessage = async (messageContent: any) => {
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

  if (process.env.TOPIC_ID === undefined) {
    // Create a new topic
    let txResponse = await new TopicCreateTransaction().execute(client);

    // Grab the newly generated topic ID
    let receipt = await txResponse.getReceipt(client);
    console.log(`Your topic ID is: ${receipt.topicId}`);

    process.env.TOPIC_ID = receipt.topicId;
    // Wait 5 seconds between consensus topic creation and subscription creation
    await new Promise((resolve) => setTimeout(resolve, 5000));
  }
  const topicId = process.env.TOPIC_ID;

  // Send message to private topic
  let submitMsgTx = await new TopicMessageSubmitTransaction({
    topicId: topicId,
    message: messageContent,
  }).freezeWith(client);

  let submitMsgTxSubmit = await submitMsgTx.execute(client);

  // Get the receipt of the transaction
  let getReceipt = await submitMsgTxSubmit.getReceipt(client);

  // Get the status of the transaction
  const transactionStatus = getReceipt.status;
  console.log("The message transaction status " + transactionStatus.toString());

  return { topicId: topicId, status: transactionStatus.toString() };
};
