import os
from web3 import Web3
from dotenv import load_dotenv

# 1. Setup and Connect
load_dotenv()
rpc_url = os.getenv("SEPOLIA_RPC_URL")
private_key = os.getenv("PRIVATE_KEY")

web3 = Web3(Web3.HTTPProvider(rpc_url))
account = web3.eth.account.from_key(private_key)

# KEEP OLD ADDRESS FOR NOW — DO NOT CHANGE YET
CONTRACT_ADDRESS = web3.to_checksum_address("0xC198759A0b6dFFE4677AF788c00c1FF51D69F151")

ABI = [
    {
        "inputs": [{"internalType": "bytes32", "name": "encryptedHandle", "type": "bytes32"}],
        "name": "setPayrollRules",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

def update_rules():
    print(f"🤖 Admin Wallet ({account.address}) connecting...")
    
    dummy_rules_hash = Web3.keccak(text="Hackathon_Payroll_Rules_v1")
    print(f"📦 Preparing to upload encrypted rules hash: {dummy_rules_hash.hex()}")

    # 1. DYNAMIC NONCE: Use 'pending' to prevent transaction jams if run repeatedly
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
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    
    print(f"⏳ Waiting for confirmation. Tx Hash: {web3.to_hex(tx_hash)}")
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    print(f"✅ Success! Rules updated in Block Number: {receipt.blockNumber}")

if __name__ == "__main__":
    update_rules()