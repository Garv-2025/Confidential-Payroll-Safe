import os
import time
from web3 import Web3
from dotenv import load_dotenv

# Setup
load_dotenv()
rpc_url = os.getenv("SEPOLIA_RPC_URL")
web3 = Web3(Web3.HTTPProvider(rpc_url))

MODULE_ADDRESS = web3.to_checksum_address("0xc5407bDC504446B0d9A1D1Ca747C37738739387C")

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
    
    # Rewind to a block slightly BEFORE your successful transaction to catch it!
    last_scanned_block = 11368740 
    
    try:
        while True:
            try:
                current_block = web3.eth.block_number
                if current_block > last_scanned_block:
                    
                    logs = contract.events.PayrollRulesUpdated.get_logs(
                        from_block=last_scanned_block + 1,
                        to_block=current_block
                    )
                    
                    for log in logs:
                        employer = log['args']['employer']
                        handle = log['args']['encryptedHandle'].hex()
                        print(f"🎯 SECURE EVENT CAUGHT! Employer {employer} updated rules: {handle}")
                    
                    last_scanned_block = current_block
                    
            except Exception as e:
                # Silently catch the 400 Bad Request sync delay and wait for the node to catch up
                pass
            
            time.sleep(12)
            
    except KeyboardInterrupt:
        print("\n🛑 Indexer stopped by user.")

if __name__ == "__main__":
    monitor_events()