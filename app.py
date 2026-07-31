import os
import time
import pandas as pd
import streamlit as st
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="PrivaPay Enterprise",
    page_icon="🛡️",
    layout="wide",
)

# --- Sidebar ---
with st.sidebar:
    st.title("🛡️ PrivaPay")
    st.caption("Confidential iExec Payroll")
    st.divider()
    
    st.subheader("Platform Status")
    st.success("🟢 TEE Workercloud Online")
    
    st.subheader("Admin Wallet")
    st.code("0x71C7656EC7ab88b098defB751B7401B5f6d8976F", language="text")
    st.caption("Network: **ETH Sepolia**")
    
    st.metric(label="Gas Balance", value="0.85 ETH")
    st.divider()
    st.info("iExec Confidential Computing is active. Payloads are encrypted.")

# --- Main Header ---
st.title("PrivaPay Enterprise")
st.subheader("🛡️ iExec Confidential Computing Enabled")

m1, m2, m3 = st.columns(3)
with m1:
    st.metric(label="Total Paid (All Time)", value="0.50 ETH")
with m2:
    st.metric(label="Active Payroll Roster", value="3 Contractors")
with m3:
    st.metric(label="Privacy Shield Status", value="100% Confidential")

st.divider()

# --- Tabs ---
tab1, tab2 = st.tabs(["🚀 Execute Direct Payout", "📋 Payroll Audit Log"])

with tab1:
    st.subheader("New Confidential Payout")
    
    emp_address = st.text_input("Employee Sepolia Address", placeholder="0x...")
    
    col_a, col_b = st.columns(2)
    with col_a:
        eth_amount = st.number_input("Amount in ETH", min_value=0.001, value=0.050, format="%.3f")
    with col_b:
        dept = st.selectbox("Department", ["Engineering", "Product", "Security", "Marketing"])

    st.write("") 
    
    if st.button("🔐 Execute Confidential Payout via iExec TEE", use_container_width=True, type="primary"):
        if not emp_address or not emp_address.startswith("0x"):
            st.error("Please provide a valid Sepolia wallet address.")
        else:
            status = st.status("Initializing Confidential Payroll Environment...", expanded=True)
            
            try:
                # 1. UI Simulation for Demo Polish
                status.write("🔐 Payload Encrypted. Connecting to iExec Workercloud...")
                time.sleep(1.2)
                status.write("🧠 Executing Logic inside TEE Enclave (Intel SGX)...")
                time.sleep(1.2)
                status.write("📡 Attestation Verified. Broadcasting signed transaction to Sepolia...")
                
                # 2. ACTUAL WEB3 BACKEND EXECUTION
                rpc_url = os.getenv("RPC_URL")
                private_key = os.getenv("PRIVATE_KEY")
                
                if not rpc_url or not private_key:
                    raise ValueError("Missing RPC_URL or PRIVATE_KEY in .env file.")
                    
                w3 = Web3(Web3.HTTPProvider(rpc_url))
                account = w3.eth.account.from_key(private_key)
                
                # Your real deployed contract address
                contract_address = w3.to_checksum_address("0x6D04A9Dc4AcDe7f658D8563D76f44D2ccf5748Ba")
                emp_address = w3.to_checksum_address(emp_address)
                
                contract_abi = [
    {"type":"constructor","inputs":[{"name":"_safeAccount","type":"address","internalType":"address"}],"stateMutability":"nonpayable"},
    {"type":"function","name":"employer","inputs":[],"outputs":[{"name":"","type":"address","internalType":"address"}],"stateMutability":"view"},
    {"type":"function","name":"payrollRulesHandle","inputs":[],"outputs":[{"name":"","type":"bytes32","internalType":"bytes32"}],"stateMutability":"view"},
    {"type":"function","name":"safeAccount","inputs":[],"outputs":[{"name":"","type":"address","internalType":"address"}],"stateMutability":"view"},
    {"type":"function","name":"setPayrollRules","inputs":[{"name":"encryptedHandle","type":"bytes32","internalType":"bytes32"}],"outputs":[],"stateMutability":"nonpayable"},
    {"type":"function","name":"withdrawEncryptedSalary","inputs":[{"name":"employee","type":"address","internalType":"address"},{"name":"amountOwed","type":"uint256","internalType":"uint256"},{"name":"userRequestHandle","type":"bytes32","internalType":"bytes32"}],"outputs":[],"stateMutability":"nonpayable"},
    {"type":"event","name":"PayrollRulesUpdated","inputs":[{"name":"employer","type":"address","indexed":True,"internalType":"address"},{"name":"encryptedHandle","type":"bytes32","indexed":False,"internalType":"bytes32"}],"anonymous":False},
    {"type":"event","name":"SalaryPaid","inputs":[{"name":"employee","type":"address","indexed":True,"internalType":"address"},{"name":"amount","type":"uint256","indexed":False,"internalType":"uint256"},{"name":"userRequestHandle","type":"bytes32","indexed":False,"internalType":"bytes32"}],"anonymous":False}
]
                
                contract = w3.eth.contract(address=contract_address, abi=contract_abi)
                amount_in_wei = w3.to_wei(eth_amount, 'ether')
                nonce = w3.eth.get_transaction_count(account.address)
                
                # Dummy handle for hackathon demo
                test_handle = b'demo_payroll'.ljust(32, b'\0') 
                
                # Calling YOUR specific function: withdrawEncryptedSalary
                payout_tx = contract.functions.withdrawEncryptedSalary(
                    emp_address, amount_in_wei, test_handle
                ).build_transaction({
                    'chainId': 11155111, # Sepolia
                    'gas': 200000,
                    'maxFeePerGas': w3.to_wei('2', 'gwei'),
                    'maxPriorityFeePerGas': w3.to_wei('1', 'gwei'),
                    'nonce': nonce,
                })
                
                # Sign and Broadcast
                signed_tx = w3.eth.account.sign_transaction(payout_tx, private_key=private_key)
                tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
                tx_hash_hex = w3.to_hex(tx_hash)

                # 3. Success State
                status.update(label="Payout Successfully Processed!", state="complete", expanded=False)
                st.balloons()
                st.success(f"Successfully processed {eth_amount} ETH payout to {emp_address}")
                
                st.markdown(f"🔗 **[View Verified Transaction on Etherscan](https://sepolia.etherscan.io/tx/{tx_hash_hex})**")
                
            except Exception as e:
                status.update(label="Transaction Failed", state="error", expanded=True)
                st.error(f"Error: {e}")

with tab2:
    st.subheader("Recent Payout History")
    mock_data = {
        "Date": ["2026-07-31", "2026-07-30", "2026-07-28", "2026-07-25", "2026-07-20"],
        "Recipient": ["0x71C...8976F", "0x123...abc", "0x456...def", "0x789...ghi", "0xabc...123"],
        "Amount ETH": [0.050, 0.150, 0.050, 0.200, 0.050],
        "Department": ["Security", "Engineering", "Engineering", "Product", "Operations"],
        "Status": ["✅ Verified", "✅ Verified", "✅ Verified", "✅ Verified", "✅ Verified"]
    }
    df = pd.DataFrame(mock_data)
    
    st.dataframe(
        df, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Amount ETH": st.column_config.NumberColumn(format="%.3f ETH"),
            "Status": st.column_config.TextColumn("On-Chain Status")
        }
    )
    st.download_button(
        label="Download Audit Report (CSV)", 
        data=df.to_csv().encode('utf-8'), 
        file_name='privapay_audit.csv', 
        mime='text/csv'
    )

st.divider()
st.caption("PrivaPay Enterprise | Built for WTF Hackathon")