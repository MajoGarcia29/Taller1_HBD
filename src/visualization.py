# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5 – Data Visualization
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

JOINT_ORDER   = ["Hip", "Knee", "Ankle"]
VALUE_COLS    = ["value_x", "value_y", "value_z"]
VALUE_LABELS  = ["Value X", "Value Y", "Value Z"]
VALUE_STYLES  = ["-", "--", ":"]   


def plot_joint_angles(df_plot: pd.DataFrame, output_path: str = "joint_angles.png") -> None:
    SIDE_COLORS = {"L": "red", "R": "blue"}
    SIDE_LABELS = {"L": "Left", "R": "Right"}

    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 15))
    fig.suptitle("Joint Angle Analysis\n(Left = Red · Right = Blue)",
                 fontsize=14, fontweight="bold", y=0.98)

    for ax_idx, joint in enumerate(JOINT_ORDER):
        ax = axes[ax_idx]
        ax.set_title(f"{joint}", fontsize=12, fontweight="bold")
        ax.set_xlabel("Sample index")
        ax.set_ylabel("Angle (deg)")
        ax.grid(True, linestyle="--", alpha=0.4)

        df_joint = df_plot[df_plot["joint"] == joint].reset_index(drop=True)

        for side in ["L", "R"]:
            subset = df_joint[df_joint["side"] == side].reset_index(drop=True)
            if subset.empty:
                continue
            color = SIDE_COLORS[side]
            for col, label, ls in zip(VALUE_COLS, VALUE_LABELS, VALUE_STYLES):
                ax.plot(
                    subset.index,
                    subset[col],
                    color=color,
                    linestyle=ls,
                    linewidth=1.5,
                    label=f"{SIDE_LABELS[side]} – {label}",
                )

        ax.legend(loc="upper right", fontsize=8, ncol=2)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Plot saved to: {output_path}")


def report_visualization(df_plot: pd.DataFrame, output_path: str = "joint_angles.png") -> None:
    print("=" * 60)
    print("SECTION 5 – Data Visualization")
    print("=" * 60)
    plot_joint_angles(df_plot, output_path)
    print()



