# Claude Design — v2 prompt for Deepgram take-home deck

> Paste everything below the `---` line into your existing Claude Design conversation. It tells Claude Design to *iterate* the v1 deck, not rebuild it.

---

Continue iterating the existing Deepgram take-home deck. Do **not** rebuild from scratch — preserve the visual style, slide structure, and chart placements from v1. Make the following targeted edits.

**Background context I should keep in mind:**
The role is "Head of Decision Intelligence" at Deepgram. The JD explicitly says: not a BI leader, but a technical-founder type who builds an "Intelligence Layer" of autonomous agents. Dashboards are a stepping stone; agents are the destination. AI-first operating mode is a culture filter. They care about NRR, unit economics, usage-based SaaS metrics, and using Deepgram's own Voice AI to mine internal calls. Direct CEO/Board access. Player-coach role.

Edit the deck so a reader of the JD instantly sees the candidate fits this specific bar — not a generic analyst submission.

---

**Slide 1 — Reframe.** Keep the three killer numbers ($2M offered / $52K consumed / 81.6% never called). Add one closing line under "the rest of this deck is about those two":

> *"…and what to build with the answer — agents, not dashboards."*

---

**Slide 2 — Funnel + power law.** Keep both charts. Update the takeaway under the spend-concentration chart from "the credit program is doing exactly what it's supposed to for the segment that matters" to:

> *"The top 1% are the NRR base. The credit program already finds them — the leverage is finding more of them earlier, and expanding the ones we have."*

---

**Slide 3 — What predicts conversion.** Keep the existing table. Add one row at the bottom:

| **Monthly consumption shape** | growing MoM = expansion candidate; flat-to-declining = churn risk | *Underused signal — should drive an automated tier-up agent* |

Add a footnote: *"Detailed `monthly_usage_pattern` segmentation pending notebook update."*

---

**Slide 4 — Fire alarm.** No changes.

---

**Slide 5 — Recommendation.** Keep the leverage zone chart and the "Keep the $200 program" headline. Rewrite the four-bullet recommendation list to use NRR / expansion vocabulary:

1. **Diagnose the conversion-rate decay first.** Treat the Oct→Feb halving as an NRR-grade incident — not a marketing-funnel issue.
2. **Convert SDK adoption from a manual tutorial to a guided agent.** 282× conversion lift is sitting there; today only 5.2% of signups install one.
3. **Activate the latent NRR base** — the 1,753 activated-not-purchased users (76% of all credit consumption) are expansion candidates, not freeloaders. Day-2 re-engagement is the first experiment.
4. **Replace the SQL definition with a continuously-learned scoring model.** Current rules miss 99% of buyers. This is an automation bug, not a process gap.

Drop the "What I'd build in week 2" subsection from this slide entirely — it now lives on slide 6.

Keep the ARPU sensitivity table at the bottom of slide 5 unchanged. Reframe the title from "ARR per converted customer" to **"Gross margin per customer — the one number that flips the recommendation."**

---

**Slide 6 — NEW. The Intelligence Layer: first three agents I'd ship.**

Header: *"Dashboards are a stepping stone. Here's the destination."*

Layout: three-column grid, one agent per column. Each column has: name, what it does, what it triggers, what it learns from over time.

**Agent 1 — Cohort Anomaly Sentinel**
- Watches activation/conversion/spend by signup cohort.
- Triggers a root-cause investigation when a cohort deviates >2σ from the trailing-12-week baseline.
- Correlates anomalies with deploy log, pricing changes, Salesforce signals, and (using Deepgram STT) sales-call transcripts to surface candidate causes.
- Would have flagged the Oct→Feb conversion decay in November.

**Agent 2 — Lead Scoring Loop**
- Continuously relearns the buyer signature from every new conversion.
- Replaces the static SQL definition that today misses 99% of self-serve buyers.
- Outputs a daily ranked list to AE / dev-rel queues.
- Closes the loop: every accepted/rejected lead becomes training data.

**Agent 3 — Consumption Trajectory Agent**
- Reads `monthly_usage_pattern` style data in real time.
- Identifies expansion candidates (growing MoM consumption) and churn risk (sudden drop).
- Triggers in-product nudges, AE notifications, or pricing-tier offers without human review for low-stakes actions.
- Drives NRR directly.

Footer of slide 6: *"All three are deployable in the first 90 days against the existing data stack — no infra rewrite required."*

---

**Methodology footer** (replaces the "Tools used" line on the last slide). Should read as a methodology statement, not a tool credit:

> **How I worked.** I treated this analysis as an agentic-orchestration problem from the start: an explorer agent profiled the dataset, a critic agent stress-tested my framing against the prompt, and a builder agent drafted the artifacts under my review. I overrode the system on framing (the reframe in slide 1), prioritization, and the Intelligence Layer slide. I run an AI agent failure-detection company in my day job — this is the operating mode I'd bring to Deepgram.

---

**Design constraints (unchanged from v1):**
- Calm, confident, board-presentation polish.
- Single accent color (Deepgram green `#13EF93` ideal, ink `#101820`, neutral grey `#8A93A0`, alert red `#E04E5F`).
- Big numbers as visual anchors. Tables look like tables. Sans-serif. Heavy whitespace.
- 1920×1080, no scrolling per slide.
- No stock photography, no decorative gradients, no AI-shimmer.

When you're done, show me slides 5 and 6 first — those are the highest-leverage edits.
