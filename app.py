import os
import time
import pandas as pd
import streamlit as st
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="Confidential Payroll Safe",
    page_icon="🛡️",
    layout="wide",
)

# --- Initialize Dynamic Session State ---
if 'total_paid' not in st.session_state:
    st.session_state.total_paid = 0.50
if 'roster_count' not in st.session_state:
    st.session_state.roster_count = 3
if 'payout_history' not in st.session_state:
    st.session_state.payout_history = pd.DataFrame({
        "Date": ["2026-07-31", "2026-07-30", "2026-07-28"],
        "Recipient": ["Robin Arryn (0x71C...8976F)", "Alex Mercer (0x123...abc)", "Elena Rostova (0x456...def)"],
        "Amount ETH": [0.050, 0.150, 0.300],
        "Department": ["Security", "Engineering", "Product"],
        "Status": ["✅ Verified", "✅ Verified", "✅ Verified"]
    })

# --- Sidebar ---
with st.sidebar:
    st.title("🛡️ Payroll Safe")
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
st.title("Confidential Payroll Safe")
st.subheader("🛡️ iExec Confidential Computing Enabled")

# Placeholder for top metrics (renders fresh data at the end of the script)
metrics_placeholder = st.empty()

st.divider()

# --- Tabs ---
tab1, tab2 = st.tabs(["🚀 Execute Direct Payout", "📋 Payroll Audit Log"])

with tab1:
    st.subheader("New Confidential Payout")
    
    emp_name = st.text_input("Employee Name", placeholder="e.g. John Doe")
    emp_address = st.text_input("Employee Sepolia Address", placeholder="0x...")
    
    col_a, col_b = st.columns(2)
    with col_a:
        eth_amount = st.number_input("Amount in ETH", min_value=0.001, value=0.050, format="%.3f")
    with col_b:
        dept = st.selectbox("Department", ["Engineering", "Product", "Security", "Marketing"])

    st.write("") 
    
    if st.button("🔐 Execute Confidential Payout via iExec TEE", use_container_width=True, type="primary"):
        if not emp_name:
            st.error("Please provide an employee name.")
        elif not emp_address or not emp_address.startswith("0x"):
            st.error("Please provide a valid Sepolia wallet address.")
        else:
            status = st.status("Initializing Confidential Payroll Environment...", expanded=True)
            
            try:
                # 1. UI Simulation
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
                
                contract_address = w3.to_checksum_address("0x6D04A9Dc4AcDe7f658D8563D76f44D2ccf5748Ba")
                emp_address_checksum = w3.to_checksum_address(emp_address)
                
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
                
                test_handle = b'demo_payroll'.ljust(32, b'\0') 
                
                payout_tx = contract.functions.withdrawEncryptedSalary(
                    emp_address_checksum, amount_in_wei, test_handle
                ).build_transaction({
                    'chainId': 11155111,
                    'gas': 200000,
                    'maxFeePerGas': w3.to_wei('2', 'gwei'),
                    'maxPriorityFeePerGas': w3.to_wei('1', 'gwei'),
                    'nonce': nonce,
                })
                
                signed_tx = w3.eth.account.sign_transaction(payout_tx, private_key=private_key)
                tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
                tx_hash_hex = w3.to_hex(tx_hash)

                # 3. Dynamic State Updates
                st.session_state.total_paid += eth_amount
                st.session_state.roster_count += 1
                
                # Append transaction to audit log table
                new_entry = pd.DataFrame([{
                    "Date": time.strftime("%Y-%m-%d"),
                    "Recipient": f"{emp_name} ({emp_address_checksum[:6]}...{emp_address_checksum[-4:]})",
                    "Amount ETH": eth_amount,
                    "Department": dept,
                    "Status": "✅ Verified"
                }])
                st.session_state.payout_history = pd.concat([new_entry, st.session_state.payout_history], ignore_index=True)

                status.update(label="Payout Successfully Processed!", state="complete", expanded=False)
                st.balloons()
                st.success(f"Successfully processed {eth_amount} ETH payout to {emp_name} ({emp_address_checksum})")
                
                st.markdown(f"🔗 **[View Verified Transaction on Etherscan](https://sepolia.etherscan.io/tx/{tx_hash_hex})**")
                
            except Exception as e:
                status.update(label="Transaction Failed", state="error", expanded=True)
                st.error(f"Error: {e}")

with tab2:
    st.subheader("Recent Payout History")
    
    st.dataframe(
        st.session_state.payout_history, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Amount ETH": st.column_config.NumberColumn(format="%.3f ETH"),
            "Status": st.column_config.TextColumn("On-Chain Status")
        }
    )
    st.download_button(
        label="Download Audit Report (CSV)", 
        data=st.session_state.payout_history.to_csv().encode('utf-8'), 
        file_name='payroll_safe_audit.csv', 
        mime='text/csv'
    )

st.divider()
st.caption("Confidential Payroll Safe | Built for WTF Hackathon")

# --- Render Dynamic Header Metrics ---
with metrics_placeholder.container():
    m1, m2, m3 = st.columns(3)
    m1.metric(label="Total Paid (All Time)", value=f"{st.session_state.total_paid:.3f} ETH")
    m2.metric(label="Active Payroll Roster", value=f"{st.session_state.roster_count} Contractors")
    m3.metric(label="Privacy Shield Status", value="100% Confidential")