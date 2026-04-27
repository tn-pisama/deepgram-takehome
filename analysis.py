"""
Deepgram self-serve cohort analysis.

Runnable end-to-end. Mirrors the cells in analysis.ipynb.
Loads data/deepgram_plg_cohort-analysttakehome.csv, prints findings, and
saves all five hero charts to charts/.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "deepgram_plg_cohort-analysttakehome.csv"
CHARTS = ROOT / "charts"
CHARTS.mkdir(exist_ok=True)

# --- House style: clean, minimal, board-ready ---
plt.rcParams.update({
    "figure.dpi": 140,
    "savefig.dpi": 160,
    "savefig.bbox": "tight",
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.titleweight": "semibold",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "grid.linestyle": "--",
})

DG_GREEN = "#13EF93"   # Deepgram brand green-ish
DG_INK = "#101820"
DG_GREY = "#8A93A0"
DG_RED = "#E04E5F"


# ============================================================
# 1. Load + data quality audit
# ============================================================

def load() -> pd.DataFrame:
    df = pd.read_csv(DATA)
    for col in ("signup_date", "first_api_call_date", "purchase_date", "sql_date"):
        df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def audit(df: pd.DataFrame) -> None:
    print("=" * 60)
    print("DATA QUALITY AUDIT")
    print("=" * 60)
    print(f"Rows: {len(df):,} | Columns: {len(df.columns)}")
    print(f"Signup window: {df['signup_date'].min().date()} → {df['signup_date'].max().date()}")
    print()
    print("Null counts (key fields):")
    for col in ("first_api_call_date", "primary_product", "products_used",
                "purchase_date", "sql_date"):
        nulls = df[col].isna().sum()
        print(f"  {col:24s} {nulls:>5,} ({nulls/len(df)*100:.1f}%)")
    print()
    pre_purch = ((df["purchase_date"].notna()) & (df["purchase_date"] < df["signup_date"])).sum()
    pre_sql = ((df["sql_date"].notna()) & (df["sql_date"] < df["signup_date"])).sum()
    print(f"ANOMALY — purchase_date before signup_date: {pre_purch} users")
    print(f"ANOMALY — sql_date before signup_date:      {pre_sql} users")
    print("→ Disclosed in deck. Likely returning customers / sales-touched leads.")
    print("→ Excluded from time-to-purchase calc; retained elsewhere.")


# ============================================================
# 2. Activation funnel
# ============================================================

def funnel(df: pd.DataFrame) -> dict:
    n = len(df)
    activated = df["first_api_call_date"].notna().sum()
    spent = (df["total_credit_spend_usd"] > 0).sum()
    purchased = int(df["purchased"].sum())
    became_sql = int(df["became_sql"].sum())

    print("\n" + "=" * 60)
    print("ACTIVATION FUNNEL")
    print("=" * 60)
    rows = [
        ("Signups", n, 100.0),
        ("Made first API call", activated, activated / n * 100),
        ("Spent any credit", spent, spent / n * 100),
        ("Purchased", purchased, purchased / n * 100),
        ("Became SQL", became_sql, became_sql / n * 100),
    ]
    for label, val, pct in rows:
        print(f"  {label:25s} {val:>7,}  ({pct:5.2f}%)")

    burned = df["total_credit_spend_usd"].sum()
    offered = n * 200
    print(f"\nCredits offered: ${offered:,.0f}")
    print(f"Credits burned:  ${burned:,.0f}  ({burned/offered*100:.1f}% burn rate)")

    return {
        "n": n,
        "activated": activated,
        "purchased": purchased,
        "became_sql": became_sql,
        "burned": burned,
        "offered": offered,
    }


def chart_funnel(df: pd.DataFrame) -> None:
    n = len(df)
    activated = df["first_api_call_date"].notna().sum()
    purchased = int(df["purchased"].sum())
    became_sql = int(df["became_sql"].sum())

    stages = ["Signups", "Activated\n(1st API call)", "Purchased", "SQL"]
    values = [n, activated, purchased, became_sql]
    pcts = [v / n * 100 for v in values]

    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    bars = ax.barh(stages[::-1], values[::-1], color=[DG_RED, DG_GREY, DG_GREY, DG_INK])
    for bar, val, pct in zip(bars, values[::-1], pcts[::-1]):
        ax.text(bar.get_width() * 1.02, bar.get_y() + bar.get_height() / 2,
                f"{val:,} ({pct:.1f}%)", va="center", fontsize=10, color=DG_INK)
    ax.set_xscale("log")
    ax.set_xlim(1, n * 2)
    ax.set_xlabel("Users (log scale)")
    ax.set_title("The activation cliff: 81.6% of signups never make a single API call",
                 loc="left")
    ax.grid(axis="y", alpha=0)
    fig.savefig(CHARTS / "01_funnel.png")
    plt.close(fig)


# ============================================================
# 3. Credit spend distribution & power law
# ============================================================

def spend_concentration(df: pd.DataFrame) -> None:
    total = df["total_credit_spend_usd"].sum()
    sorted_spend = df["total_credit_spend_usd"].sort_values(ascending=False)
    n = len(df)

    print("\n" + "=" * 60)
    print("CREDIT SPEND CONCENTRATION (power law)")
    print("=" * 60)
    print(f"Total spend across all users: ${total:,.0f}")
    for pct in (0.01, 0.05, 0.10, 0.25):
        k = int(n * pct)
        share = sorted_spend.head(k).sum() / total * 100
        print(f"  Top {pct*100:>4.1f}% ({k:>4} users): ${sorted_spend.head(k).sum():>8,.0f}  ({share:5.1f}% of all spend)")

    top100 = df.nlargest(100, "total_credit_spend_usd")
    print(f"\nTop 100 spenders — purchase rate: {top100['purchased'].mean()*100:.0f}%")
    print(f"Top 100 spenders — business email: {(top100['email_type']=='business').sum()}/100")
    print(f"Top 100 spenders — SDK or direct_api: {(top100['integration_method'].isin(['sdk','direct_api'])).sum()}/100")
    print(f"Top 100 spenders — mean days_active: {top100['days_active'].mean():.1f}")


def chart_spend_concentration(df: pd.DataFrame) -> None:
    n = len(df)
    total = df["total_credit_spend_usd"].sum()
    sorted_spend = df["total_credit_spend_usd"].sort_values(ascending=False).reset_index(drop=True)
    cum_share = sorted_spend.cumsum() / total * 100
    user_share = (np.arange(1, n + 1) / n) * 100

    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    ax.plot(user_share, cum_share, color=DG_INK, linewidth=2.2)
    ax.fill_between(user_share, 0, cum_share, color=DG_GREEN, alpha=0.18)
    ax.plot([0, 100], [0, 100], color=DG_GREY, linewidth=1, linestyle="--", label="Equal distribution")

    for marker_pct in (1, 5, 10):
        share = cum_share.iloc[int(n * marker_pct / 100) - 1]
        ax.scatter([marker_pct], [share], color=DG_RED, zorder=5, s=40)
        ax.annotate(f"Top {marker_pct}% → {share:.0f}% of spend",
                    xy=(marker_pct, share), xytext=(marker_pct + 6, share - 4),
                    fontsize=10, color=DG_INK)

    ax.set_xlabel("Cumulative % of users (sorted by spend, descending)")
    ax.set_ylabel("Cumulative % of credit spend")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_title("Credit spend is severely power-law: top 1% of users = 47% of all spend",
                 loc="left")
    ax.legend(loc="lower right", frameon=False)
    fig.savefig(CHARTS / "02_spend_concentration.png")
    plt.close(fig)


# ============================================================
# 4. Predictors of conversion
# ============================================================

def predictors(df: pd.DataFrame) -> None:
    print("\n" + "=" * 60)
    print("PREDICTORS OF CONVERSION")
    print("=" * 60)

    print("\nIntegration method:")
    g = df.groupby("integration_method")["purchased"].agg(["sum", "mean", "count"])
    g["lift_vs_none"] = g["mean"] / g.loc["none", "mean"]
    print(g.round(4).to_string())

    print("\nPrimary product:")
    g = df.groupby("primary_product", dropna=False)["purchased"].agg(["sum", "mean", "count"])
    print(g.round(4).to_string())

    print("\nEmail type:")
    g = df.groupby("email_type")["purchased"].agg(["sum", "mean", "count"])
    print(g.round(4).to_string())

    print("\nSpend tier vs purchase rate:")
    df_t = df.copy()
    df_t["spend_tier"] = pd.cut(
        df_t["total_credit_spend_usd"],
        bins=[-0.01, 0, 1, 10, 50, 200, 1000],
        labels=["$0", "$0-1", "$1-10", "$10-50", "$50-200", "$200+"],
    )
    g = df_t.groupby("spend_tier", observed=True)["purchased"].agg(["sum", "mean", "count"])
    print(g.round(3).to_string())


def chart_integration_lift(df: pd.DataFrame) -> None:
    g = df.groupby("integration_method")["purchased"].agg(["sum", "mean", "count"])
    order = ["none", "console_only", "direct_api", "sdk"]
    g = g.reindex(order)
    rates = g["mean"].values * 100
    counts = g["count"].values

    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    colors = [DG_GREY, DG_GREY, DG_INK, DG_GREEN]
    bars = ax.bar(order, rates, color=colors)
    for bar, rate, count in zip(bars, rates, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.25,
                f"{rate:.1f}%\nn={count:,}", ha="center", fontsize=10, color=DG_INK)
    ax.set_ylabel("Purchase rate (%)")
    ax.set_ylim(0, max(rates) * 1.25)
    ax.set_title("SDK adoption is the killer feature: 282× conversion lift over no integration",
                 loc="left")
    ax.grid(axis="x", alpha=0)
    fig.savefig(CHARTS / "03_integration_lift.png")
    plt.close(fig)


# ============================================================
# 5. Cohort analysis — conversion decay
# ============================================================

def cohort_decay(df: pd.DataFrame) -> pd.DataFrame:
    print("\n" + "=" * 60)
    print("MONTHLY COHORT — ACTIVATION & CONVERSION")
    print("=" * 60)
    df = df.copy()
    df["signup_month"] = df["signup_date"].dt.to_period("M")
    mc = df.groupby("signup_month").agg(
        n=("user_id", "count"),
        activated=("first_api_call_date", lambda s: s.notna().sum()),
        purchased=("purchased", "sum"),
    )
    mc["activation_rate"] = (mc["activated"] / mc["n"] * 100).round(2)
    mc["conversion_rate"] = (mc["purchased"] / mc["n"] * 100).round(2)
    print(mc.to_string())
    print("\nNote: late cohorts have less time to convert (right-censoring).")
    print("Even so — Sep cohort had 6 months and converted 1.08%; Feb cohort had 2 months and converted 0.45%.")
    return mc


def chart_conversion_decay(df: pd.DataFrame) -> None:
    df = df.copy()
    df["signup_month"] = df["signup_date"].dt.to_period("M")
    mc = df.groupby("signup_month").agg(
        n=("user_id", "count"),
        activated=("first_api_call_date", lambda s: s.notna().sum()),
        purchased=("purchased", "sum"),
    )
    # Drop the partial March cohort (only 45 signups, 1 day of data)
    mc = mc[mc["n"] > 100]
    mc["activation_rate"] = mc["activated"] / mc["n"] * 100
    mc["conversion_rate"] = mc["purchased"] / mc["n"] * 100
    months = [str(p) for p in mc.index]

    fig, ax1 = plt.subplots(figsize=(8.5, 4.5))
    ax2 = ax1.twinx()
    ax1.plot(months, mc["activation_rate"], color=DG_GREY, marker="o", linewidth=2,
             label="Activation rate")
    ax2.plot(months, mc["conversion_rate"], color=DG_RED, marker="o", linewidth=2.5,
             label="Conversion rate")

    for x, y in zip(months, mc["conversion_rate"]):
        ax2.annotate(f"{y:.2f}%", (x, y), textcoords="offset points", xytext=(0, 10),
                     ha="center", fontsize=10, color=DG_RED)

    ax1.set_ylabel("Activation rate (%)", color=DG_GREY)
    ax2.set_ylabel("Conversion rate (%)", color=DG_RED)
    ax1.set_ylim(0, max(mc["activation_rate"]) * 1.4)
    ax2.set_ylim(0, max(mc["conversion_rate"]) * 1.5)
    ax1.tick_params(axis="y", colors=DG_GREY)
    ax2.tick_params(axis="y", colors=DG_RED)
    ax2.grid(False)
    ax1.set_title("Fire alarm: conversion has halved while activation stayed flat",
                  loc="left")
    fig.savefig(CHARTS / "04_conversion_decay.png")
    plt.close(fig)


# ============================================================
# 6. SQL pipeline disconnect
# ============================================================

def sql_disconnect(df: pd.DataFrame) -> None:
    print("\n" + "=" * 60)
    print("SQL PIPELINE DISCONNECT")
    print("=" * 60)
    sql_and_purch = int((df["became_sql"] & df["purchased"]).sum())
    sql_not_purch = int((df["became_sql"] & ~df["purchased"]).sum())
    purch_not_sql = int((~df["became_sql"] & df["purchased"]).sum())
    total_sql = int(df["became_sql"].sum())
    total_purch = int(df["purchased"].sum())
    print(f"Total SQLs:      {total_sql}")
    print(f"Total purchases: {total_purch}")
    print(f"SQL & purchased:     {sql_and_purch:>3}")
    print(f"SQL not purchased:   {sql_not_purch:>3}  ({sql_not_purch/total_sql*100:.0f}% of SQLs)")
    print(f"Purchased not SQL:   {purch_not_sql:>3}  ({purch_not_sql/total_purch*100:.0f}% of buyers)")
    print("→ Sales is touching the wrong people. Current SQL definition misses 99% of buyers.")


# ============================================================
# 7. Leverage zone — activated but not purchased
# ============================================================

def leverage_zone(df: pd.DataFrame) -> None:
    print("\n" + "=" * 60)
    print("THE LEVERAGE ZONE — activated but didn't buy")
    print("=" * 60)
    activated = df[df["first_api_call_date"].notna()]
    not_purch = activated[~activated["purchased"]]
    print(f"Activated: {len(activated):,}")
    print(f"Of which not purchased: {len(not_purch):,}")
    print(f"Their total credit spend: ${not_purch['total_credit_spend_usd'].sum():,.0f}")
    print(f"Mean days_active: {not_purch['days_active'].mean():.1f}")
    one_and_done = (not_purch["days_active"] == 1).sum()
    print(f"One-and-done (1 active day): {one_and_done:,} ({one_and_done/len(not_purch)*100:.1f}%)")
    print("→ Highest-leverage cohort. They showed intent, hit the API, then disappeared.")


def chart_leverage_zone(df: pd.DataFrame) -> None:
    activated = df[df["first_api_call_date"].notna()].copy()
    activated["bucket"] = pd.cut(
        activated["days_active"],
        bins=[0, 1, 3, 7, 30, 200],
        labels=["1 day", "2-3 days", "4-7 days", "8-30 days", "30+ days"],
    )
    g = activated.groupby("bucket", observed=True).agg(
        n=("user_id", "count"),
        purchased=("purchased", "sum"),
    )
    g["purchase_rate"] = g["purchased"] / g["n"] * 100

    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    bars = ax.bar(g.index.astype(str), g["purchase_rate"],
                  color=[DG_RED, DG_GREY, DG_GREY, DG_INK, DG_GREEN])
    for bar, rate, n in zip(bars, g["purchase_rate"], g["n"]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                f"{rate:.1f}%\nn={n:,}", ha="center", fontsize=10, color=DG_INK)
    ax.set_ylabel("Purchase rate (%)")
    ax.set_xlabel("Days active in first session window")
    ax.set_ylim(0, max(g["purchase_rate"]) * 1.3)
    ax.set_title("The leverage zone: 53% of activators never come back for a second day",
                 loc="left")
    ax.grid(axis="x", alpha=0)
    fig.savefig(CHARTS / "05_leverage_zone.png")
    plt.close(fig)


# ============================================================
# 8. ROI sensitivity
# ============================================================

def roi_sensitivity(df: pd.DataFrame) -> None:
    print("\n" + "=" * 60)
    print("ROI SENSITIVITY — credits burned vs revenue (parametric)")
    print("=" * 60)
    burned = df["total_credit_spend_usd"].sum()
    purchased = int(df["purchased"].sum())
    print(f"Credits burned: ${burned:,.0f}")
    print(f"Purchases:      {purchased}")
    print()
    print(f"{'Assumed ARR/customer':>22s}  {'Total revenue':>15s}  {'ROI multiple':>15s}")
    print("-" * 60)
    for arpu in (500, 2_500, 5_000, 25_000, 50_000):
        rev = purchased * arpu
        roi = rev / burned
        print(f"  ${arpu:>10,}             ${rev:>12,}      {roi:>10.1f}×")
    print("\n→ Even at $500/customer, the program is 0.86× ROI on credit spend (break-even-ish).")
    print("→ At $2,500+ ARR, it's a clear win. ASK THE VP for actual ARPU before recommending changes to the credit amount.")


# ============================================================
# Time to purchase
# ============================================================

def time_to_purchase(df: pd.DataFrame) -> None:
    print("\n" + "=" * 60)
    print("TIME TO PURCHASE (excluding pre-signup anomalies)")
    print("=" * 60)
    purch = df[df["purchased"] & df["purchase_date"].notna()].copy()
    purch_post = purch[purch["purchase_date"] >= purch["signup_date"]]
    ttp = (purch_post["purchase_date"] - purch_post["signup_date"]).dt.days
    print(f"Valid post-signup purchases: {len(purch_post)}")
    print(f"Median: {ttp.median():.0f} days | Mean: {ttp.mean():.1f} | p90: {ttp.quantile(.9):.0f}")
    print(f"Same-day purchases: {(ttp == 0).sum()} ({(ttp == 0).mean()*100:.0f}%)")
    print("→ A fast-path 'install → buy' motion exists. Design the funnel for it.")


def main() -> None:
    df = load()
    audit(df)
    funnel(df)
    spend_concentration(df)
    predictors(df)
    cohort_decay(df)
    sql_disconnect(df)
    leverage_zone(df)
    time_to_purchase(df)
    roi_sensitivity(df)

    chart_funnel(df)
    chart_spend_concentration(df)
    chart_integration_lift(df)
    chart_conversion_decay(df)
    chart_leverage_zone(df)
    print(f"\nAll 5 charts saved to {CHARTS}/")


if __name__ == "__main__":
    main()
