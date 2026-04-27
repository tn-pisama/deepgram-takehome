# Claude Design — v3 micro-fix prompt (slide 7 only)

> Paste below the `---` into the existing Claude Design conversation. This is a one-slide precision fix — do not touch anything else.

---

One small precision fix on **slide 7 (Predictors of Conversion)** only. Do not modify any other slide.

**The issue.** The `none` integration bar currently shows `0.04%` (n = 8,160). The lift column says `282×`. Anyone who divides `10.4 / 0.04` gets `260`, not `282`. The math doesn't reconcile because `0.04%` is over-rounded — the actual rate is `3 / 8,160 = 0.0368%`.

**The fix.** On the bar chart in slide 7, change the label above the `none` bar from `0.04%` to `0.037%`. Optionally, change the label above `console_only` from `0.40%` to `0.449%` for the same reason (actual is `3 / 668 = 0.449%`). Keep both `n = 8,160` and `n = 668` annotations as they are.

After the fix:
- `none` bar: **`0.037%`** · n = 8,160
- `console_only` bar: **`0.449%`** · n = 668
- `direct_api` bar: **`4.6%`** · n = 654 *(unchanged)*
- `sdk` bar: **`10.4%`** · n = 518 *(unchanged)*

Now the math reconciles: `10.4 / 0.037 = 281` ≈ the `282×` lift in the table. The signal table on the right of the slide stays exactly as it is — `282×` for SDK, `125×` for direct_api, `2.5×` for business email, etc.

Do not touch the title, the table, the footnote, the layout, or any other slide. Just the two bar labels.

When done, re-export the PDF and share the new download link.
