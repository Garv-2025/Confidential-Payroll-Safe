# Confidential Payroll Safe

Confidential B2B Web3 Payroll powered by iExec TEE and Ethereum Sepolia.

## The Problem
Public blockchains are inherently transparent. While this is great for decentralized finance, it is a non-starter for enterprise B2B applications. Traditional on-chain payroll protocols expose salary data, contractor addresses, and corporate cash flow to the entire world.

## The Solution
Confidential Payroll Safe bridges the gap between Web3 settlement and Web2 privacy. By leveraging Trusted Execution Environments (TEE) via the iExec workercloud, payroll rules are encrypted and salary distributions are executed off-chain inside a secure Intel SGX enclave.

The result? Employees receive verifiable on-chain ETH payouts on Sepolia, while corporate payroll logic and salary tiers remain strictly confidential.

## Architecture & Tech Stack
This repository contains our hackathon MVP, built to demonstrate the core cryptographic flow and UX.

* **Smart Contracts:** Solidity (Deployed on Ethereum Sepolia)
* **Backend Logic:** Python & Web3.py
* **Frontend Interface:** Streamlit
* **Confidentiality Layer:** Designed around iExec TEE

## How to Run Locally

### 1. Clone the Repository
```bash
git clone [https://github.com/Garv-2025/Confidential-Payroll-Safe.git](https://github.com/Garv-2025/Confidential-Payroll-Safe.git)
cd Confidential-Payroll-Safe
2. Set Up Virtual Environment & Dependencies
Bash
python -m venv venv
source venv/Scripts/activate
pip install streamlit web3 python-dotenv pandas
3. Environment Variables
Create a file named .env in the root directory:

Plaintext
RPC_URL="[https://eth-sepolia.g.alchemy.com/v2/YOUR_ALCHEMY_KEY](https://eth-sepolia.g.alchemy.com/v2/YOUR_ALCHEMY_KEY)"
PRIVATE_KEY="your_wallet_private_key_here"
4. Launch the Application
Bash
python -m streamlit run app.py
Future Roadmap
Production Frontend Bridge: Transitioning this Streamlit prototype into a full React and Node.js application bridge.

Advanced Contract Security: Migrating our contract testing framework to Foundry to run deeper fuzzing and security vulnerability audits.

True TEE Integration: Replacing simulated attestation flows with live iExec Oracle callbacks for on-chain verification.

Built for the WTF Hackathon (July 2026)