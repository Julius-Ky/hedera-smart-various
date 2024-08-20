import { Response, Request } from "express";
import { createFile } from "../../services/files";

interface File {
  fileContent: any;
}
const saveFile = async (req: Request, res: Response): Promise<void> => {
  try {
    const body = req.body as Pick<File, "fileContent">;
    console.log(`Saving file`);
    const fileId = await createFile(body.fileContent);
    res.status(200).json({ fileId: fileId });
  } catch (error) {
    console.log(error);
    res.status(400).json({ message: "An error occured saving the file" });
  }
};

export { saveFile };
