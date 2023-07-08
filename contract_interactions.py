from datetime import datetime
import json
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
            AND "@timestamp" BETWEEN '{from_timestamp}' AND '{until_timestamp}' \
            GROUP BY to_address
        """
    }
    url = "https://api.syve.ai/v1/sql"
    response = requests.post(url, json=query)
    records = response.json()
    return records


if __name__ == "__main__":
    etherscan_labels = load_etherscan_labels()
    token_address = "0xd33526068d116ce69f19a9ee46f0bd304f21a51f"  # Rocket Pool
    protocol_contracts = get_protocol_contracts(token_address, etherscan_labels)

    until_timestamp = int(datetime.now().timestamp())
    fromt_timestamp = until_timestamp - 365 * 86400
    counts = sql_fetch_num_contract_interactions(
        contract_addresses=protocol_contracts,
        from_timestamp=fromt_timestamp,
        until_timestamp=until_timestamp,
    )
    print(json.dumps(counts, indent=4))
