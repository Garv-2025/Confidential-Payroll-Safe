import os
import time
from web3 import Web3
from dotenv import load_dotenv

# Setup
load_dotenv()
rpc_url = os.getenv("SEPOLIA_RPC_URL")
web3 = Web3(Web3.HTTPProvider(rpc_url))

# ⚠️ UPDATE THIS WITH YOUR NEW V2 CONTRACT ADDRESS AFTER DEPLOYMENT
MODULE_ADDRESS = web3.to_checksum_address("0x0000000000000000000000000000000000000000")

# Minimal ABI specifically for the event we are targeting
ABI = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "employer", "type": "address"},
            {"indexed": False, "internalType": "bytes32", "name": "encryptedHandle", "type": "bytes32"}
        ],
        "name": "PayrollRulesUpdated",
        "type": "event"
    }
]

contract = web3.eth.contract(address=MODULE_ADDRESS, abi=ABI)

def monitor_events():
    print(f"🔒 Monitoring module {MODULE_ADDRESS} for encrypted events...")
    last_scanned_block = web3.eth.block_number
    
    try:
        while True:
            current_block = web3.eth.block_number
            if current_block > last_scanned_block:
                
                # Using get_logs to ensure we don't drop events on public RPCs
                logs = contract.events.PayrollRulesUpdated.get_logs(
                    fromBlock=last_scanned_block + 1,
                    toBlock=current_block
                )
                
                for log in logs:
                    employer = log['args']['employer']
                    handle = log['args']['encryptedHandle'].hex()
                    print(f"🎯 SECURE EVENT CAUGHT! Employer {employer} updated rules: {handle}")
                
                last_scanned_block = current_block
            
            time.sleep(12)
            
    except KeyboardInterrupt:
        print("\n🛑 Indexer stopped by user.")

if __name__ == "__main__":
    monitor_events()