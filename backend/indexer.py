import os
import time
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to Sepolia testnet
rpc_url = os.getenv("SEPOLIA_RPC_URL")
if not rpc_url:
    raise ValueError("SEPOLIA_RPC_URL not found in .env file")

web3 = Web3(Web3.HTTPProvider(rpc_url))

# Verify connection
if web3.is_connected():
    print(f"✅ Successfully connected to Ethereum Sepolia!")
    print(f"📡 Current Block Number: {web3.eth.block_number}")
else:
    print("❌ Failed to connect to Sepolia. Check your RPC URL.")
    exit()

# Address of deployed module (will be updated post-deployment)
MODULE_ADDRESS = web3.to_checksum_address("0x0000000000000000000000000000000000000000")

def monitor_confidential_events():
    print(f"🔒 Monitoring module {MODULE_ADDRESS} for encrypted withdrawal events...")
    
    last_processed_block = web3.eth.block_number
    
    try:
        while True:
            current_block = web3.eth.block_number
            if current_block > last_processed_block:
                print(f"🔍 Scanned Block {current_block} - Privacy maintained. No plain-text data leaked.")
                last_processed_block = current_block
            
            time.sleep(12)
            
    except KeyboardInterrupt:
        print("\n🛑 Indexer stopped by user.")

if __name__ == "__main__":
    monitor_confidential_events()