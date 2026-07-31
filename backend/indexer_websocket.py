import asyncio
import requests
import json
import time
from web3 import AsyncWeb3, WebSocketProvider
from web3.utils.subscriptions import LogsSubscription, LogsSubscriptionContext

# 1. Configuration variables
WSS_ENDPOINT = "wss://eth-sepolia.g.alchemy.com/v2/QLTONUdBiYcSZUgsDJZPv"
CONTRACT_ADDRESS = "0x6D04A9Dc4AcDe7f658B8563D76f44D2ccF5748Ba"

# 2. ABI
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
async def log_handler(handler_context: LogsSubscriptionContext) -> None:
    log_receipt = handler_context.result
    contract = handler_context.contract
    
    print("\n================ 🚨 LIVE EVENT DETECTED 🚨 ================")
    print(f"Block Number : {log_receipt.get('blockNumber')}")
    print(f"Tx Hash      : {log_receipt.get('transactionHash').hex()}")
    
    try:
        decoded_event = contract.events.PayrollRulesUpdated().process_log(log_receipt)
        employer = decoded_event['args']['employer']
        handle = decoded_event['args']['encryptedHandle'].hex()
        
        print("\n--- DECODED PAYLOAD ---")
        print(f"▸ Employer        : {employer}")
        print(f"▸ Encrypted Handle: {handle}")
        
        #  IExec TEE Simulation
        print("\n🔒 Initializing iExec Trusted Execution Environment (TEE)...")
        time.sleep(1)
        print("⚙️  Running confidential off-chain computation...")
        
        for i in range(1, 11):
            print(f"   [{'#' * i}{'.' * (10-i)}] {i*10}%", end="\r")
            time.sleep(0.3)
        
        print("\n✅ TEE Computation Complete. Cryptographic proof generated.")
        
        # --- THE FAKE DATABASE ---
        database_entry = {
            "status": "PROCESSED",
            "employer": employer,
            "encryptedHandle": handle,
            "timestamp": int(time.time()),
            "tee_proof": "0xMockProofGeneratedByIexecBlackBox892347"
        }
        
        with open("mock_database.json", "w") as db_file:
            json.dump(database_entry, db_file, indent=4)
            
        print("💾 Data written to mock_database.json!")

        # webhook
        webhook_url = "http://localhost:3000/api/webhook"
        payload = {
            "employer": employer,
            "encryptedHandle": handle,
            "tee_proof": database_entry["tee_proof"]
        }
        
        try:
            response = requests.post(webhook_url, json=payload)
            print(f"▸ Sent to Bridge  : Status {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("▸ Sent to Bridge  : ⚠️ Node server not running yet. Payload ready.")
            
    except Exception as e:
        print(f"\n⚠️ Could not decode log. Error details: {e}")
        print(f"Raw Data: {log_receipt.get('data')}")

    print("===========================================================\n")

async def sub_manager():
    w3 = await AsyncWeb3(WebSocketProvider(WSS_ENDPOINT))
    checksum_address = w3.to_checksum_address(CONTRACT_ADDRESS)
    
    contract = w3.eth.contract(address=checksum_address, abi=CONTRACT_ABI)

    print(f"📡 Connecting to Sepolia via WebSockets...")
    print(f"👁️ Monitoring contract: {checksum_address} for events...")

    await w3.subscription_manager.subscribe(
        [
            LogsSubscription(
                label="Contract Monitoring",
                address=checksum_address,
                handler=log_handler,
                handler_context={"contract": contract}
            )
        ]
    )

    try:
        await w3.subscription_manager.handle_subscriptions()
    except Exception as e:
        print(f"Connection error or closed: {e}")

if __name__ == "__main__":
    asyncio.run(sub_manager())