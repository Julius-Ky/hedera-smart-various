![Logo- Smart various](https://github.com/user-attachments/assets/ba19d732-0c02-496f-bab2-2d18717c4499)
# Hedera-smart-various

**Smart Various** is an AI-powered platform designed to enhance the security and quality of Solidity smart contracts. Utilizing **Reinforcement Learning** and **Deep Q-Network (DQN)**, it analyzes, improves, and strengthens contracts. Key features include preventive security checks, automated corrections, detailed reporting, and a user-friendly interface. The platform supports on-chain data storage and AI model training through the **Hedera** network. It offers a free preliminary self-audit service to help developers address issues early and streamline final professional audits, ensuring the reliability and learning capability of Web3 applications. Stored data is provided in B2B and B2C formats via API and can be utilized as a security solution.

## Problems
As the blockchain technology and cryptocurrency markets continue to grow, security issues and malicious activities are also on the rise. Phishing, scams, and malicious contract codes are major concerns, especially as they often originate from compromised smart contract code and wallet approvals. In response to this, we propose an AI-powered platform for analyzing, modifying, and improving smart contract codes, providing detailed reports on identified issues and applied fixes.

## Solutions
1. **Security Analysis**: Automatically identifying vulnerabilities and potential security issues in smart contract code, distinguishing between scam contracts and legitimate ones.
2. **Code Enhancement**: Upgrading the code to improve security, efficiency, and compliance with best practices.
3. **Interoperability Conversion**: Converting smart contracts written in one language (e.g., Solidity for Ethereum) to another (e.g., for Hedera Hashgraph) to enable deployment across different blockchain platforms.
4. **Feedback and Reporting**: Providing detailed reports on the issues found, the improvements made, and the rationale behind changes.

## Process
![Untitled](https://github.com/user-attachments/assets/2bc20a17-4b29-47ea-b876-0609dcb57bb9)

## AI Model Process
![스크린샷 2024-08-19 110911](https://github.com/user-attachments/assets/d180b417-6e5b-4825-9234-73584ef32ebb)

## Tech
The AI Smart Module is designed to analyze solidity contracts and provide recommendations by using Reinforcement Learning Techniques.

### **Components**
- Deep Q-Network (DQN) for AI-driven decisions.
- Flask for API interaction and web service.
- JSON for data exchange and storage.
- Hedera a decentralized data management platform.

### Deep Q-Network (DQN) Model
**DQN explained simply:**
- The goal of a Deep Q-Network is to train a network (an agent) to approximate the value of the Q function that maps the optimal action according to the state by interacting with an environment.The agent is rewarded for correct moves and punished for the wrong ones.
- The target of the model is to classify: real from fake smart contract plus identify potential recommendations for smart contracts.

### Model Components
- **State Space:** "Unauthorized access", "Incomplete whitelists checks", "Lack of event logging", "Gas Efficiency", "Documentation".
- **Action Space:** The model will be able to discern either recommend improvement or leave as it is.
- **Reward Function:** Incentivizes correct identification and action.

### Infrastructure
- **Programming Languages: Python**
    - Not only handles the structure, logic of DQN model, but also the interaction between components.
- **HTML, CSS**
    - HTML provides web page structure, whereas CSS is mainly used to control web page styling.
- **Web Framework: Flask**
    - Provides API endpoints to access the model outputs and serve the data.
- **Data Format: JSON**
    - used for transmitting the model data in web applications , smart contract information, and other data.
- **Blockchain Platform: Hedera**
    - Decentralized platform that stores and displays data related to smart contracts using Hedera’s Service.

### Blockchain
- **Ethereum Virtual Machine (EVM): Solidity**
    - A contract-oriented, high-level programming language for building smart contracts.
- **Hedera SDKs & APIs: JavaScript**
    - Facilitate the process of performing queries from the Hedera Mirror Node API & Network Explorer

## Team
- Joseph Cho (Project Manager)
- Ana Ramirez (AI Engineer)
- Julius Kariuki (Software Engineer)
- Fahad (Researcher)

## Roadmap
> **2024 Q4**
- MVP Version Launching
- Success the AI Model V1.0
- Create the landing page
- Create the Docs

> **2025 Q1**
- AI model V1.5 upgrade (MVP version model update, additional development language support)
- Data updates stored on blockchain
- UX/UI updates

> **2025 Q2**
- Upgrade the AI Model V1.8 (Add the URL, Wallet address, Other  Smart contract language)
- Make the data collector API
- UX/UI Update

> **2025 Q3**
- AI Model V2.0 Main Launching
- Update the data collector API
- Data API business provision
- Partnership established (Certik, Hacken, Chalysis, etc...)
