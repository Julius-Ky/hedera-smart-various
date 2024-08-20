import express, { Express } from "express";
import dotenv from "dotenv";
import helmet from "helmet";
import routes from "./routes";

const cors = require("cors");
const bodyParser = require("body-parser");

dotenv.config();
const app: Express = express();

const PORT: string | number = process.env.PORT || 4800;

app.use(helmet());
app.use(cors());
app.use(bodyParser.json());
app.use(routes);

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
