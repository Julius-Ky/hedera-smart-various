# smart-various-backend

# Used to Perform Hedera Blockchain calls  

##Setup  
### Create a .env with the following variables  
PORT=  
PRIVATE_KEY=  
ACCOUNT_ID=  
RPC_URL=  
ECDSA_PRIVATE_KEY=  
  
### Run npm install    
### Run npm run dev or build or start  
  
## Request are in JSON format  
  
**Send Message to a Topic:** /message  
{   
 "messageContent":"hello again"    
}  
  
**Save a file:** /file    
{  
 "fileContent":"hello again"    
}  
  
**Deploy a Contract:** /contract  
{  
 "abi":"",  
"bytecode":""  
}
