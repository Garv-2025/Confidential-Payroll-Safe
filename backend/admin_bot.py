import os
from web3 import Web3
from dotenv import load_dotenv

# 1. Setup and Connect
load_dotenv()
rpc_url = os.getenv("SEPOLIA_RPC_URL")
private_key = os.getenv("PRIVATE_KEY")

web3 = Web3(Web3.HTTPProvider(rpc_url))
account = web3.eth.account.from_key(private_key)

# 1. Configuration variables
WSS_ENDPOINT = "wss://eth-sepolia.g.alchemy.com/v2/QLTONUdBiYcSZUgsDJZPv"
CONTRACT_ADDRESS = "0x6D04A9Dc4AcDe7f658B8563D76f44D2ccF5748Ba"

# 2. Your Extracted Contract ABI (Updated for the new contract)
CONTRACT_ABI = [
    {"type":"constructor","inputs":[{"name":"_safeAccount","type":"address","internalType":"address"}],"stateMutability":"nonpayable"},
    {"type":"function","name":"employer","inputs":[],"outputs":[{"name":"","type":"address","internalType":"address"}],"stateMutability":"view"},
    {"type":"function","name":"payrollRulesHandle","inputs":[],"outputs":[{"name":"","type":"bytes32","internalType":"bytes32"}],"stateMutability":"view"},
    {"type":"function","name":"safeAccount","inputs":[],"outputs":[{"name":"","type":"address","internalType":"address"}],"stateMutability":"view"},
    {"type":"function","name":"setPayrollRules","inputs":[{"name":"encryptedHandle","type":"bytes32","internalType":"bytes32"}],"outputs":[],"stateMutability":"nonpayable"},
    {"type":"function","name":"withdrawEncryptedSalary","inputs":[{"name":"employee","type":"address","internalType":"address"},{"name":"amountOwed","type":"uint256","internalType":"uint256"},{"name":"userRequestHandle","type":"bytes32","internalType":"bytes32"}],"outputs":[],"stateMutability":"nonpayable"},
    {"type":"event","name":"PayrollRulesUpdated","inputs":[{"name":"employer","type":"address","indexed":True,"internalType":"address"},{"name":"encryptedHandle","type":"bytes32","indexed":False,"internalType":"bytes32"}],"anonymous":False},
    {"type":"event","name":"SalaryPaid","inputs":[{"name":"employee","type":"address","indexed":True,"internalType":"address"},{"name":"amount","type":"uint256","indexed":False,"internalType":"uint256"},{"name":"userRequestHandle","type":"bytes32","indexed":False,"internalType":"bytes32"}],"anonymous":False}
]

contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

def update_rules():
    print(f"🤖 Admin Wallet ({account.address}) connecting...")
    
    dummy_rules_hash = Web3.keccak(text="Hackathon_Payroll_Rules_v1")
    print(f"📦 Preparing to upload encrypted rules hash: {dummy_rules_hash.hex()}")

    nonce = web3.eth.get_transaction_count(account.address, 'pending')
    
    # 2. DYNAMIC GAS PRICING: Calculate gas based on live network block data
    latest_block = web3.eth.get_block('latest')
    base_fee = latest_block.get('baseFeePerGas', web3.to_wei('2', 'gwei'))
    max_priority_fee = web3.to_wei('2', 'gwei')
    max_fee = (base_fee * 2) + max_priority_fee

    tx_params = {
        'chainId': 11155111, # Sepolia
        'from': account.address,
        'nonce': nonce,
        'maxFeePerGas': max_fee,
        'maxPriorityFeePerGas': max_priority_fee,
    }

    # Build function call transaction data
    tx = contract.functions.setPayrollRules(dummy_rules_hash).build_transaction(tx_params)

    # 3. DYNAMIC GAS ESTIMATION: Ask node to estimate required gas + add 20% safety buffer
    estimated_gas = web3.eth.estimate_gas(tx)
    tx['gas'] = int(estimated_gas * 1.2)

    # Sign & Send
    print("✍️  Signing transaction with dynamic gas & nonce...")
    signed_tx = web3.eth.account.sign_transaction(tx, private_key=private_key)
    
    print("🚀 Sending to Sepolia Network...")
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    
    print(f"⏳ Waiting for confirmation. Tx Hash: {web3.to_hex(tx_hash)}")
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    print(f"✅ Success! Rules updated in Block Number: {receipt.blockNumber}")

if __name__ == "__main__":
    update_rules()