import { Response, Request } from "express";
import { deployContract } from "../../services/contracts";

interface Contract {
  abi: any;
  bytecode: any;
}
const uploadContract = async (req: Request, res: Response): Promise<void> => {
  try {
    const body = req.body as Pick<Contract, "abi" | "bytecode">;
    console.log(`Deploying the  contract`);
    const deploymentResponse = await deployContract(body.abi, body.bytecode);
    res.status(200).json(deploymentResponse);
  } catch (error) {
    console.log(error);
    res
      .status(400)
      .json({ message: "An error occured deploying the contract" });
  }
};

export { uploadContract };
