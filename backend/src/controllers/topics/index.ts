import { Response, Request } from "express";
import { sendMessage } from "../../services/topics";

interface Message {
  messageContent: any;
}
const saveMessage = async (req: Request, res: Response): Promise<void> => {
  try {
    const body = req.body as Pick<Message, "messageContent">;
    console.log(`Saving message`);
    const sendMessageResponse = await sendMessage(body.messageContent);
    res.status(200).json(sendMessageResponse);
  } catch (error) {
    console.log(error);
    res.status(400).json({ message: "An error occured saving the message" });
  }
};

export { saveMessage };
