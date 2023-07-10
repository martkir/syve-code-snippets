import requests


def get_fetch_latest_prices(token_addresses):
    # Note: Maximum is 25 tokens for GET request
    token_addresses_str = ",".join(token_addresses)
    url = f"https://api.syve.ai/v1/price/latest?token_address={token_addresses_str}"
    response = requests.get(url)
    records = response.json()
    return records


def post_fetch_latest_prices(token_addresses):
    # Note: Maximum is 10,000 tokens for GET request
    url = f"https://api.syve.ai/v1/price/latest"
    response = requests.post(url, json=token_addresses)
    records = response.json()
    return records


def main():
    token_addresses = [
        "0xa876f27f13a9eb6e621202cefdd5afc4a90e6457",
        "0x6982508145454ce325ddbe47a25d4ec3d2311933",
        "0xc5fb36dd2fb59d3b98deff88425a3f425ee469ed",
        "0x31442e7d7c850fe05cbb2c67eca1e58c4d810984",
        "0x6fb83434b7d5b339ea6689581019ff1d44f475f5",
        "0x2216e873ea4282ebef7a02ac5aea220be6391a7c",
        "0x20364f78385ec4f46f33ee7795330dd815a87b1c",
        "0x432e9bca5a18a8cfcdae86120d134849b97deeb1",
        "0xcf9560b9e952b195d408be966e4f6cf4ab8206e5",
        "0x53fffb19bacd44b82e204d036d579e86097e5d09",
        "0x2c056f9402a0627bc0e580365bb12979fc011e2c",
        "0x278db13f1c0c1db6f815c6f85e54d82eab3946e3",
        "0xd8e2d95c8614f28169757cd6445a71c291dec5bf",
        "0x3b803cd0515dcff3ac958f2f11af168b85147136",
        "0xfb66321d7c674995dfcc2cb67a30bc978dc862ad",
        "0x388bc6728b3cab9e93bd79105d6ecb3db8431918",
    ]
    # records = get_fetch_latest_prices(token_addresses)
    records = post_fetch_latest_prices(token_addresses)
    for record in records:
        print(record.keys())


if __name__ == "__main__":
    main()
