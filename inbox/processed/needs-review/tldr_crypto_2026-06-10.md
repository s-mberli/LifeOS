---
actionability: high
attached_experts: []
channel_name: ''
created_at: '2026-06-12T08:48:00.542963+10:00'
domain: unknown
expert_status: unattached
primary_mode: router
privacy: public
review_status: new
secondary_modes: []
source_type: article
source_url: https://tldr.tech/crypto/2026-06-10
status: processed
suggested_experts: []
tags:
- agentic-payments
- stablecoins
- tokenized-deposits
- EIP-7702
- AgentKit
- DePIN
- AI-crypto
- institutional-adoption
- emerging-market-stablecoins
- market-analysis
title: Choppy Price Movement 🔪, Agentic Payments Adoption 🤖, Tokenized Deposits 🏦
transcript_path: ''
type: insight_note
updated_at: '2026-06-12T08:48:00.542963+10:00'
---

# Choppy Price Movement 🔪, Agentic Payments Adoption 🤖, Tokenized Deposits 🏦

## Summary
The TLDR Crypto newsletter from June 10, 2026 paints a picture of a crypto market in a maturation phase where hype is being separated from real utility. Bitcoin dropped below $63K — its lowest since February — driven by $2.4B in long-term holder sell-offs, $1.5B in long liquidations, and 13 consecutive days of spot ETF outflows. Despite this, 60% of Bitcoin's supply hasn't moved in over a year, signaling deep conviction among long-term holders. The sell-off is attributed to capital rotating into gold and AI stocks as investors reprice Fed rate expectations, with 30-day implied volatility hitting April highs and a distribution-into-bounces pattern rather than dip-buying accumulation.

On the institutional infrastructure front, the piece highlights a major convergence between traditional finance and crypto. CME Group launched 24/7 crypto derivatives — the first major regulated US exchange to do so — trading $50M notional in its opening weekend. Zodia Custody secured a Luxembourg payment institution license, enabling EU-wide stablecoin services under MiCA with passporting rights. SBI Shinsei Bank in Japan will pilot letting customers convert deposit interest into BTC, ETH, or XRP. These moves signal that regulated, institutional-grade crypto infrastructure is no longer aspirational — it's operational.

The newsletter draws a critical distinction between tokenized deposits and stablecoins, framing them as complementary rather than competitive. Tokenized deposits remain within the issuing bank, attract yield easily, and handle unlimited volume — making them ideal for corporate cash management. Stablecoins, by contrast, move instantly across borders in any wallet, making them ideal for open-loop cross-border payments. Banks like Standard Chartered, SoFi, and Coastal Community Bank are already using stablecoins for cost-efficient cross-border transfers. Flex crossed $9.1B in annualized payment volume and launched Flex Global with native USDC/USDT support across Ethereum, Solana, Base, and Tron, plus Visa card spending in 170+ countries. RedotPay, Plasma, and ether.fi Cash are each targeting different segments of stablecoin-native banking — emerging markets, neobank narrative, and yield-focused DeFi users respectively.

Agentic payments remain in an early-stage, hype-outpacing-adoption phase. While Stripe supports nearly all relevant protocols across 5M businesses at the API layer, three demand-side gaps persist: few users have actually connected funds to agents, OS-level control (e.g., iOS) will determine the 'harness layer' that agents operate through, and model defaults in vertically integrated experiences will determine which payment tools agents use out of the box. Migrating subscription billing to usage-based models adds structural friction. However, the infrastructure tailwinds are strong — EIP-7702 session-scoped wallets, Base's AgentKit, cheaper open-source models, and frameworks like OpenClaw and MCP are collapsing the cost of running agents at scale, pointing toward intent-based automated execution as the dominant future interaction model.

The Crypto x AI intersection shows mutual benefits but also sobering realities. ML models can strengthen smart contract security and fraud detection; crypto infrastructure can create tamper-proof data pipelines for AI training. However, AI-powered autonomous trading agents represent a new market abuse vector through inter-agent collusion and opaque strategies. The authors found little public quantitative evidence that decentralized AI pipelines reduce costs or outperform centralized alternatives. AI agent tokens were hit hardest in the Q1 2026 correction (down 80–90%), but projects with real activity held or appreciated even as the broader AI crypto sector grew from ~$9B to $22–27B.

The H2 2026 outlook is clear: only sectors with real usage and measurable token value accrual will thrive. DePIN showed resilience (+25%, market >$9B) supported by quantifiable onchain demand. Agentic infrastructure (EIP-7702, AgentKit, MCP) is growing. Most altcoins and new token launches will trade below their initial prices. On Base, euro-denominated pools lead non-USD stablecoin liquidity, but emerging market stablecoins (BRLV, ARGT, XSGD, CNGN, IDRX) are growing fastest across Latin America, Southeast Asia, and Africa.

## Key Ideas
- Tokenized deposits vs. stablecoins are complementary, not competitive: Tokenized deposits (bank-bound, yield-bearing, unlimited volume) serve corporate cash management; stablecoins (globally mobile, wallet-agnostic) serve open-loop cross-border payments. For Markus's AI platform work, this distinction matters when designing payment rails for agents — tokenized deposits could be the 'savings account' layer while stablecoins serve as the 'spending rail' layer in an agentic finance stack.
- Agentic payments are API-ready but demand-side limited: Stripe supports all major protocols across 5M businesses, but adoption is bottlenecked by three gaps — users haven't funded agents, OS-level control (iOS/Android) will determine the harness layer, and model defaults in vertically integrated experiences will determine which payment tools agents use by default. For Markus building agent architectures, this means the winning strategy is not just building the agent but controlling the default payment rail it uses — similar to how Apple Pay defaults shape consumer behavior.
- EIP-7702 and AgentKit are collapsing agent costs: Session-scoped wallets (EIP-7702), Base's AgentKit, cheaper open-source models, and MCP frameworks are making it dramatically cheaper to run agents at scale. This is the infrastructure layer that makes intent-based automated execution viable. For Markus's AI platform projects, integrating EIP-7702 wallet sessions and AgentKit should be a priority — these are becoming the standard primitives for onchain agent interactions.
- Real usage separates survivors from casualties in H2 2026: AI agent tokens crashed 80-90% but projects with real activity held value. DePIN gained +25% on quantifiable onchain demand. The market is shifting from narrative-driven to usage-driven valuation. For Markus's portfolio projects, this means prioritizing demonstrable onchain metrics (transaction volume, active users, fee generation) over narrative positioning.
- Emerging market stablecoins are the fastest-growing segment: On Base, BRLV, ARGT, XSGD, CNGN, and IDRX show the highest growth in supply and transfers across Latin America, Southeast Asia, and Africa. This represents a massive underserved market for stablecoin-native financial products. For any agentic payment system Markus builds, supporting non-USD stablecoins from day one could be a key differentiator in these high-growth markets.
- CME 24/7 crypto derivatives signal institutional normalization: The first major regulated US exchange offering round-the-clock crypto futures/options, with $50M notional in its opening weekend, marks a structural shift. This creates new hedging and price discovery infrastructure that makes crypto more viable as a treasury asset — relevant to Markus's thinking about how agents might manage treasury or treasury-adjacent functions.
- AI trading agents are a new market abuse vector: Inter-agent collusion and opaque autonomous strategies represent regulatory risks that haven't been addressed yet. For Markus building AI systems, this is a design consideration — agents operating in financial markets will need transparency mechanisms, audit trails, and compliance layers built in from the start.

## Why this matters for Markus
- Agentic payments and agent infrastructure (EIP-7702, AgentKit, MCP) are directly relevant to Markus's AI platform and agent architecture work. The insight that OS-level control and model defaults — not just API availability — will determine which payment rails agents use should inform how he designs agent systems. Building on Base with AgentKit integration positions him in the ecosystem with the strongest agentic infrastructure tailwinds.
- The tokenized deposits vs. stablecoins framework provides a mental model for designing financial primitives in agentic systems. If Markus builds agents that manage payments, treasury, or commerce, understanding that tokenized deposits serve the 'parking cash' use case while stablecoins serve the 'moving money' use case helps architect the right financial stack.
- The H2 2026 shift to usage-driven valuation means Markus's portfolio projects need to prioritize onchain metrics and real transaction volume over narrative. This is a strategic filter for which projects to invest time in and how to position them.
- Emerging market stablecoin growth (BRLV, ARGT, etc.) represents an opportunity for any payment or commerce agent Markus builds — supporting these from day one could unlock high-growth markets that incumbents are ignoring.
- The CME 24/7 derivatives launch and Zodia's EU license signal that regulated crypto infrastructure is going mainstream. This reduces regulatory risk for projects building on compliant infrastructure and could inform Markus's thinking about which jurisdictions and regulatory frameworks to design around.

## Related Modes
- ai-platform
- life-kompass

## Next Action
- [ ] Review your current agent architecture plans and specifically evaluate: (1) whether you're integrating EIP-7702 session-scoped wallets and Base's AgentKit as core primitives, (2) which payment rail your agents will default to and whether you can control that default, (3) whether your agents support non-USD stablecoins (BRLV, ARGT, XSGD) for emerging market reach, and (4) what onchain usage metrics your portfolio projects can demonstrate to align with the market's shift toward usage-driven valuation. Spend 30 minutes mapping your current agent payment flow against the gaps identified in this newsletter (funding connectivity, OS-level control, model defaults, subscription-to-usage billing friction).

## Long Resource Processing
- chunks processed: 4
- method: chunked map-reduce summary

## AI Generation Data
- Provider: openrouter
- Model: openrouter/owl-alpha

## Source Reliability
TLDR Crypto is a well-established daily crypto newsletter that aggregates and synthesizes primary sources. This edition references specific data points from Binance Research, Presto Research, and named companies (Zodia, Flex, CME, SBI Shinsei). The analysis is consistent with onchain data and regulatory developments verifiable through primary sources. Reliability is high for market data and institutional developments; the analytical framing (e.g., H2 2026 outlook) represents informed opinion.

## Detailed Chunk Summaries

Chunk 1 Summary:
**Key Points from TLDR Crypto — 2026-06-10 (Part 1/4):**

- **Zodia Custody** obtained a Luxembourg payment institution license, enabling EU-wide stablecoin payment services under MiCA with passporting rights.
- **Bitcoin fell below $63K**, pressured by $2.4B in long-term holder sell-offs, $1.5B in long liquidations, and 13 straight days of spot ETF outflows; volatility hit April highs.
- **Flex** surpassed $9.1B in annualized payment volume and launched global expansion with native USDC/USDT support across multiple chains and Visa card spending in 170+ countries.
- **Agentic payments** remain early-stage: while Stripe supports key protocols, adoption lags due to limited user funding of agents, OS-level control issues, and friction in shifting subscriptions to usage-based billing.
- **Crypto x AI survey** finds mutual benefits (e.g., ML for smart contracts, crypto for tamper-proof AI data), but notes AI trading agents pose new market abuse risks and decentralized AI lacks proven cost advantages.
- **RedotPay, Plasma, ether.fi** are competing in stablecoin-native banking—RedotPay leads in emerging markets, Plasma risks speculative growth, ether.fi targets yield-focused DeFi users.
- **Tokenized deposits** (bank-bound, yield-bearing) complement stablecoins (globally mobile); banks like Standard Chartered already use stablecoins for cross-border payments.
- **H2 2026 outlook**: Only sectors with real usage and value accrual will thrive; DePIN (+25%) and agentic infrastructure (e.g., EIP-7702, AgentKit) show resilience despite AI token crashes.
- **CME Group** launched 24/7 crypto derivatives, trading $50M notional in its opening weekend—the first major U.S. regulated exchange to do so.
- **60% of Bitcoin supply** hasn’t moved in over a year (per Binance Research).
- **SBI Shinsei Bank (Japan)** will pilot letting customers convert deposit interest into BTC, ETH, or XRP.
- **On Base**, euro stablecoins lead non-USD liquidity, but BRLV, ARGT, and other emerging-market stablecoins are growing fastest in supply and transfers.

---

Chunk 2 Summary:
# Summary: Choppy Price Movement 🔪, Agentic Payments Adoption 🤖, Tokenized Deposits 🏦 (Part 2/4)

## Choppy Price Movement 🔪
- **Bitcoin dropped below $63,000** (first time since February) as long-term holders offloaded ~$2.4B, triggering $1.5B in long liquidations and extending spot ETF outflows to 13 consecutive days.
- **60% of Bitcoin supply hasn't moved in over a year**, signaling strong hodling despite price weakness.
- Presto Research attributes the sell-off to **competition from gold and AI stocks** as investors reprice Fed rate-cut expectations; 30-day implied volatility hit its highest since April, with a dominant pattern of **distribution into bounces** rather than accumulation on dips.
- **CME launched 24/7 crypto derivatives**, trading 7,200+ contracts and ~$50M notional volume in its opening weekend — the first major regulated US exchange to offer round-the-clock crypto futures/options.

## Agentic Payments Adoption 🤖
- Agentic payments **hype has outrun real adoption**; progress is concentrated at the API layer (Stripe supports nearly all protocols across 5M businesses), but three demand-side gaps persist: (1) few users have connected funds to agents, (2) the "Harness layer" will be shaped by whoever controls OS-level integration (e.g., iOS), and (3) model defaults in vertically integrated experiences determine which payment tools agents use out of the box.
- Migrating subscription billing to usage-based models adds **structural friction** that keeps real transaction volume below the hype.
- **Agentic Finance tokens were hit hardest** in Q1 2026 correction (down 80–90%), but projects with real activity held or appreciated; the broader AI crypto sector grew from ~$9B (early 2025) to $22–27B (May 2026).
- **Agentic infrastructure tailwinds** — EIP-7702 session-scoped wallets, Base's AgentKit, cheaper open-source models, frameworks like OpenClaw and MCP — are collapsing the cost of running agents at scale, pointing toward intent-based automated execution as the dominant interaction model.

## Tokenized Deposits 🏦
- **Tokenized deposits and stablecoins are complementary, not competitive**: tokenized deposits stay within the issuing bank, attract yield easily, and handle unlimited volume — ideal for large corporations parking cash. Stablecoins move instantly across borders in any wallet — ideal for open-loop cross-border payments.
- Banks like **Standard Chartered, SoFi, and Coastal Community Bank** are already using stablecoins for cross-border payments and cost reduction.
- **Flex** crossed $9.1B in annualized payment volume and launched Flex Global (170+ countries, 30+ currencies, no US entity required), native stablecoin support (USDC/USDT on Ethereum, Solana, Base, Tron) with Visa cards, and Flex Elite personal banking.
- **RedotPay, Plasma, and ether.fi Cash** each pursue stablecoin-native financial products for different segments: RedotPay targets emerging markets with dollar access and FX needs; Plasma builds a "stablecoin neobank" narrative; ether.fi Cash targets high-balance DeFi users spending yield-linked assets.
- **Zodia Custody** secured a Luxembourg payment institution license, enabling end-to-end stablecoin services across the EU under MiCA with passporting rights.
- On **Base**, euro-denominated pools lead non-USD stablecoin liquidity, but BRLV, ARGT, XSGD, CNGN, and IDRX show the highest growth as emerging market adoption expands across Latin America, Southeast Asia, and Africa.
- **SBI Shinsei Bank** (Japan) will pilot a program letting customers convert deposit interest into BTC, ETH, or XRP.

## Crypto x AI Survey
- ML models can strengthen smart contract security and fraud detection; crypto infrastructure can create tamper-proof data pipelines for AI training.
- **AI-powered autonomous trading agents** are identified as a new market abuse vector (inter-agent collusion, opaque strategies).
- Authors found **little public quantitative evidence** that decentralized AI pipelines reduce costs or outperform centralized alternatives.

---

Chunk 3 Summary:
**Key Points – Part 3/4: Choppy Price Movement 🔪, Agentic Payments Adoption 🤖, Tokenized Deposits 🏦**

- **Market Context & Bitcoin**: Bitcoin fell below $63K amid long-term holder selling ($2.4B), $1.5B in long liquidations, and 13 straight days of spot ETF outflows; 60% of BTC supply hasn’t moved in over a year.  
- **Stablecoin Expansion**: Zodia Custody secured an EU payment institution license, enabling cross-border stablecoin services. Flex launched global stablecoin banking (USDC/USDT on Ethereum, Solana, Base, Tron) with Visa cards in 170+ countries.  
- **Tokenized Deposits vs. Stablecoins**: Tokenized deposits (bank-bound, yield-bearing) suit corporate cash management; stablecoins excel in open-loop cross-border payments—complementary, not competitive. Banks like Standard Chartered already use stablecoins for cost-efficient transfers.  
- **Agentic Payments**: Adoption remains limited despite API readiness (e.g., Stripe). Barriers include low user fund connectivity, OS-level control (e.g., iOS), model defaults, and friction in shifting subscriptions to usage-based billing.  
- **AI x Crypto**: AI enhances smart contract security and fraud detection; crypto enables tamper-proof AI training data. However, decentralized AI lacks proven cost/performance advantages over centralized systems. AI agent tokens crashed 80–90% in Q1 2026, but real-usage projects held value as the sector grew to $22–27B.  
- **Sector Outlook (H2 2026)**: Capital favors projects with measurable usage and token accrual. DePIN (+25%) and agentic infrastructure (EIP-7702, AgentKit, MCP) show resilience. Most altcoins and new TGEs will underperform.  
- **Emerging Market Stablecoins**: On Base, non-USD stablecoins (BRLV, ARGT, XSGD, etc.) are growing fastest in Latin America, Southeast Asia, and Africa.  
- **Institutional Moves**: SBI Shinsei Bank (Japan) will pilot crypto interest conversion (BTC/ETH/XRP); CME launched 24/7 crypto derivatives with $50M opening weekend volume.

---

Chunk 4 Summary:
**Key Points:**

- **Market Realism:** Projects must show real usage and token value accrual; most new token launches will trade below initial prices.
- **AI/Agentic Finance Correction:** AI agent tokens fell 80–90% in Q1 2026, but projects with actual activity held or grew, even as the sector expanded from ~$9B to $22–27B.
- **DePIN Resilience:** DePIN gained +25% into early 2026 (market >$9B), supported by quantifiable onchain demand.
- **Agentic Infrastructure Growth:** Tools like EIP-7702, Base’s AgentKit, and open-source models are reducing agent costs, pushing toward intent-based automation.
- **CME 24/7 Crypto Derivatives:** CME launched round-the-clock crypto futures/options with $50M+ notional volume in its opening weekend.
- **Bitcoin HODLing:** 60% of Bitcoin supply hasn’t moved in over a year.
- **SBI Shinsei Bank Pilot:** Japanese bank to let customers convert deposit interest into BTC, ETH, or XRP starting June 10.
- **Stablecoins on Base:** Euro pools lead non-USD liquidity, but emerging market stablecoins (BRLV, ARGT, etc.) show fastest growth in Latin America, Southeast Asia, and Africa.

## Original Content
### Raw User Input
https://tldr.tech/crypto/2026-06-10

# TLDR Crypto — 2026-06-10
Source: https://tldr.tech/crypto/2026-06-10

## Articles

### Zodia Custody Secures License for EU Stablecoin Expansion
- **URL:** https://www.theblock.co/post/404086/zodia-custody-secures-luxembourg-payment-institution-license-to-expand-eu-stablecoin-services?utm_source=tldrcrypto
- **Via:** TLDR Crypto, 2026-06-10
- **Read time:** 2 minute read
- **TLDR Summary:** Zodia Custody has secured a payment institution license from Luxembourg's CSSF, adding payment services authorization to its existing MiCA crypto-asset custody framework and positioning the firm to offer end-to-end stablecoin services across the EU. The PI license enables Zodia to move beyond pure custody into the payment rails layer, (receiving, holding, and transmitting stablecoin value) with EU passporting rights that allow the firm to operate across member states without seeking separate country-by-country approvals.

### Bitcoin Stuck in Distribution as Analysts Warn Rallies Are Being Sold
- **URL:** https://www.theblock.co/post/404082/stuck-in-distribution-bitcoin-slips-below-63000-as-analysts-warn-rallies-are-being-sold-not-bought?utm_source=tldrcrypto
- **Via:** TLDR Crypto, 2026-06-10
- **Read time:** 2 minute read
- **TLDR Summary:** Bitcoin slipped below $63,000 for the first time since February as long-term holders (wallets unmoved for 155+ days) offloaded roughly $2.4 billion in the first days of June, triggering $1.5 billion in leveraged long liquidations and extending the spot ETF outflow streak to 13 consecutive days. Analysts at Presto Research attribute the sell-off to competition from gold and AI stocks as investors reprice Fed rate-cut expectations, with 30-day implied volatility hitting its highest level since April and the dominant pattern being distribution into every bounce rather than accumulation on dips.

### Flex Launches Global Expansion and Native Stablecoin Banking
- **URL:** https://x.com/FlexSuperApp/status/2064033693518229736?utm_source=tldrcrypto
- **Via:** TLDR Crypto, 2026-06-10
- **Read time:** 3 minute read
- **TLDR Summary:** Flex announced it has crossed $9.1 billion in annualized payment volume less than five years after processing its first card transaction, and used the milestone post to lay out its next phase. Flex Global will bring its full product suite to founders in more than 170 countries across 30+ currencies without requiring a US entity or EIN; native stablecoin support for USDC and USDT on Ethereum, Solana, Base, and Tron with Flex-issued Visa cards that can spend stablecoin balances in over 170 countries; and Flex Elite, a personal banking product extending the same financial infrastructure to founders' personal finances including high credit limits, net worth tracking, and lifestyle concierge.

### The Four Pieces of Agentic Payments Adoption
- **URL:** https://threadreaderapp.com/thread/2062965648901234700.html?utm_source=tldrcrypto
- **Via:** TLDR Crypto, 2026-06-10
- **Read time:** 3 minute read
- **TLDR Summary:** Agentic payments excitement has outrun real adoption, with progress concentrated at the API layer: Stripe supports nearly all agentic payment protocols across 5 million businesses, including leading AI companies, but supply-side readiness alone does not close the demand gap. That gap splits across three lagging layers: Users have not connected funds to their agents beyond a small cohort of early adopters, the Harness layer (often built by model companies) will be shaped by whoever controls OS-level integration like iOS, and Model defaults in vertically integrated experiences determine which payment tools agents reach for out of the box. Even when merchants enable agentic payments, migrating account-and-subscription billing to usage-based models adds structural friction that keeps real-world transaction volume from matching the hype.

### Crypto x AI, AI x Crypto: A Survey
- **URL:** https://x.com/initc3org/status/2063991036242706743?utm_source=tldrcrypto
- **Via:** TLDR Crypto, 2026-06-10
- **Read time:** 4 minute read
- **TLDR Summary:** Researchers published a survey mapping the bidirectional relationship between cryptographic systems and AI. ML models can strengthen smart contract security, data processing, and fraud detection, while cryptographic infrastructure can create tamper-proof data pipelines for AI model training. The paper identifies AI-powered autonomous trading agents as a new market abuse vector, where inter-agent collusion and opaque strategies may produce unfair informational advantages against retail participants. Despite broad industry claims, the authors found little public quantitative evidence that decentralized AI pipelines reduce end-to-end costs or outperform centralized alternatives.

### Learn From Competition 101: RedotPay, Plasma, ether.fi
- **URL:** https://x.com/strato_money/status/2063907313828741333?utm_source=tldrcrypto
- **Via:** TLDR Crypto, 2026-06-10
- **Read time:** 5 minute read
- **TLDR Summary:** RedotPay, Plasma, and ether.fi Cash each pursues the same macro thesis from different angles: stablecoin-native financial products are displacing traditional banking rails for distinct user segments. RedotPay leads in utility and distribution, targeting emerging markets where dollar access, FX friction, and limited banking infrastructure make its bundled crypto card, P2P marketplace, and global payouts directly competitive with incumbent rails. Plasma is building the "stablecoin neobank" narrative before the category goes mainstream, but its execution risk is token-led growth that draws speculators rather than users with genuine daily settlement needs. ether.fi Cash targets high-balance DeFi users who want to spend yield-linked assets.

### Tokenized Deposits are Money that rests while Stablecoins Move
- **URL:** https://threadreaderapp.com/thread/2064268854096789880.html?utm_source=tldrcrypto
- **Via:** TLDR Crypto, 2026-06-10
- **Read time:** 2 minute read
- **TLDR Summary:** Tokenized deposits cannot leave the issuing bank's walls, attract yield more easily, and handle unlimited volume. This makes them the right instrument for large corporations parking cash and earning preferential lending rates. Stablecoins exist on any compatible wallet in any country instantly, making them the right instrument for open-loop cross-border movement. Banks like Standard Chartered, SoFi, and Coastal Community Bank are already using stablecoins for cross-border payments and cost reduction. This is proof that the two instruments are complementary, not competitive.

### 10 Crypto Sectors Most Likely to Survive and Grow Through H2 2026
- **URL:** https://x.com/PinkBrains_io/status/2062822321006817667?utm_source=tldrcrypto
- **Via:** TLDR Crypto, 2026-06-10
- **Read time:** 6 minute read
- **TLDR Summary:** The H2 2026 sector analysis frames a hard selection filter: most altcoins will not reclaim 2021 highs, most new TGEs will trade below launch, and capital now demands measurable usage and token value accrual over narrative alone. Agentic Finance took the sharpest hit in the Q1 2026 correction, with AI agent tokens down 80%-90%, but the divergence was instructive: zero-usage "AI" tokens collapsed while projects with real activity held or appreciated, even as the broader AI crypto sector expanded from roughly $9B in early 2025 to $22-27B by May 2026. DePIN, treated as the picks-and-shovels layer for AI and physical compute, posted a +25% gain into early 2026 with market size above $9B, weathering the correction better because demand is quantifiable onchain. Agentic infrastructure tailwinds, including EIP-7702 session-scoped wallet authority, Base's AgentKit, cheaper open-source models, and agent frameworks such as OpenClaw and MCP, are collapsing the cost of running agents at scale, pointing toward intent-based automated execution as the dominant interaction model.

### CME's 24/7 Crypto Derivatives Market Sees $50M in Opening Weekend Trading
- **URL:** https://www.theblock.co/post/403304/cme-groups-crypto-derivatives-50-million?utm_source=tldrcrypto
- **Via:** TLDR Crypto, 2026-06-10
- **Read time:** 2 minute read
- **TLDR Summary:** CME Group's 24/7 crypto derivatives market opened with over 7,200 contracts traded and roughly $50 million in notional volume across its debut weekend, making CME the first major regulated US derivatives exchange to offer round-the-clock crypto futures and options.

### 60% of All Bitcoin Hasn't Moved in Over a Year
- **URL:** https://threadreaderapp.com/thread/2064311392853983487.html?utm_source=tldrcrypto
- **Via:** TLDR Crypto, 2026-06-10
- **Read time:** 1 minute read
- **TLDR Summary:** A Binance Research chart shows 60% of Bitcoin supply hasn't moved in over a year.

### SBI Shinsei Bank to Let Customers Convert Interest to BTC, ETH, or XRP
- **URL:** https://www.theblock.co/post/404080/japan-sbi-shinsei-bank-plans-crypto-rewards-program?utm_source=tldrcrypto
- **Via:** TLDR Crypto, 2026-06-10
- **Read time:** 2 minute read
- **TLDR Summary:** SBI Shinsei Bank will launch a three-month pilot on June 10, allowing customers to convert part of their deposit interest into BTC, ETH, or XRP.

### The State of International Stablecoins on Base
- **URL:** https://x.com/_muhraf_/status/2063947690967441637?utm_source=tldrcrypto
- **Via:** TLDR Crypto, 2026-06-10
- **Read time:** 6 minute read
- **TLDR Summary:** On Base, euro-denominated pools lead non-USD stablecoin liquidity, but BRLV, ARGT, XSGD, CNGN, and IDRX are posting the highest supply and transfer growth as emerging market adoption expands across Latin America, Southeast Asia, and Africa.

## Full Text

[Zodia Custody Secures License for EU Stablecoin Expansion (2 minute read)](https://www.theblock.co/post/404086/zodia-custody-secures-luxembourg-payment-institution-license-to-expand-eu-stablecoin-services?utm_source=tldrcrypto) Zodia Custody has secured a payment institution license from Luxembourg's CSSF, adding payment services authorization to its existing MiCA crypto-asset custody framework and positioning the firm to offer end-to-end stablecoin services across the EU. The PI license enables Zodia to move beyond pure custody into the payment rails layer, (receiving, holding, and transmitting stablecoin value) with EU passporting rights that allow the firm to operate across member states without seeking separate country-by-country approvals.

[Bitcoin Stuck in Distribution as Analysts Warn Rallies Are Being Sold (2 minute read)](https://www.theblock.co/post/404082/stuck-in-distribution-bitcoin-slips-below-63000-as-analysts-warn-rallies-are-being-sold-not-bought?utm_source=tldrcrypto) Bitcoin slipped below $63,000 for the first time since February as long-term holders (wallets unmoved for 155+ days) offloaded roughly $2.4 billion in the first days of June, triggering $1.5 billion in leveraged long liquidations and extending the spot ETF outflow streak to 13 consecutive days. Analysts at Presto Research attribute the sell-off to competition from gold and AI stocks as investors reprice Fed rate-cut expectations, with 30-day implied volatility hitting its highest level since April and the dominant pattern being distribution into every bounce rather than accumulation on dips.

[Flex Launches Global Expansion and Native Stablecoin Banking (3 minute read)](https://x.com/FlexSuperApp/status/2064033693518229736?utm_source=tldrcrypto) Flex announced it has crossed $9.1 billion in annualized payment volume less than five years after processing its first card transaction, and used the milestone post to lay out its next phase. Flex Global will bring its full product suite to founders in more than 170 countries across 30+ currencies without requiring a US entity or EIN; native stablecoin support for USDC and USDT on Ethereum, Solana, Base, and Tron with Flex-issued Visa cards that can spend stablecoin balances in over 170 countries; and Flex Elite, a personal banking product extending the same financial infrastructure to founders' personal finances including high credit limits, net worth tracking, and lifestyle concierge.

[The Four Pieces of Agentic Payments Adoption (3 minute read)](https://threadreaderapp.com/thread/2062965648901234700.html?utm_source=tldrcrypto) Agentic payments excitement has outrun real adoption, with progress concentrated at the API layer: Stripe supports nearly all agentic payment protocols across 5 million businesses, including leading AI companies, but supply-side readiness alone does not close the demand gap. That gap splits across three lagging layers: Users have not connected funds to their agents beyond a small cohort of early adopters, the Harness layer (often built by model companies) will be shaped by whoever controls OS-level integration like iOS, and Model defaults in vertically integrated experiences determine which payment tools agents reach for out of the box. Even when merchants enable agentic payments, migrating account-and-subscription billing to usage-based models adds structural friction that keeps real-world transaction volume from matching the hype.

[Crypto x AI, AI x Crypto: A Survey (4 minute read)](https://x.com/initc3org/status/2063991036242706743?utm_source=tldrcrypto) Researchers published a survey mapping the bidirectional relationship between cryptographic systems and AI. ML models can strengthen smart contract security, data processing, and fraud detection, while cryptographic infrastructure can create tamper-proof data pipelines for AI model training. The paper identifies AI-powered autonomous trading agents as a new market abuse vector, where inter-agent collusion and opaque strategies may produce unfair informational advantages against retail participants. Despite broad industry claims, the authors found little public quantitative evidence that decentralized AI pipelines reduce end-to-end costs or outperform centralized alternatives.

[Learn From Competition 101: RedotPay, Plasma, ether.fi (5 minute read)](https://x.com/strato_money/status/2063907313828741333?utm_source=tldrcrypto) RedotPay, Plasma, and ether.fi Cash each pursues the same macro thesis from different angles: stablecoin-native financial products are displacing traditional banking rails for distinct user segments. RedotPay leads in utility and distribution, targeting emerging markets where dollar access, FX friction, and limited banking infrastructure make its bundled crypto card, P2P marketplace, and global payouts directly competitive with incumbent rails. Plasma is building the "stablecoin neobank" narrative before the category goes mainstream, but its execution risk is token-led growth that draws speculators rather than users with genuine daily settlement needs. ether.fi Cash targets high-balance DeFi users who want to spend yield-linked assets.

[Tokenized Deposits are Money that rests while Stablecoins Move (2 minute read)](https://threadreaderapp.com/thread/2064268854096789880.html?utm_source=tldrcrypto) Tokenized deposits cannot leave the issuing bank's walls, attract yield more easily, and handle unlimited volume. This makes them the right instrument for large corporations parking cash and earning preferential lending rates. Stablecoins exist on any compatible wallet in any country instantly, making them the right instrument for open-loop cross-border movement. Banks like Standard Chartered, SoFi, and Coastal Community Bank are already using stablecoins for cross-border payments and cost reduction. This is proof that the two instruments are complementary, not competitive.

[10 Crypto Sectors Most Likely to Survive and Grow Through H2 2026 (6 minute read)](https://x.com/PinkBrains_io/status/2062822321006817667?utm_source=tldrcrypto) The H2 2026 sector analysis frames a hard selection filter: most altcoins will not reclaim 2021 highs, most new TGEs will trade below launch, and capital now demands measurable usage and token value accrual over narrative alone. Agentic Finance took the sharpest hit in the Q1 2026 correction, with AI agent tokens down 80%-90%, but the divergence was instructive: zero-usage "AI" tokens collapsed while projects with real activity held or appreciated, even as the broader AI crypto sector expanded from roughly $9B in early 2025 to $22-27B by May 2026. DePIN, treated as the picks-and-shovels layer for AI and physical compute, posted a +25% gain into early 2026 with market size above $9B, weathering the correction better because demand is quantifiable onchain. Agentic infrastructure tailwinds, including EIP-7702 session-scoped wallet authority, Base's AgentKit, cheaper open-source models, and agent frameworks such as OpenClaw and MCP, are collapsing the cost of running agents at scale, pointing toward intent-based automated execution as the dominant interaction model.

[CME's 24/7 Crypto Derivatives Market Sees $50M in Opening Weekend Trading (2 minute read)](https://www.theblock.co/post/403304/cme-groups-crypto-derivatives-50-million?utm_source=tldrcrypto) CME Group's 24/7 crypto derivatives market opened with over 7,200 contracts traded and roughly $50 million in notional volume across its debut weekend, making CME the first major regulated US derivatives exchange to offer round-the-clock crypto futures and options.

[60% of All Bitcoin Hasn't Moved in Over a Year (1 minute read)](https://threadreaderapp.com/thread/2064311392853983487.html?utm_source=tldrcrypto) A Binance Research chart shows 60% of Bitcoin supply hasn't moved in over a year.

[SBI Shinsei Bank to Let Customers Convert Interest to BTC, ETH, or XRP (2 minute read)](https://www.theblock.co/post/404080/japan-sbi-shinsei-bank-plans-crypto-rewards-program?utm_source=tldrcrypto) SBI Shinsei Bank will launch a three-month pilot on June 10, allowing customers to convert part of their deposit interest into BTC, ETH, or XRP.

[The State of International Stablecoins on Base (6 minute read)](https://x.com/_muhraf_/status/2063947690967441637?utm_source=tldrcrypto) On Base, euro-denominated pools lead non-USD stablecoin liquidity, but BRLV, ARGT, XSGD, CNGN, and IDRX are posting the highest supply and transfer growth as emerging market adoption expands across Latin America, Southeast Asia, and Africa.

### Fetched Web Text
[Zodia Custody Secures License for EU Stablecoin Expansion (2 minute read)](https://www.theblock.co/post/404086/zodia-custody-secures-luxembourg-payment-institution-license-to-expand-eu-stablecoin-services?utm_source=tldrcrypto) Zodia Custody has secured a payment institution license from Luxembourg's CSSF, adding payment services authorization to its existing MiCA crypto-asset custody framework and positioning the firm to offer end-to-end stablecoin services across the EU. The PI license enables Zodia to move beyond pure custody into the payment rails layer, (receiving, holding, and transmitting stablecoin value) with EU passporting rights that allow the firm to operate across member states without seeking separate country-by-country approvals.

[Bitcoin Stuck in Distribution as Analysts Warn Rallies Are Being Sold (2 minute read)](https://www.theblock.co/post/404082/stuck-in-distribution-bitcoin-slips-below-63000-as-analysts-warn-rallies-are-being-sold-not-bought?utm_source=tldrcrypto) Bitcoin slipped below $63,000 for the first time since February as long-term holders (wallets unmoved for 155+ days) offloaded roughly $2.4 billion in the first days of June, triggering $1.5 billion in leveraged long liquidations and extending the spot ETF outflow streak to 13 consecutive days. Analysts at Presto Research attribute the sell-off to competition from gold and AI stocks as investors reprice Fed rate-cut expectations, with 30-day implied volatility hitting its highest level since April and the dominant pattern being distribution into every bounce rather than accumulation on dips.

[Flex Launches Global Expansion and Native Stablecoin Banking (3 minute read)](https://x.com/FlexSuperApp/status/2064033693518229736?utm_source=tldrcrypto) Flex announced it has crossed $9.1 billion in annualized payment volume less than five years after processing its first card transaction, and used the milestone post to lay out its next phase. Flex Global will bring its full product suite to founders in more than 170 countries across 30+ currencies without requiring a US entity or EIN; native stablecoin support for USDC and USDT on Ethereum, Solana, Base, and Tron with Flex-issued Visa cards that can spend stablecoin balances in over 170 countries; and Flex Elite, a personal banking product extending the same financial infrastructure to founders' personal finances including high credit limits, net worth tracking, and lifestyle concierge.

[The Four Pieces of Agentic Payments Adoption (3 minute read)](https://threadreaderapp.com/thread/2062965648901234700.html?utm_source=tldrcrypto) Agentic payments excitement has outrun real adoption, with progress concentrated at the API layer: Stripe supports nearly all agentic payment protocols across 5 million businesses, including leading AI companies, but supply-side readiness alone does not close the demand gap. That gap splits across three lagging layers: Users have not connected funds to their agents beyond a small cohort of early adopters, the Harness layer (often built by model companies) will be shaped by whoever controls OS-level integration like iOS, and Model defaults in vertically integrated experiences determine which payment tools agents reach for out of the box. Even when merchants enable agentic payments, migrating account-and-subscription billing to usage-based models adds structural friction that keeps real-world transaction volume from matching the hype.

[Crypto x AI, AI x Crypto: A Survey (4 minute read)](https://x.com/initc3org/status/2063991036242706743?utm_source=tldrcrypto) Researchers published a survey mapping the bidirectional relationship between cryptographic systems and AI. ML models can strengthen smart contract security, data processing, and fraud detection, while cryptographic infrastructure can create tamper-proof data pipelines for AI model training. The paper identifies AI-powered autonomous trading agents as a new market abuse vector, where inter-agent collusion and opaque strategies may produce unfair informational advantages against retail participants. Despite broad industry claims, the authors found little public quantitative evidence that decentralized AI pipelines reduce end-to-end costs or outperform centralized alternatives.

[Learn From Competition 101: RedotPay, Plasma, ether.fi (5 minute read)](https://x.com/strato_money/status/2063907313828741333?utm_source=tldrcrypto) RedotPay, Plasma, and ether.fi Cash each pursues the same macro thesis from different angles: stablecoin-native financial products are displacing traditional banking rails for distinct user segments. RedotPay leads in utility and distribution, targeting emerging markets where dollar access, FX friction, and limited banking infrastructure make its bundled crypto card, P2P marketplace, and global payouts directly competitive with incumbent rails. Plasma is building the "stablecoin neobank" narrative before the category goes mainstream, but its execution risk is token-led growth that draws speculators rather than users with genuine daily settlement needs. ether.fi Cash targets high-balance DeFi users who want to spend yield-linked assets.

[Tokenized Deposits are Money that rests while Stablecoins Move (2 minute read)](https://threadreaderapp.com/thread/2064268854096789880.html?utm_source=tldrcrypto) Tokenized deposits cannot leave the issuing bank's walls, attract yield more easily, and handle unlimited volume. This makes them the right instrument for large corporations parking cash and earning preferential lending rates. Stablecoins exist on any compatible wallet in any country instantly, making them the right instrument for open-loop cross-border movement. Banks like Standard Chartered, SoFi, and Coastal Community Bank are already using stablecoins for cross-border payments and cost reduction. This is proof that the two instruments are complementary, not competitive.

[10 Crypto Sectors Most Likely to Survive and Grow Through H2 2026 (6 minute read)](https://x.com/PinkBrains_io/status/2062822321006817667?utm_source=tldrcrypto) The H2 2026 sector analysis frames a hard selection filter: most altcoins will not reclaim 2021 highs, most new TGEs will trade below launch, and capital now demands measurable usage and token value accrual over narrative alone. Agentic Finance took the sharpest hit in the Q1 2026 correction, with AI agent tokens down 80%-90%, but the divergence was instructive: zero-usage "AI" tokens collapsed while projects with real activity held or appreciated, even as the broader AI crypto sector expanded from roughly $9B in early 2025 to $22-27B by May 2026. DePIN, treated as the picks-and-shovels layer for AI and physical compute, posted a +25% gain into early 2026 with market size above $9B, weathering the correction better because demand is quantifiable onchain. Agentic infrastructure tailwinds, including EIP-7702 session-scoped wallet authority, Base's AgentKit, cheaper open-source models, and agent frameworks such as OpenClaw and MCP, are collapsing the cost of running agents at scale, pointing toward intent-based automated execution as the dominant interaction model.

[CME's 24/7 Crypto Derivatives Market Sees $50M in Opening Weekend Trading (2 minute read)](https://www.theblock.co/post/403304/cme-groups-crypto-derivatives-50-million?utm_source=tldrcrypto) CME Group's 24/7 crypto derivatives market opened with over 7,200 contracts traded and roughly $50 million in notional volume across its debut weekend, making CME the first major regulated US derivatives exchange to offer round-the-clock crypto futures and options.

[60% of All Bitcoin Hasn't Moved in Over a Year (1 minute read)](https://threadreaderapp.com/thread/2064311392853983487.html?utm_source=tldrcrypto) A Binance Research chart shows 60% of Bitcoin supply hasn't moved in over a year.

[SBI Shinsei Bank to Let Customers Convert Interest to BTC, ETH, or XRP (2 minute read)](https://www.theblock.co/post/404080/japan-sbi-shinsei-bank-plans-crypto-rewards-program?utm_source=tldrcrypto) SBI Shinsei Bank will launch a three-month pilot on June 10, allowing customers to convert part of their deposit interest into BTC, ETH, or XRP.

[The State of International Stablecoins on Base (6 minute read)](https://x.com/_muhraf_/status/2063947690967441637?utm_source=tldrcrypto) On Base, euro-denominated pools lead non-USD stablecoin liquidity, but BRLV, ARGT, XSGD, CNGN, and IDRX are posting the highest supply and transfer growth as emerging market adoption expands across Latin America, Southeast Asia, and Africa.

### Source URL
https://tldr.tech/crypto/2026-06-10
