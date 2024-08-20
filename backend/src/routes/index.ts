import { Router } from "express";
import { uploadContract } from "../controllers/contracts";
import { saveFile } from "../controllers/files";
import { saveMessage } from "../controllers/topics";

const router: Router = Router();

//Contracts
router.post("/contract", uploadContract);

//Files
router.post("/file", saveFile);

//Messages
router.post("/message", saveMessage);

export default router;
