# TLDR Crypto — 2026-06-08
Source: https://tldr.tech/crypto/2026-06-08

## Articles

### HTX to Delist USD1 After World Liberty Financial Froze User Addresses
- **URL:** https://www.theblock.co/post/403885/htx-to-delist-trump-linked-usd1-after-saying-world-liberty-financial-froze-exchange-linked-addresses?utm_source=tldrcrypto
- **Via:** TLDR Crypto, 2026-06-08
- **Read time:** 2 minute read
- **TLDR Summary:** HTX is suspending all WLFI and USD1 trading pairs and forcibly converting every user's USD1 holdings into USDT after World Liberty Financial unilaterally froze on-chain addresses tied to HTX without warning and citing a UK sanctions compliance review. The exchange is pushing back hard, making clear that the frozen addresses belong to ordinary retail users who legally purchased their holdings, not to any sanctioned entity or HTX itself, and formally demanding WLFI lift the freeze immediately. The incident is the most direct collision yet between a politically connected US stablecoin project's compliance controls and the practical reality of exchange users being locked out of assets they had nothing to do with.

### Researcher Finds Undetectable Infinite-Mint Bug in Zcash Orchard Circuit
- **URL:** https://threadreaderapp.com/thread/2062677164865228948.html?utm_source=tldrcrypto
- **Via:** TLDR Crypto, 2026-06-08
- **Read time:** 2 minute read
- **TLDR Summary:** Shielded Labs commissioned a security researcher to audit the Zcash Orchard circuit, where he found a vulnerability that would have permitted unlimited ZEC minting without any on-chain trace. The flaw sat inside the Orchard shielded-pool zero-knowledge proving system, the layer that enforces supply integrity, meaning the same privacy properties protecting users would also conceal inflation from public detection. The bug was patched within days, but prior discovery or exploitation cannot be ruled out and is not provable without deeper forensic analysis. The researcher later added Monero to his audit scope, directing attention toward similar ZK circuit risks across privacy-focused chains.

### Morpho Rebrands to Open Credit Network and Releases Morpho Midnight
- **URL:** https://x.com/Morpho/status/2062855606101287397?utm_source=tldrcrypto
- **Via:** TLDR Crypto, 2026-06-08
- **Read time:** 4 minute read
- **TLDR Summary:** Morpho rebranded to "the open credit network for the world" and released the whitepaper and codebase for Morpho Midnight, a fixed-rate, fixed-term lending protocol built on the same isolated, immutable, permissionless architecture as Morpho Blue, with an explicit scope of putting $200T of global credit onchain. Midnight's core mechanic, "offered capital," keeps lender funds earning variable rates on Morpho Blue until a fixed-rate offer is matched, with positions sharing a maturity made fungible to allow early exit and late entry, directly addressing the capital commitment and liquidity fragmentation problems that caused prior fixed-rate protocols to fail. May integrations include Kraken's Bitcoin Vault, Trezor's Stablecoin Earn, Stable's StableEarn, and Circle Arc credit products running on Morpho, plus NASDAQ-listed Figure deploying home-equity-backed PRIME as collateral.

### pERC20: A Privacy-Native Fungible Token Standard for Ethereum
- **URL:** https://threadreaderapp.com/thread/2062459401802314025.html?utm_source=tldrcrypto
- **Via:** TLDR Crypto, 2026-06-08
- **Read time:** 3 minute read
- **TLDR Summary:** pERC20 is a proposed Ethereum token standard that deliberately breaks ERC-20 compatibility, replacing public balanceOf, approve, allowance, and transferFrom with a ZK note-based interface using Orchard-style Groth16 proofs. Tokens exist only as encrypted ZK-UTXO notes with no public-to-private shielding step required, and note-to-note transfers keep amounts and counterparties hidden on-chain. totalSupply remains public and a valueBalance == 0 constraint enforced on every transfer blocks covert inflation while preserving balance privacy. Compliance integrates via frozen-root binding, where each action commits to a cmxFrozenRoot and the ZK circuit must prove the spent note is absent from an admin-maintained sparse Merkle blacklist, enabling targeted note freezes without exposing other users' balances.

### How Intent-Based Payment Routing Works for X-Chain Money Movement
- **URL:** https://polygon.technology/learn/payment/how-intent-based-payment-routing-works-for-cross-chain-money-movement?utm_source=tldrcrypto
- **Via:** TLDR Crypto, 2026-06-08
- **Read time:** 3 minute read
- **TLDR Summary:** Polygon's explainer covers how intent-based routing, the approach underpinning its Open Money Stack and Trails orchestration layer, solves the cross-chain payments problem by letting users declare what they want (send X to Y on any chain) and letting the infrastructure resolve the how invisibly, routing across 16+ EVM chains without exposing developers or users to bridging complexity. Traditional bridges require users to understand source and destination chain mechanics, intent protocols abstract that into a signed declaration that solvers compete to fulfill optimally, handling routing, bridging, and execution in the background.

### 10 Crypto Sectors Most Likely to Survive and Grow Through H2 2026
- **URL:** https://x.com/PinkBrains_io/status/2062822321006817667?utm_source=tldrcrypto
- **Via:** TLDR Crypto, 2026-06-08
- **Read time:** 5 minute read
- **TLDR Summary:** Despite an 80%-90% Q1 2026 drawdown across AI agent tokens, the broader AI-crypto sector grew from roughly $9B to $22B-27B between early 2025 and May 2026, as onchain-usage-backed projects held value while zero-usage tokens collapsed. Agentic Finance is flagged as a top H2 survivor, built on EIP-7702 session-scoped wallet authority, Base AgentKit, lower inference costs from Kimi, DeepSeek, and Qwen, and agent frameworks including MCP, with HeyAnon, Wayfinder, Bankr, and senpi as named project candidates. AI compute DePIN held up better through Q1 with a roughly $9.4B market cap (+25%), roughly $150M January 2026 onchain revenue, and benchmarks shifting to compute utilization versus AWS spot pricing, led by Render's NVIDIA Blackwell B200 onboarding at roughly $38M in monthly onchain revenue and Bittensor's roughly $43M in Q1 AI-services revenue.

### The Four Ideologies of Bitcoin
- **URL:** https://x.com/saylor/status/2062853047991103638?utm_source=tldrcrypto
- **Via:** TLDR Crypto, 2026-06-08
- **Read time:** 6 minute read
- **TLDR Summary:** Saylor's essay maps Bitcoin's maturing community into four ideological camps that share conviction in Bitcoin's primacy but diverge on its trajectory. Maximalists treat Bitcoin as a singular monetary breakthrough, centering decentralization and protection against monetary debasement, while Capitalists argue Bitcoin reaches full potential only by integrating into TradFi structures including corporate balance sheets, credit instruments, and capital markets. Technologists push for continued protocol improvement, while Fundamentalists resist changes that risk corruption or regulatory capture of Bitcoin's core properties. Saylor frames the four camps as overlapping analytical lenses rather than factions, positioning their tensions as the central debates shaping Bitcoin's next phase of adoption.

### Uniswap's Hayden Adams: DeFi Is Proving Itself Inevitable
- **URL:** https://threadreaderapp.com/thread/2062932478545854637.html?utm_source=tldrcrypto
- **Via:** TLDR Crypto, 2026-06-08
- **Read time:** 2 minute read
- **TLDR Summary:** Hayden Adams draws a direct parallel between Uniswap's 2018 launch, at peak Ethereum bear market sentiment, and today, arguing the project's path forward is to build through the downturn again, this time proving DeFi is inevitable rather than merely possible. Adams expects the tokenization of existing assets alongside new crypto-native assets, with DeFi being integrated into payment processors, brokerages, and asset issuers until it absorbs the entire global financial stack.

### Marc Zeller Makes ether.fi Cash His Primary Card Over Gnosis Pay
- **URL:** https://threadreaderapp.com/thread/2063332932576743712.html?utm_source=tldrcrypto
- **Via:** TLDR Crypto, 2026-06-08
- **Read time:** 1 minute read
- **TLDR Summary:** Marc Zeller, founder of Aave Chan Initiative, says ether.fi Cash has displaced Gnosis Pay as his primary card after extended use, citing four advantages.

### Wallet Linked to Joseph Lubin Moves 110,000 ETH to Defend $259M DAI Debt Position
- **URL:** https://www.theblock.co/post/403876/wallet-linked-to-ethereum-co-founder-joseph-lubin-moves-110000-eth-to-defend-259m-dai-debt-position?utm_source=tldrcrypto
- **Via:** TLDR Crypto, 2026-06-08
- **Read time:** 2 minute read
- **TLDR Summary:** A wallet associated with Ethereum co-founder and Consensys CEO Joseph Lubin transferred 110,000 ETH, its first outflow in over three years, to MakerDAO in three tranches of 30k, 40k, and 40k ETH, adding collateral to a vault now holding over 137,000 WETH against roughly $259 million in borrowed DAI.

### Coinbase Launches Pre-IPO Perps Starting with SpaceX
- **URL:** https://threadreaderapp.com/thread/2062475039358816625.html?utm_source=tldrcrypto
- **Via:** TLDR Crypto, 2026-06-08
- **Read time:** 1 minute read
- **TLDR Summary:** Coinbase launched pre-IPO perpetual futures starting with SpaceX, available 24/7 to eligible non-US users, settled in USDC with no expiry.

### Bridge Co-Founder Zach Abrams: This Downturn Is Not 2022
- **URL:** https://threadreaderapp.com/thread/2063275751563293180.html?utm_source=tldrcrypto
- **Via:** TLDR Crypto, 2026-06-08
- **Read time:** 1 minute read
- **TLDR Summary:** When Bridge launched, Terra-Luna collapsed, FTX imploded, Bitcoin fell over 75%, and the entire crypto asset class was effectively uninvestable.

## Full Text

[HTX to Delist USD1 After World Liberty Financial Froze User Addresses (2 minute read)](https://www.theblock.co/post/403885/htx-to-delist-trump-linked-usd1-after-saying-world-liberty-financial-froze-exchange-linked-addresses?utm_source=tldrcrypto) HTX is suspending all WLFI and USD1 trading pairs and forcibly converting every user's USD1 holdings into USDT after World Liberty Financial unilaterally froze on-chain addresses tied to HTX without warning and citing a UK sanctions compliance review. The exchange is pushing back hard, making clear that the frozen addresses belong to ordinary retail users who legally purchased their holdings, not to any sanctioned entity or HTX itself, and formally demanding WLFI lift the freeze immediately. The incident is the most direct collision yet between a politically connected US stablecoin project's compliance controls and the practical reality of exchange users being locked out of assets they had nothing to do with.

[Researcher Finds Undetectable Infinite-Mint Bug in Zcash Orchard Circuit (2 minute read)](https://threadreaderapp.com/thread/2062677164865228948.html?utm_source=tldrcrypto) Shielded Labs commissioned a security researcher to audit the Zcash Orchard circuit, where he found a vulnerability that would have permitted unlimited ZEC minting without any on-chain trace. The flaw sat inside the Orchard shielded-pool zero-knowledge proving system, the layer that enforces supply integrity, meaning the same privacy properties protecting users would also conceal inflation from public detection. The bug was patched within days, but prior discovery or exploitation cannot be ruled out and is not provable without deeper forensic analysis. The researcher later added Monero to his audit scope, directing attention toward similar ZK circuit risks across privacy-focused chains.

[Morpho Rebrands to Open Credit Network and Releases Morpho Midnight (4 minute read)](https://x.com/Morpho/status/2062855606101287397?utm_source=tldrcrypto) Morpho rebranded to "the open credit network for the world" and released the whitepaper and codebase for Morpho Midnight, a fixed-rate, fixed-term lending protocol built on the same isolated, immutable, permissionless architecture as Morpho Blue, with an explicit scope of putting $200T of global credit onchain. Midnight's core mechanic, "offered capital," keeps lender funds earning variable rates on Morpho Blue until a fixed-rate offer is matched, with positions sharing a maturity made fungible to allow early exit and late entry, directly addressing the capital commitment and liquidity fragmentation problems that caused prior fixed-rate protocols to fail. May integrations include Kraken's Bitcoin Vault, Trezor's Stablecoin Earn, Stable's StableEarn, and Circle Arc credit products running on Morpho, plus NASDAQ-listed Figure deploying home-equity-backed PRIME as collateral.

[pERC20: A Privacy-Native Fungible Token Standard for Ethereum (3 minute read)](https://threadreaderapp.com/thread/2062459401802314025.html?utm_source=tldrcrypto) pERC20 is a proposed Ethereum token standard that deliberately breaks ERC-20 compatibility, replacing public balanceOf, approve, allowance, and transferFrom with a ZK note-based interface using Orchard-style Groth16 proofs. Tokens exist only as encrypted ZK-UTXO notes with no public-to-private shielding step required, and note-to-note transfers keep amounts and counterparties hidden on-chain. totalSupply remains public and a valueBalance == 0 constraint enforced on every transfer blocks covert inflation while preserving balance privacy. Compliance integrates via frozen-root binding, where each action commits to a cmxFrozenRoot and the ZK circuit must prove the spent note is absent from an admin-maintained sparse Merkle blacklist, enabling targeted note freezes without exposing other users' balances.

[QVAC by Tether: run local AI no one can see (Sponsor)](https://qvac.tether.io/blog/local-ai-without-memory-limits-how-qvacs-latest-upgrade-unlocks-5x-more-context-on-your-device/?utm_source=newsletter&amp;utm_medium=email&amp;utm_campaign=TLDRCrypto&amp;utm_term=secondaryjune8) QVAC, Tether's open-source local AI SDK, runs on your device. Run LLMs, build a local AI agent, generate images and video. Prompts never leave your machine. The latest update added TurboQuant, up to 5x more context. No subscription.  [See how it works](https://qvac.tether.io/blog/local-ai-without-memory-limits-how-qvacs-latest-upgrade-unlocks-5x-more-context-on-your-device/?utm_source=newsletter&utm_medium=email&utm_campaign=TLDRCrypto&utm_term=secondaryjune8)  or  [get it on GitHub](https://github.com/tetherto/qvac) .

[How Intent-Based Payment Routing Works for X-Chain Money Movement (3 minute read)](https://polygon.technology/learn/payment/how-intent-based-payment-routing-works-for-cross-chain-money-movement?utm_source=tldrcrypto) Polygon's explainer covers how intent-based routing, the approach underpinning its Open Money Stack and Trails orchestration layer, solves the cross-chain payments problem by letting users declare what they want (send X to Y on any chain) and letting the infrastructure resolve the how invisibly, routing across 16+ EVM chains without exposing developers or users to bridging complexity. Traditional bridges require users to understand source and destination chain mechanics, intent protocols abstract that into a signed declaration that solvers compete to fulfill optimally, handling routing, bridging, and execution in the background.

[10 Crypto Sectors Most Likely to Survive and Grow Through H2 2026 (5 minute read)](https://x.com/PinkBrains_io/status/2062822321006817667?utm_source=tldrcrypto) Despite an 80%-90% Q1 2026 drawdown across AI agent tokens, the broader AI-crypto sector grew from roughly $9B to $22B-27B between early 2025 and May 2026, as onchain-usage-backed projects held value while zero-usage tokens collapsed. Agentic Finance is flagged as a top H2 survivor, built on EIP-7702 session-scoped wallet authority, Base AgentKit, lower inference costs from Kimi, DeepSeek, and Qwen, and agent frameworks including MCP, with HeyAnon, Wayfinder, Bankr, and senpi as named project candidates. AI compute DePIN held up better through Q1 with a roughly $9.4B market cap (+25%), roughly $150M January 2026 onchain revenue, and benchmarks shifting to compute utilization versus AWS spot pricing, led by Render's NVIDIA Blackwell B200 onboarding at roughly $38M in monthly onchain revenue and Bittensor's roughly $43M in Q1 AI-services revenue.

[The Four Ideologies of Bitcoin (6 minute read)](https://x.com/saylor/status/2062853047991103638?utm_source=tldrcrypto) Saylor's essay maps Bitcoin's maturing community into four ideological camps that share conviction in Bitcoin's primacy but diverge on its trajectory. Maximalists treat Bitcoin as a singular monetary breakthrough, centering decentralization and protection against monetary debasement, while Capitalists argue Bitcoin reaches full potential only by integrating into TradFi structures including corporate balance sheets, credit instruments, and capital markets. Technologists push for continued protocol improvement, while Fundamentalists resist changes that risk corruption or regulatory capture of Bitcoin's core properties. Saylor frames the four camps as overlapping analytical lenses rather than factions, positioning their tensions as the central debates shaping Bitcoin's next phase of adoption.

[Uniswap's Hayden Adams: DeFi Is Proving Itself Inevitable (2 minute read)](https://threadreaderapp.com/thread/2062932478545854637.html?utm_source=tldrcrypto) Hayden Adams draws a direct parallel between Uniswap's 2018 launch, at peak Ethereum bear market sentiment, and today, arguing the project's path forward is to build through the downturn again, this time proving DeFi is inevitable rather than merely possible. Adams expects the tokenization of existing assets alongside new crypto-native assets, with DeFi being integrated into payment processors, brokerages, and asset issuers until it absorbs the entire global financial stack.

[Marc Zeller Makes ether.fi Cash His Primary Card Over Gnosis Pay (1 minute read)](https://threadreaderapp.com/thread/2063332932576743712.html?utm_source=tldrcrypto) Marc Zeller, founder of Aave Chan Initiative, says ether.fi Cash has displaced Gnosis Pay as his primary card after extended use, citing four advantages.

[Wallet Linked to Joseph Lubin Moves 110,000 ETH to Defend $259M DAI Debt Position (2 minute read)](https://www.theblock.co/post/403876/wallet-linked-to-ethereum-co-founder-joseph-lubin-moves-110000-eth-to-defend-259m-dai-debt-position?utm_source=tldrcrypto) A wallet associated with Ethereum co-founder and Consensys CEO Joseph Lubin transferred 110,000 ETH, its first outflow in over three years, to MakerDAO in three tranches of 30k, 40k, and 40k ETH, adding collateral to a vault now holding over 137,000 WETH against roughly $259 million in borrowed DAI.

[Coinbase Launches Pre-IPO Perps Starting with SpaceX (1 minute read)](https://threadreaderapp.com/thread/2062475039358816625.html?utm_source=tldrcrypto) Coinbase launched pre-IPO perpetual futures starting with SpaceX, available 24/7 to eligible non-US users, settled in USDC with no expiry.

[Bridge Co-Founder Zach Abrams: This Downturn Is Not 2022 (1 minute read)](https://threadreaderapp.com/thread/2063275751563293180.html?utm_source=tldrcrypto) When Bridge launched, Terra-Luna collapsed, FTX imploded, Bitcoin fell over 75%, and the entire crypto asset class was effectively uninvestable.