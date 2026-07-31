🛡️ PrivaPay Enterprise
Confidential B2B Web3 Payroll powered by iExec TEE and Ethereum Sepolia.

⚠️ The Problem
Public blockchains are inherently transparent. While this is great for decentralized finance, it is a non-starter for enterprise B2B applications. Traditional on-chain payroll protocols expose salary data, contractor addresses, and corporate cash flow to the entire world.

💡 The Solution
PrivaPay bridges the gap between Web3 settlement and Web2 privacy. By leveraging Trusted Execution Environments (TEE) via the iExec workercloud, PrivaPay encrypts payroll rules and executes salary distributions off-chain inside a secure Intel SGX enclave.

The result? Employees receive verifiable on-chain ETH payouts on Sepolia, while the corporate payroll logic and salary tiers remain strictly confidential.

🏗️ Architecture & Tech Stack
This repository contains our hackathon MVP, built to demonstrate the core cryptographic flow and UX.

Smart Contracts: Solidity (Deployed on Ethereum Sepolia)

Backend Logic: Python & Web3.py for transaction building and network broadcasting.

Frontend Interface: Streamlit for rapid Python-based UI prototyping and enterprise dashboard simulation.

Confidentiality Layer: Designed around iExec TEE (Note: The current MVP simulates the enclave attestation delay for demonstration purposes).

🚀 How to Run Locally (For Judges)
Follow these steps to run the enterprise dashboard on your local machine.

1. Clone the Repository
Bash
git clone https://github.com/your-username/privapay-enterprise.git
cd privapay-enterprise
2. Set Up Virtual Environment & Dependencies
Bash
python -m venv venv
source venv/Scripts/activate  # On Windows
# source venv/bin/activate    # On Mac/Linux

pip install streamlit web3 python-dotenv pandas
3. Environment Variables
Create a file named .env in the root directory and add your Sepolia credentials:

Plaintext
RPC_URL="https://eth-sepolia.g.alchemy.com/v2/YOUR_ALCHEMY_KEY"
PRIVATE_KEY="your_wallet_private_key_here"
(Ensure this wallet has a small amount of Sepolia ETH for gas fees).

4. Launch the Application
Bash
python -m streamlit run app.py
The dashboard will automatically open in your browser at http://localhost:8501.

🛣️ Future Roadmap
While this MVP successfully proves the confidential payout architecture, our immediate next steps for production scaling include:

Production Frontend Bridge: Transitioning this Streamlit prototype into a full React and Node.js application bridge to handle robust enterprise traffic and state management.

Advanced Contract Security: Migrating our contract testing framework to Foundry to run deeper fuzzing and security vulnerability audits on the payout distribution functions.

True TEE Integration: Replacing the simulated attestation flow with live iExec Oracle callbacks for strict on-chain verification.

Built for the WTF Hackathon (July 2026)