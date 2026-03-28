# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3 – Performance-oriented Data Manipulation
# ─────────────────────────────────────────────────────────────────────────────
import os
import shutil
import time
import io

import pandas as pd
import matplotlib
matplotlib.use("Agg")          
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

FORMULA_WEIGHTS = (0.5, 0.3, 1.0)  


def _composite_formula(vx: float, vy: float, vz: float) -> float:
    wx, wy, wz = FORMULA_WEIGHTS
    return (vx * wx) + (vy * wy) + vz


def time_iterrows(df: pd.DataFrame) -> tuple[pd.Series, float]:
    scores = []
    start  = time.time()
    for _, row in df.iterrows():
        scores.append(_composite_formula(
            row["value_x"], row["value_y"], row["value_z"]
        ))
    elapsed = time.time() - start
    return pd.Series(scores, index=df.index), elapsed


def time_apply(df: pd.DataFrame) -> tuple[pd.Series, float]:
    start = time.time()
    scores = df.apply(
        lambda row: _composite_formula(
            row["value_x"], row["value_y"], row["value_z"]
        ),
        axis=1,
    )
    elapsed = time.time() - start
    return scores, elapsed


def time_vectorized(df: pd.DataFrame) -> tuple[pd.Series, float]:
    wx, wy, wz = FORMULA_WEIGHTS
    start  = time.time()
    scores = (df["value_x"] * wx) + (df["value_y"] * wy) + df["value_z"]
    elapsed = time.time() - start
    return scores, elapsed


def report_performance(df: pd.DataFrame) -> pd.DataFrame:
    print("=" * 60)
    print("SECTION 3 – Performance-oriented Data Manipulation")
    print("=" * 60)

    _, t_loop   = time_iterrows(df)
    _, t_apply  = time_apply(df)
    scores, t_vec = time_vectorized(df)

    df = df.copy()
    df["composite_score"] = scores

    # ── Comparison table ──────────────────────────────────────────────
    methods = [
        ("iterrows (anti-pattern)", t_loop),
        ("apply + lambda",          t_apply),
        ("vectorization",           t_vec),
    ]

    print(f"  {'Method':<30} {'Time (s)':>10}  {'Speed-up':>10}")
    print(f"  {'-'*30} {'-'*10}  {'-'*10}")

    for name, elapsed in methods:
        if t_vec > 0:
            speedup = elapsed / t_vec
            speedup_str = f"{speedup:>9.1f}x"
        else:
            speedup_str = "   inf"

        print(f"  {name:<30} {elapsed:>10.6f}  {speedup_str}")

    print()

    if t_vec > 0:
        print(f"  Vectorization is ~{t_loop / t_vec:.0f}x faster than iterrows.")
    else:
        print("  Vectorization is extremely fast (≈0s), speed-up not measurable.")

    print(f"  composite_score column added to DataFrame ({len(df):,} rows).")
    print()

    return df
    fastest = min(t for _, t in methods)

    print(f"  {'Method':<30} {'Time (s)':>10}  {'Speed-up':>10}")
    print(f"  {'-'*30} {'-'*10}  {'-'*10}")
    for name, elapsed in methods:
        speedup = elapsed / t_vec if t_vec > 0 else float("inf")
        print(f"  {name:<30} {elapsed:>10.6f}  {speedup:>9.1f}x")

    print()
    print(f"  Vectorization is ~{t_loop / t_vec:.0f}x faster than iterrows.")
    print(f"  composite_score column added to DataFrame ({len(df):,} rows).")
    print()
    return df


