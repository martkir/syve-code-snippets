import json
import time
import requests


def fetch_token_creation_transfers(token_addresses):
    """
    "A token contract which creates new tokens SHOULD trigger a Transfer event with the _from address set to 0x0 when tokens are created."
    (See: https://eips.ethereum.org/EIPS/eip-20)
    """
    token_addresses_str = "', '".join(token_addresses)
    query_str = f"""
        SELECT * FROM eth_erc20 \
        WHERE token_address IN ('{token_addresses_str}') \
        AND from_address = '0x0000000000000000000000000000000000000000' LIMIT 1000
    """
    query = {"query": query_str}
    url = "https://api.syve.ai/v1/sql"
    response = requests.post(url, json=query)
    transfers = response.json()
    return transfers


def fetch_transactions_by_transaction_hashes(tx_hashes):
    tx_hashes_str = "', '".join(tx_hashes)
    query_str = f"""
        SELECT * FROM "syve_eth_transactions_data_stream_version-2" \
        WHERE transaction_hash IN ('{tx_hashes_str}') LIMIT 1000
    """
    query = {"query": query_str}
    url = "https://api.syve.ai/v1/sql"
    response = requests.post(url, json=query)
    transactions = response.json()
    return transactions


def main():
    token_addresses = [
        "0x12bac8c392f5a2ec82f3c2799289a1a7515d8f02",
        "0xb32f48647e53ac67e650e0e27423e676c04b356d",
        "0xdc9b75e5dfe429750e6bcd1d6b4b20ec6537e137",
        "0x7d5a4b2fa3ff259c9c4d730d6b523d7652878d82",
        "0xbbb6b9ce0d60b53ded1057c8cf6b3f5f6e9bae9c",
        "0xf4c65b0bcb17cc39a498285bd9cdda47a74b7109",
        "0x21378515c8cfa8078c026ccec54e57d13a683a80",
        "0x612a90cec0209a163deede0a429a84a163e3fc45",
        "0xd33526068d116ce69f19a9ee46f0bd304f21a51f",  # Rocket Pool
    ]

    transfers = fetch_token_creation_transfers(token_addresses)
    # Rate limit is 1 request per second:
    time.sleep(1)

    # Get the transaction hashes of when the tokens were created:
    transfers_map = {}
    for transfer in transfers:
        tx_hash = transfer["transaction_hash"]
        transfers_map[tx_hash] = transfer

    tx_hashes = list(transfers_map.keys())
    transactions = fetch_transactions_by_transaction_hashes(tx_hashes)
    time.sleep(1)

    output = []

    # The "from_address" of the transaction that created the token is the deployer address.
    output = {}
    for tx in transactions:
        deployer_address = tx["from_address"]
        token_address = transfers_map[tx["transaction_hash"]]["token_address"]
        output[deployer_address] = {
            "token_address": token_address,
            "contract_creation_events": [],
        }

    deployer_addresses = list(output.keys())

    # Looking for transactions with "from_address" = deployer_address and "to_address" = None
    deployer_addresses_str = "', '".join(deployer_addresses)
    query_str = f"""
        SELECT * FROM "eth_transactions" 
        WHERE "from_address" IN ('{deployer_addresses_str}') AND "to_address" IS NULL LIMIT 1000
    """
    query = {"query": query_str}
    url = "https://api.syve.ai/v1/sql"
    response = requests.post(url, json=query)
    transactions = response.json()

    for tx in transactions:
        deployer_address = tx["from_address"]
        output[deployer_address]["contract_creation_events"].append(
            {
                "transaction_hash": tx["transaction_hash"],
                "timestamp": tx["timestamp"],
                "block_number": tx["block_number"],
            }
        )
    print(json.dumps(output, indent=4))


if __name__ == "__main__":
    main()
