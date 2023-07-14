from datetime import datetime
import json
import time
import requests


def load_etherscan_labels():
    data_path = "/home/martin/syve-code-snippets/etherscan_labels.json"
    data = json.load(open(data_path))
    return data


def get_protocol_contracts(token_address, etherscan_labels):
    token_label = etherscan_labels[token_address]["labels"][0]
    protocol_contract_addresses = []
    for contract_address in etherscan_labels:
        labels = etherscan_labels[contract_address]["labels"]
        if token_label in labels:
            protocol_contract_addresses.append(contract_address)
    return protocol_contract_addresses


def sql_fetch_num_contract_interactions(contract_addresses, from_timestamp, until_timestamp):
    contract_addresses_str = ", ".join(f"'{address}'" for address in contract_addresses)
    query = {
        "query": f"""
            SELECT COUNT(*) as count, to_address \
            FROM "eth_transactions" \
            WHERE to_address IN ({contract_addresses_str}) \
            AND "timestamp" BETWEEN '{from_timestamp}' AND '{until_timestamp}' \
            GROUP BY to_address
        """
    }
    url = "https://api.syve.ai/v1/sql"
    response = requests.post(url, json=query)
    records = response.json()
    return records


def test():
    etherscan_labels = load_etherscan_labels()
    token_address = "0xd33526068d116ce69f19a9ee46f0bd304f21a51f"  # Rocket Pool
    protocol_contracts = get_protocol_contracts(token_address, etherscan_labels)
    print("Number of contracts to count interactions for: ", len(protocol_contracts))
    output_path = "/home/martin/syve-code-snippets/rocket_pool_contract_counts.json"
    until_timestamp = int(datetime.now().timestamp())
    fromt_timestamp = until_timestamp - 365 * 86400
    fetch_start = time.time()
    print("Fetching interaction counts between ", fromt_timestamp, " and ", until_timestamp, "...")
    counts = sql_fetch_num_contract_interactions(
        contract_addresses=protocol_contracts,
        from_timestamp=fromt_timestamp,
        until_timestamp=until_timestamp,
    )
    print("Finished fetching - Took: ", time.time() - fetch_start)
    counts = sorted(counts, key=lambda x: -1 * x["count"], reverse=True)
    json.dump(counts, open(output_path, "w+"), indent=4)
    print("Saved smart contract counts to: ", output_path)


if __name__ == "__main__":
    test()
