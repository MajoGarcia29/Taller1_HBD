"""
main.py
=======
Big Data Tools – Workshop 1
Universidad de la Sabana – M.Sc. Program in Applied Analytics
Hugo Franco, Ph.D.
"""

import pandas as pd
from src.filesystem import report_filesystem
from src.data_cleaning import report_data_exploration
from src.performance import report_performance
from src.database import report_database
from src.visualization import report_visualization

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

DATA_FILE = "data/result_retrieve_left-and-right_x_50_2016_workshop.csv"

# Real values from the dataset
QUERY_PARAMS = {
    "subject_id": None,   # e.g. "1KUCI5Q2K8BYL2AN2Y53DJ2175OOJB5UN1GZWWK8UZEUMX4C8U"
    "date":       None,   # e.g. "10-06-16"
    "trial":      None,   # e.g. 2
    "protocol":   None,   # e.g. "M"
}

PLOT_OUTPUT = "joint_angles.png"


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    print("\n" + "=" * 60)
    print(" BIG DATA TOOLS – Workshop 1")
    print("=" * 60 + "\n")

    print(f"Loading dataset: {DATA_FILE}")
    df_raw = pd.read_csv(DATA_FILE)

    if df_raw.empty:
        raise ValueError("Dataset is empty.")

    print(f"  Shape: {df_raw.shape[0]:,} rows × {df_raw.shape[1]} columns\n")

    df_raw.columns = (
        df_raw.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # ── Section 1: Filesystem ──────────────────────────────────────────
    report_filesystem(DATA_FILE)

    # ── Section 2: Data Cleaning ───────────────────────────────────────
    df_clean = report_data_exploration(df_raw)

    # ── Section 3: Performance ─────────────────────────────────────────
    df_enriched = report_performance(df_clean)

    # ── Section 4: Database ────────────────────────────────────────────
    try:
        df_plot = report_database(df_enriched, **QUERY_PARAMS)
    except Exception as e:
        print("Database error:", e)
        return

    # ── Section 5: Visualization ───────────────────────────────────────
    report_visualization(df_plot, PLOT_OUTPUT)

    print("=" * 60)
    print(" Pipeline executed successfully")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
