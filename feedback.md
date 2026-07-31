# iExec Developer Feedback: WTF Hackathon

**Project:** Confidential Payroll Safe
**Stack:** Python, Streamlit, Web3.py, Solidity

Overall, building with the iExec confidential computing layer (Nox) as a solo developer was a highly rewarding experience that allowed me to bridge a critical gap in enterprise Web3 adoption. 

Here is my honest feedback from the development process:

* **The Python/Web3.py Experience:** The majority of Web3 documentation heavily favors JavaScript/TypeScript. While I was able to successfully route encrypted payloads and broadcast to Sepolia using Python and Web3.py, having more explicit, native Python examples in the iExec documentation would drastically speed up onboarding for backend-focused developers.
* **Attestation Flow Testing:** Testing the TEE enclave attestation loop locally requires some mental gymnastics. A localized "mock enclave" testing environment or a sandbox specific to rapid UI prototyping would be a massive quality-of-life upgrade. 
* **Documentation:** The core concepts of Nox and the workercloud are well-documented, but diving into the specifics of custom smart contract integration required trial and error. Expanding the "Troubleshooting" sections for common on-chain deployment errors would be highly appreciated.

I am excited to take this MVP further and scale the frontend architecture in the future. Thank you for the support during the hackathon!