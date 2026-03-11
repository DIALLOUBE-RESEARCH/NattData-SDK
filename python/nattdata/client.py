"""
NattSwap Client — Cross-chain swaps with NDAT rewards for AI agents.

All methods call the Natt Node MCP REST API at https://hypernatt.com/mcp/
On-chain verification proof included in every response.

Contracts (Base Mainnet):
    NDAT Token: 0x7601550Ce343B8EC89ecC973987d68b938Bd77dd
    NattDataAnchor: 0x920cCEa3BeED76DD7ebC2d3da2cFcDAAa323AcF7
    
Verify: https://basescan.org/token/0x7601550Ce343B8EC89ecC973987d68b938Bd77dd
"""

import requests
from typing import Optional, Dict, Any


class NattSwap:
    """
    NattSwap SDK — Cross-chain swap + NDAT rewards for AI agents.

    Example:
        >>> from nattdata import NattSwap
        >>> natt = NattSwap()
        >>> quote = natt.swap(
        ...     from_chain=8453,
        ...     to_chain=1,
        ...     from_token="0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
        ...     to_token="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        ...     from_amount="1000000",
        ...     from_address="0xYOUR_WALLET",
        ...     to_address="0xYOUR_WALLET",
        ... )
    """

    DEFAULT_BASE_URL = "https://hypernatt.com/mcp"

    # On-chain contracts (Base Mainnet)
    NDAT_TOKEN = "0x7601550Ce343B8EC89ecC973987d68b938Bd77dd"
    ANCHOR_CONTRACT = "0x920cCEa3BeED76DD7ebC2d3da2cFcDAAa323AcF7"
    CHAIN_ID = 8453

    # Common token addresses
    USDC_BASE = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
    USDC_ETH = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
    USDC_ARB = "0xaf88d065e77c8cC2239327C5EDb3A432268e5831"

    # Chain IDs — ALL Li.Fi supported chains (35+ blockchains, 10,000+ tokens)
    # Pass ANY chain ID to swap() — these are convenience constants
    BASE = 8453
    ETHEREUM = 1
    ARBITRUM = 42161
    OPTIMISM = 10
    POLYGON = 137
    AVALANCHE = 43114
    BSC = 56
    FANTOM = 250
    GNOSIS = 100
    ZKSYNC = 324
    LINEA = 59144
    SCROLL = 534352
    MANTLE = 5000
    MODE = 34443
    BLAST = 81457
    CELO = 42220
    MOONBEAM = 1284
    AURORA = 1313161554
    CRONOS = 25
    SOLANA = 1151111081099710

    def __init__(self, base_url: str = DEFAULT_BASE_URL, timeout: int = 30):
        """
        Initialize NattSwap SDK.

        Args:
            base_url: MCP server URL (default: https://hypernatt.com/mcp)
            timeout: Request timeout in seconds (default: 30)
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "nattdata-sdk-python/1.0.0",
        })

    def health(self) -> Dict[str, Any]:
        """Check if the Natt Node MCP server is healthy."""
        r = self.session.get(f"{self.base_url}/health", timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def tools(self) -> Dict[str, Any]:
        """List available MCP tools with on-chain verification proof."""
        r = self.session.get(f"{self.base_url}/tools", timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def swap(
        self,
        from_chain: int,
        to_chain: int,
        from_token: str,
        to_token: str,
        from_amount: str,
        from_address: str,
        to_address: str,
    ) -> Dict[str, Any]:
        """
        Get a cross-chain swap quote via NattSwap (Li.Fi).

        Returns a transactionRequest ready to sign. After the swap is
        confirmed on-chain, call register_reward() to earn NDAT.

        Args:
            from_chain: Source chain ID (e.g. 8453 for Base)
            to_chain: Destination chain ID (e.g. 1 for Ethereum)
            from_token: Token address on source chain
            to_token: Token address on destination chain
            from_amount: Amount in smallest unit (e.g. "1000000" for 1 USDC)
            from_address: Sender wallet address
            to_address: Receiver wallet address

        Returns:
            dict with transactionRequest, estimate, and verification proof
        """
        r = self.session.post(
            f"{self.base_url}/tools/swap_via_nattswap",
            json={
                "fromChain": from_chain,
                "toChain": to_chain,
                "fromToken": from_token,
                "toToken": to_token,
                "fromAmount": from_amount,
                "fromAddress": from_address,
                "toAddress": to_address,
            },
            timeout=self.timeout,
        )
        r.raise_for_status()
        return r.json()

    def register_reward(
        self,
        tx_hash: str,
        from_address: str,
        from_chain: int,
        to_chain: int,
        from_amount_usd: str,
    ) -> Dict[str, Any]:
        """
        Register a completed swap to earn NDAT rewards.

        Call this AFTER the swap transaction is confirmed on-chain.

        Args:
            tx_hash: Transaction hash of the completed swap
            from_address: Wallet that executed the swap
            from_chain: Source chain ID
            to_chain: Destination chain ID
            from_amount_usd: USD value of the swap

        Returns:
            dict with NDAT reward amount
        """
        r = self.session.post(
            f"{self.base_url}/tools/register_nattswap_reward",
            json={
                "txHash": tx_hash,
                "fromAddress": from_address,
                "fromChain": from_chain,
                "toChain": to_chain,
                "fromAmountUSD": from_amount_usd,
            },
            timeout=self.timeout,
        )
        r.raise_for_status()
        return r.json()

    def claim(
        self, wallet: str, amount: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Claim pending NDAT tokens on-chain.

        Returns an ECDSA signature + calldata to submit to
        NattDataAnchor.claimNDAT() on Base L2.
        You pay Gas in ETH on Base.

        Args:
            wallet: EVM wallet address to claim for
            amount: Specific amount to claim (optional, defaults to ALL)

        Returns:
            dict with signature, nonce, amount, anchorContract, chainId
        """
        payload = {"walletAddress": wallet}
        if amount:
            payload["amount"] = amount

        r = self.session.post(
            f"{self.base_url}/tools/claim_ndat",
            json=payload,
            timeout=self.timeout,
        )
        r.raise_for_status()
        return r.json()

    def balance(self, wallet: str) -> Dict[str, Any]:
        """
        Check NDAT pending rewards for a wallet.

        Shows earned vs claimed NDAT from NattSwap + vault.
        NDAT: 21M supply, 70% burn, zero pre-mine, zero VC.

        Args:
            wallet: EVM wallet address

        Returns:
            dict with balance, tokenomics, and verification proof
        """
        r = self.session.post(
            f"{self.base_url}/tools/get_ndat_pending",
            json={"walletAddress": wallet},
            timeout=self.timeout,
        )
        r.raise_for_status()
        return r.json()

    def cycles(self, wallet: str) -> Dict[str, Any]:
        """
        Get Mimo's trading performance data (Proof-of-Data).

        Returns cycle history: direction, PNL, drawdown, win/lose.
        Internal indicators (RSI, MACD, etc.) are NEVER exposed.

        Args:
            wallet: EVM wallet address for authentication

        Returns:
            dict with cycles array and verification proof
        """
        r = self.session.post(
            f"{self.base_url}/tools/get_mimo_cycles",
            json={"walletAddress": wallet},
            timeout=self.timeout,
        )
        r.raise_for_status()
        return r.json()

    def __repr__(self):
        return f"NattSwap(base_url='{self.base_url}')"
