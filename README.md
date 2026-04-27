# Deepgram self-serve cohort take-home

**Tuomo Nikulainen** · Head of Decision Intelligence assessment · 2026-04-26

## TL;DR

The VP asked whether the $200 credit program is attracting builders or freeloaders. **The framing is wrong.** Of $2M offered, only $52K (2.6%) was consumed, and 81.6% of signups never made a single API call — there is no meaningful credit-leakage problem.

The actual stories in the data:

1. **Activation cliff.** 8,160 of 10,000 signups never call the API.
2. **Conversion has halved in the last 5 months** (1.16% Oct cohort → 0.45% Feb cohort) while activation stayed flat. Something downstream broke. This is the most urgent finding.
3. **SDK adoption is the killer feature** — 282× conversion lift over no integration. Top 1% of users (47% of all spend, 34% conversion) are 100% SDK or direct API.
4. **Current SQL definition is broken.** 89 of 90 buyers were never SQL'd; 19 of 20 SQLs never bought.

**Recommendation:** keep the $200 program; redirect operational investment to (a) diagnose the conversion decay, (b) convert SDK adoption from a tutorial to a guided agent, (c) activate the 1,753 latent NRR users, (d) replace the SQL definition with a continuously-learned scoring model.

The full deliverable is the deck — see [`Nikulainen-Deepgram-Decision-Intelligence.pdf`](Nikulainen-Deepgram-Decision-Intelligence.pdf) (13 slides). Slide 12 sketches the Intelligence Layer — the first three agents I'd ship in the first 90 days.

## Files

| File | Purpose |
|---|---|
| `Nikulainen-Deepgram-Decision-Intelligence.pdf` | Final 13-slide deck. Read this first. |
| `deck.md` | Markdown source narrative for the deck — useful for diff/version control. |
| `analysis.ipynb` | Reproducible Jupyter notebook with the full analysis (8 sections). |
| `analysis.py` | Same analysis as a runnable Python script. Generates all 5 charts in one command. |
| `build_notebook.py` | Generator that builds `analysis.ipynb` from cell definitions. |
| `claude-design-prompt-v2.md` | The prompt I used to drive the deck design in Claude Design. |
| `charts/` | The 5 hero charts as PNGs, referenced from the deck. |
| `data/deepgram_plg_cohort-analysttakehome.csv` | The provided dataset (copied so the repo is self-contained). |
| `requirements.txt` | Python dependencies. |

## How to run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run the analysis as a script (prints findings, regenerates all 5 charts)
python analysis.py

# Or open the notebook
jupyter lab analysis.ipynb

# Or re-execute the notebook headless
jupyter nbconvert --to notebook --execute --inplace analysis.ipynb
```

Tested on Python 3.13. The notebook runs top-to-bottom from a clean kernel.

## How I worked

I treated this analysis as an **agentic-orchestration problem** from the start: an explorer agent profiled the dataset, a critic agent stress-tested my framing against the prompt, and a builder agent drafted the artifacts under my review. I overrode the system on framing (the reframe in slide 3), prioritization, and the Intelligence Layer slide (12). Tooling: Claude Code (Opus 4.7) for analysis and chart drafting; Claude Design for the visual deck.

I run an AI agent failure-detection company in my day job, so the operating mode in slide 12 isn't theoretical for me — it's how I work, and the system I'd bring to Deepgram.

## Questions I'd ask you next

1. What changed between Oct and Feb — pricing, onboarding, traffic mix?
2. What's the cost-to-serve on the 81.6% who never call the API?
3. Who currently owns the SDK-install moment, and what's their headcount?
4. Is the `voice_agent` 5.8% rate stable, or is the cohort still too small to trust?
5. What's our actual ARR per converted self-serve customer? The recommendation flips from "hold" to "expand the credit budget" somewhere between $2,500 and $5,000 ARR — see the sensitivity table on slide 13.

## What's out of scope

- Statistical significance tests on the conversion-decay finding. Would need a bootstrap or more cohorts.
- LTV / payback-period modeling. The data doesn't support it (no per-customer revenue).
- A/B test design for the recommended interventions. Separate doc on request.
- Cross-tabs between integration method × product (e.g. is `voice_agent + SDK` a leading conversion segment?). Worth doing in week 2.
- Detailed `monthly_usage_pattern` segmentation — flagged on slide 7 as the next notebook update.

## Pre-signup data anomalies (disclosed)

- 11 users have `purchase_date < signup_date`
- 16 users have `sql_date < signup_date`

The spec says this is allowed (returning customers / sales-touched leads / second account creation). I disclose them, exclude from time-to-purchase calculations, and retain elsewhere because excluding them would distort cohort sizes.
