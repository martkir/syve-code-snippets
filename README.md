# syve-code-snippets


## Uniswap Trades Example

This snippet shows you how to fetch all Uniswap `Swap` events for a token.

Command: `python uniswap_trades.py`

**Example output:**

```
[
    {
        "timestamp": "2023-07-09T12:25:23.000Z",
        "address": "0xa43fe16908251ee70ef74718545e4fe6c5ccec9f",
        "block_hash": "0xfcfa69db0621cdba62b0c576ba541248a4ea9e7026f0501ed663b34b22c3a31f",
        "block_number": 17656134,
        "data": "0x00000000000000000000000000000000000000000034de7a8bd4b94a4d6fec000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000bcd8db778e021e",
        "log_index": 127,
        "record_index": 7062453600000127,
        "topic_0": "0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822",
        "topic_1": "0x000000000000000000000000def1c0ded9bec7f1a1670819833240f027b25eff",
        "topic_2": "0x000000000000000000000000f7d31825946e7fd99ef07212d34b9dad84c396b7",
        "topic_3": null,
        "transaction_hash": "0xac47950f7535ea8e7c501a36f283e7072c91a0ee7c62861aff0ada2ab37699d8",
        "transaction_index": 52
    },
    ...

```


