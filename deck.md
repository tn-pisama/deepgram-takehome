# Deepgram self-serve cohort — what the data is actually telling us

**Tuomo Nikulainen** · Head of Decision Intelligence · candidate · 2026-04-26

> The presentable artifact is [`Nikulainen-Deepgram-Decision-Intelligence.pdf`](Nikulainen-Deepgram-Decision-Intelligence.pdf) (13 slides). This markdown is the source narrative.

---

## Slide 01 — Title

**What the data is actually telling us.**
Self-serve cohort · take-home analysis · 26 April 2026

---

## Slide 02 — The data, in three numbers

**There is no credit-leakage problem. You couldn't give the credits away if you tried.**

| | | |
|---|---|---|
| Credits offered | **$2.0M** | 10,000 signups × $200 |
| Credits consumed | **$52.1K** | 2.6% burn rate |
| Signups with zero API calls | **81.6%** | 8,160 of 10,000 |

*Source: self-serve cohort dataset · 6-month window ending 2026-02*

---

## Slide 03 — The question is wrong

> *"Are we attracting builders or freeloaders, and where is the credit spend going?"*

**The two questions worth asking:**

1. **Why do four in five signups never touch the product?** *(The activation cliff.)*
2. **Why has conversion halved in five months while activation stayed flat?** *(The fire alarm.)*

*The rest of this deck is about those two — and what to build with the answer.* **Agents, not dashboards.**

---

## Slide 04 — Where the cohort actually goes

**10,000 signups → 1,840 activations → 90 buyers → 20 SQLs.**
The cliff sits at "signup → first API call."

(Funnel chart, log scale — `charts/01_funnel.png`)

---

## Slide 05 — Where the spend goes

**Top 1% of users consume 47% of all credits — and convert at 34%.**

*The 1% that matters:* 100 users · 47% of spend · 34% conversion · 100% on SDK or direct API.

The top 1% are the NRR base. The credit program already finds them — the leverage is finding more of them *earlier*, and expanding the ones we have.

**Don't kill it. Compound it.**

(Lorenz curve — `charts/02_spend_concentration.png`)

---

## Slide 06 — Section divider

**What predicts conversion — and what doesn't.**
SDK adoption, voice_agent, business email, the broken SQL flag.

---

## Slide 07 — Predictors of conversion

**SDK adoption is the highest-leverage lever.**

| Signal | Conversion lift | Verdict |
|---|---:|---|
| **SDK adoption** | **282×** | Killer feature |
| Direct API integration | 125× | Strong |
| Business email domain | 2.5× | Real but small |

**Signal quality — what we're not yet using**

| | | |
|---|---|---|
| Current SQL flag | misses 99% of buyers | Definition is broken |
| `monthly_usage_pattern` | not yet segmented | Underused — tier-up agent |
| `voice_agent` product | 5.8% conv. rate | Smallest cohort, hottest segment |

Today only 5.2% of signups (518 / 10,000) ever install an SDK. Detailed `monthly_usage_pattern` segmentation pending notebook update.

(Bar chart — `charts/03_integration_lift.png`)

---

## Slide 08 — The fire alarm

**Conversion has halved since October. Activation hasn't moved.**

| Cohort | Activation | Conversion |
|---|---:|---:|
| 2025-09 | 17.9% | 1.08% |
| 2025-10 | 18.4% | 1.16% |
| 2025-11 | 19.2% | 1.02% |
| 2025-12 | 20.6% | 0.97% |
| 2026-01 | 17.4% | 0.72% |
| **2026-02** | **16.7%** | **0.45%** |

(Dual-axis line chart — `charts/04_conversion_decay.png`)

---

## Slide 09 — Three hypotheses, the data alone can't pick

**Something downstream of activation broke between October and February.**

| Hypothesis 01 | Hypothesis 02 | Hypothesis 03 |
|---|---|---|
| **Pricing or paywall friction landed in Q1 2026.** Check release notes and the experiment log. Did a paywall, plan change, or rate-limit ship? | **Onboarding regression broke the first-session "wow."** Same activation rate, fewer purchases — the gap is between first call and first dollar. Look at SDK quickstart and dashboard CTAs. | **Competitive pressure compressed the consideration window.** OpenAI Realtime, ElevenLabs, Cartesia all moved during this window. Activated users may now be comparison-shopping. |

**Caveat handled:** Sep had 6 months and converted 1.08%; Feb had 2 months and is at 0.45%. Median time-to-purchase is 4 days, so most Feb conversion has already happened. The drop is real, not censoring.

**Next move:** pull product release notes + experiment log; run an exit survey on the activated-not-converted Jan/Feb cohort.

---

## Slide 10 — The leverage zone

**53% of activators never come back for a second day. The ones who do convert at 27%.**

| One day · then gone | 30+ days active |
|---:|---:|
| **0.3%** purchase rate | **27.1%** purchase rate |
| 934 users · they proved intent and disappeared | 48 users · 90× the conversion rate per active day |

**The leverage zone:** day-2 re-engagement is the obvious experiment. They came once. Bring them back.

(Bar chart — `charts/05_leverage_zone.png`)

---

## Slide 11 — Recommendation

**Keep the $200 credit program. Redirect operational investment, in this order.**

1. **Diagnose the conversion-rate decay first.** Treat the Oct→Feb halving as an NRR-grade incident — not a marketing-funnel issue.
2. **Convert SDK adoption from a manual tutorial to a guided agent.** 282× conversion lift is sitting there; today only 5.2% of signups install one.
3. **Activate the latent NRR base.** The 1,753 activated-not-purchased users (76% of all credit consumption) are expansion candidates, not freeloaders. Day-2 re-engagement is the first experiment.
4. **Replace the SQL definition with a continuously-learned scoring model.** Current rules miss 99% of buyers. This is an automation bug, not a process gap.

**One bet beyond the four:** double down on `voice_agent` — highest conversion rate, smallest cohort, hottest market segment.

---

## Slide 12 — The Intelligence Layer

**Dashboards are a stepping stone. Here's the destination — first three agents I'd ship.**

### 01 · Cohort Anomaly Sentinel
*Watches activation, conversion, and spend by signup cohort.*
- **Triggers** a root-cause investigation when a cohort deviates >2σ from the trailing-12-week baseline.
- **Correlates** anomalies with deploy log, pricing changes, Salesforce signals, and — using Deepgram STT — sales-call transcripts.
- **Learns** from every confirmed cause; would have flagged the Oct→Feb decay in November.

### 02 · Lead Scoring Loop
*Continuously relearns the buyer signature from every new conversion.*
- **Replaces** the static SQL definition that today misses 99% of self-serve buyers.
- **Outputs** a daily ranked list to AE and dev-rel queues.
- **Closes the loop:** every accepted or rejected lead becomes training data.

### 03 · Consumption Trajectory Agent
*Reads `monthly_usage_pattern`-style data in real time.*
- **Identifies** expansion candidates (growing MoM consumption) and churn risk (sudden drop).
- **Triggers** in-product nudges, AE notifications, and pricing-tier offers — without human review for low-stakes actions.
- **Drives** NRR directly.

**All three are deployable in the first 90 days against the existing data stack — no infra rewrite required.**

---

## Slide 13 — The one number that flips the recommendation

**Gross margin per customer.**

| Assumed ARR | Revenue · 90 buyers | ROI on $52K credits |
|---:|---:|---:|
| $500 | $45K | 0.9× |
| **$2,500** | **$225K** | **4.3×** |
| $5,000 | $450K | 8.6× |
| $25,000 | $2.25M | 43× |

**Where the recommendation flips:** from "hold the credit budget" to "expand it" — the answer sits between $2,500 and $5,000 ARR.

### How I worked
I treated this analysis as an agentic-orchestration problem from the start: an explorer agent profiled the dataset, a critic agent stress-tested my framing against the prompt, and a builder agent drafted the artifacts under my review. I overrode the system on framing (the reframe in slide 03), prioritization, and the Intelligence Layer slide.

**I run an AI agent failure-detection company in my day job — this is the operating mode I'd bring to Deepgram.**

### Questions I'd ask you next
1. What changed between Oct and Feb — pricing, onboarding, traffic mix?
2. What's the cost-to-serve on the 81.6% who never call the API?
3. Who currently owns the SDK-install moment, and what's their headcount?
4. Is the `voice_agent` 5.8% rate stable, or is the cohort still too small to trust?
