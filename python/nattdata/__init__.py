"""
NattData SDK — The first agent-first SDK for cross-chain swaps with NDAT rewards.

Usage:
    from nattdata import NattSwap

    natt = NattSwap()
    quote = natt.swap(from_chain=8453, to_chain=1, from_token="0x833...", ...)
    balance = natt.balance(wallet="0xYOUR_WALLET")
    claim = natt.claim(wallet="0xYOUR_WALLET")
"""

from nattdata.client import NattSwap

__version__ = "1.1.0"
__all__ = ["NattSwap"]
