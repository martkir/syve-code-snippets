from datetime import datetime
import json
import time
import requests


UNISWAP_V2_SWAP_SIGNATURE = "0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822"


def fetch_uniswap_v2_trades(pool_address, from_timestamp, until_timestamp, limit=10):
    address_str = pool_address
    query_str = f"""
        SELECT * FROM "eth_logs" \
        WHERE topic_0 = '{UNISWAP_V2_SWAP_SIGNATURE}' AND address = '{address_str}' \
        AND "@timestamp" BETWEEN '{from_timestamp}' AND '{until_timestamp}' \
        ORDER BY "@timestamp" DESC \
        LIMIT {limit}
    """
    query = {"query": query_str}
    url = "https://api.syve.ai/v1/sql"
    response = requests.post(url, json=query)
    records = response.json()
    return records


def fetch_pool_metadata(token_address):
    query_str = f"""
        SELECT * FROM "eth_pool_metadata" \
        WHERE "token_0_address" = '{token_address}' \
        OR "token_1_address" = '{token_address}' \
        LIMIT 10
    """
    query = {"query": query_str}
    url = "https://api.syve.ai/v1/sql"
    response = requests.post(url, json=query)
    records = response.json()
    return records


if __name__ == "__main__":
    token_address = "0x7391e573ddf984fb137a5de759b885c566ef28bc"
    pool_metadata = fetch_pool_metadata(token_address)
    time.sleep(0.2)
    pool_addresses = [record["pool_address"] for record in pool_metadata]
    now_timestamp = int(datetime.now().timestamp())

    for pool_address in pool_addresses:
        records = fetch_uniswap_v2_trades(
            pool_address="0xa43fe16908251ee70ef74718545e4fe6c5ccec9f",
            from_timestamp=now_timestamp - 86400,
            until_timestamp=now_timestamp,
            limit=5,
        )
        print(json.dumps(records, indent=4))
        exit()
