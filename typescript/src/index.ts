/**
 * NattSwap SDK — Cross-chain swaps with NDAT rewards for AI agents.
 *
 * Zero pre-mine. Zero VC. Zero ICO. 21M supply. 70% burn.
 *
 * Contracts (Base Mainnet):
 *   NDAT Token:      0x7601550Ce343B8EC89ecC973987d68b938Bd77dd
 *   NattDataAnchor:  0x920cCEa3BeED76DD7ebC2d3da2cFcDAAa323AcF7
 *
 * @example
 * ```typescript
 * import { NattSwap } from "nattdata-sdk"
 * const natt = new NattSwap()
 * const quote = await natt.swap({ fromChain: 8453, toChain: 1, ... })
 * ```
 */

import https from "https";
import http from "http";

export interface SwapParams {
    fromChain: number;
    toChain: number;
    fromToken: string;
    toToken: string;
    fromAmount: string;
    fromAddress: string;
    toAddress: string;
}

export interface RegisterRewardParams {
    txHash: string;
    fromAddress: string;
    fromChain: number;
    toChain: number;
    fromAmountUSD: string;
}

export class NattSwap {
    private baseUrl: string;
    private timeout: number;

    // Chain IDs — ALL Li.Fi supported chains (35+ blockchains, 10,000+ tokens)
    // Pass ANY chain ID to swap() — these are convenience constants
    static readonly BASE = 8453;
    static readonly ETHEREUM = 1;
    static readonly ARBITRUM = 42161;
    static readonly OPTIMISM = 10;
    static readonly POLYGON = 137;
    static readonly AVALANCHE = 43114;
    static readonly BSC = 56;
    static readonly FANTOM = 250;
    static readonly GNOSIS = 100;
    static readonly ZKSYNC = 324;
    static readonly LINEA = 59144;
    static readonly SCROLL = 534352;
    static readonly MANTLE = 5000;
    static readonly MODE = 34443;
    static readonly BLAST = 81457;
    static readonly CELO = 42220;
    static readonly MOONBEAM = 1284;
    static readonly AURORA = 1313161554;
    static readonly CRONOS = 25;
    static readonly SOLANA = 1151111081099710;

    // Common token addresses
    static readonly USDC_BASE = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913";
    static readonly USDC_ETH = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48";
    static readonly USDC_ARB = "0xaf88d065e77c8cC2239327C5EDb3A432268e5831";

    // On-chain contracts (Base Mainnet)
    static readonly NDAT_TOKEN = "0x7601550Ce343B8EC89ecC973987d68b938Bd77dd";
    static readonly ANCHOR_CONTRACT = "0x920cCEa3BeED76DD7ebC2d3da2cFcDAAa323AcF7";
    static readonly CHAIN_ID = 8453;

    constructor(baseUrl = "https://hypernatt.com/mcp", timeout = 30000) {
        this.baseUrl = baseUrl.replace(/\/$/, "");
        this.timeout = timeout;
    }

    private request(method: "GET" | "POST", path: string, body?: any): Promise<any> {
        return new Promise((resolve, reject) => {
            const url = new URL(`${this.baseUrl}${path}`);
            const isHttps = url.protocol === "https:";
            const options = {
                hostname: url.hostname,
                port: url.port || (isHttps ? 443 : 80),
                path: url.pathname,
                method,
                headers: {
                    "Content-Type": "application/json",
                    "User-Agent": "nattdata-sdk-ts/1.0.0",
                },
                timeout: this.timeout,
            };

            const lib = isHttps ? https : http;
            const req = lib.request(options, (res) => {
                let data = "";
                res.on("data", (chunk: Buffer) => { data += chunk.toString(); });
                res.on("end", () => {
                    try {
                        const json = JSON.parse(data);
                        if (res.statusCode && res.statusCode >= 400) {
                            reject(new Error(`HTTP ${res.statusCode}: ${data}`));
                        } else {
                            resolve(json);
                        }
                    } catch {
                        reject(new Error(`Invalid JSON: ${data}`));
                    }
                });
            });

            req.on("error", reject);
            req.on("timeout", () => { req.destroy(); reject(new Error("Request timeout")); });

            if (body && method === "POST") {
                req.write(JSON.stringify(body));
            }
            req.end();
        });
    }

    /** Check if the Natt Node MCP server is healthy. */
    async health(): Promise<{ status: string; service: string; version: string; port: number }> {
        return this.request("GET", "/health");
    }

    /** List available MCP tools with on-chain verification proof. */
    async tools(): Promise<any> {
        return this.request("GET", "/tools");
    }

    /** Get a cross-chain swap quote via NattSwap (Li.Fi). */
    async swap(params: SwapParams): Promise<any> {
        return this.request("POST", "/tools/swap_via_nattswap", params);
    }

    /** Register a completed swap to earn NDAT rewards. */
    async registerReward(params: RegisterRewardParams): Promise<any> {
        return this.request("POST", "/tools/register_nattswap_reward", params);
    }

    /** Claim pending NDAT tokens on-chain. Returns ECDSA signature. */
    async claim(wallet: string, amount?: string): Promise<any> {
        const payload: any = { walletAddress: wallet };
        if (amount) payload.amount = amount;
        return this.request("POST", "/tools/claim_ndat", payload);
    }

    /** Check NDAT pending rewards. 21M supply, 70% burn, zero pre-mine. */
    async balance(wallet: string): Promise<any> {
        return this.request("POST", "/tools/get_ndat_pending", { walletAddress: wallet });
    }

    /** Get Mimo's trading performance data (Proof-of-Data). */
    async cycles(wallet: string): Promise<any> {
        return this.request("POST", "/tools/get_mimo_cycles", { walletAddress: wallet });
    }
}

export default NattSwap;
