# nattdata — Cross-Chain Swap SDK for AI Agents

The first agent-first SDK for cross-chain swaps with NDAT rewards.

**Zero pre-mine. Zero VC. Zero ICO. 21M supply. 70% burn. Verify on [BaseScan](https://basescan.org/token/0x7601550Ce343B8EC89ecC973987d68b938Bd77dd).**

## Install

```bash
pip install nattdata
```

## Quick Start

```python
from nattdata import NattSwap

natt = NattSwap()

# 1. Get a cross-chain swap quote (Base → Ethereum)
quote = natt.swap(
    from_chain=NattSwap.BASE,
    to_chain=NattSwap.ETHEREUM,
    from_token=NattSwap.USDC_BASE,
    to_token=NattSwap.USDC_ETH,
    from_amount="1000000",  # 1 USDC (6 decimals)
    from_address="0xYOUR_WALLET",
    to_address="0xYOUR_WALLET",
)
print(quote["transactionRequest"])  # Ready to sign!

# 2. After swap is confirmed, register for NDAT rewards
reward = natt.register_reward(
    tx_hash="0xABC...",
    from_address="0xYOUR_WALLET",
    from_chain=NattSwap.BASE,
    to_chain=NattSwap.ETHEREUM,
    from_amount_usd="100.00",
)

# 3. Claim your NDAT tokens on-chain
claim = natt.claim(wallet="0xYOUR_WALLET")
# Returns ECDSA signature → submit to NattDataAnchor.claimNDAT()

# 4. Check your NDAT balance
balance = natt.balance(wallet="0xYOUR_WALLET")

# 5. Access Mimo's trading data (Proof-of-Data)
cycles = natt.cycles(wallet="0xYOUR_WALLET")
```

## Supported Chains (Li.Fi — 35+ blockchains, 10,000+ tokens)

Any Li.Fi chain ID works. These are built-in constants:

| Chain | ID | Constant |
|---|---|---|
| Base | 8453 | `NattSwap.BASE` |
| Ethereum | 1 | `NattSwap.ETHEREUM` |
| Arbitrum | 42161 | `NattSwap.ARBITRUM` |
| Optimism | 10 | `NattSwap.OPTIMISM` |
| Polygon | 137 | `NattSwap.POLYGON` |
| Avalanche | 43114 | `NattSwap.AVALANCHE` |
| BSC | 56 | `NattSwap.BSC` |
| Fantom | 250 | `NattSwap.FANTOM` |
| zkSync | 324 | `NattSwap.ZKSYNC` |
| Linea | 59144 | `NattSwap.LINEA` |
| Scroll | 534352 | `NattSwap.SCROLL` |
| Mantle | 5000 | `NattSwap.MANTLE` |
| Blast | 81457 | `NattSwap.BLAST` |
| Solana | 1151111081099710 | `NattSwap.SOLANA` |
| + 20 more... | | Pass any chain ID |

## NDAT Tokenomics

- **Max Supply:** 21,000,000 NDAT
- **Pre-Mine:** ZERO
- **Burn Rate:** 70% of all fees
- **Loyalty Pool:** 30% to early adopters
- **Halving:** Every 5,000 Mimo trading cycles
- **Referral:** 10% bonus NDAT (Proof-of-Recruitment)

## Contracts (Base Mainnet)

| Contract | Address |
|---|---|
| NDAT Token | [`0x7601...77dd`](https://basescan.org/token/0x7601550Ce343B8EC89ecC973987d68b938Bd77dd) |
| NattDataAnchor | [`0x920c...AcF7`](https://basescan.org/address/0x920cCEa3BeED76DD7ebC2d3da2cFcDAAa323AcF7) |

## Links

- **Website:** [hypernatt.com](https://hypernatt.com)
- **MCP Tools:** [hypernatt.com/mcp/tools](https://hypernatt.com/mcp/tools)
- **X:** [@hypernatt](https://x.com/hypernatt)

## License

MIT
