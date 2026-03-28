# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2 – Data Exploration & Cleansing
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

def validate_dtypes(df: pd.DataFrame) -> None:
    print("  Column data types:")
    for col, dtype in df.dtypes.items():
        flag = " ← numeric stored as text?" if dtype == object else ""
        print(f"    {col:<25} {str(dtype):<15}{flag}")
    print()


def missing_value_report(df: pd.DataFrame) -> pd.DataFrame:
    counts  = df.isnull().sum()
    pct     = (counts / len(df)) * 100
    report  = pd.DataFrame({"missing_count": counts, "missing_pct": pct})
    report  = report[report["missing_count"] > 0].sort_values(
        "missing_pct", ascending=False
    )

    print("  Missing value summary (only columns with nulls shown):")
    if report.empty:
        print("    No missing values found.")
    else:
        print(f"    {'Column':<25} {'Count':>8} {'Percentage':>12}")
        print(f"    {'-'*25} {'-'*8} {'-'*12}")
        for col, row in report.iterrows():
            print(
                f"    {col:<25} {int(row['missing_count']):>8} "
                f"{row['missing_pct']:>11.2f}%"
            )
    print()
    return report


def drop_missing_values(
    df: pd.DataFrame,
    subset: list[str] | None = None
) -> pd.DataFrame:

    if subset is None:
        subset = ["value_x", "value_y", "value_z"]

    original_rows = len(df)
    df_clean      = df.dropna(subset=subset).copy()
    dropped_rows  = original_rows - len(df_clean)

    print(f"  Rows before cleaning : {original_rows:,}")
    print(f"  Rows dropped         : {dropped_rows:,}")
    print(f"  Rows after cleaning  : {len(df_clean):,}")
    print()
    return df_clean


def report_data_exploration(df: pd.DataFrame) -> pd.DataFrame:
    print("=" * 60)
    print("SECTION 2 – Data Exploration & Cleansing")
    print("=" * 60)
    validate_dtypes(df)
    missing_value_report(df)
    df_clean = drop_missing_values(df)
    return df_clean


