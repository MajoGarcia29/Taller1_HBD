import os
import shutil
import time
import io

import pandas as pd
import matplotlib
matplotlib.use("Agg")           
import matplotlib.lines as mlines


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1 – Advanced Filesystem & Format Diagnostics
# ─────────────────────────────────────────────────────────────────────────────

def get_absolute_path(filepath: str) -> str:
    return os.path.abspath(filepath)


def check_permissions(filepath: str) -> dict:
    return {
        "readable": os.access(filepath, os.R_OK),
        "writable": os.access(filepath, os.W_OK),
    }


def get_disk_usage(filepath: str) -> dict:
    usage = shutil.disk_usage(filepath)
    return {
        "total_bytes": usage.total,
        "used_bytes":  usage.used,
        "free_bytes":  usage.free,
    }


def bytes_to_human(size_bytes: int) -> str:
    KB = 1_024
    MB = 1_024 ** 2
    GB = 1_024 ** 3

    if size_bytes >= GB:
        return f"{size_bytes / GB:.2f} GB"
    elif size_bytes >= MB:
        return f"{size_bytes / MB:.2f} MB"
    else:
        return f"{size_bytes / KB:.2f} KB"


def report_filesystem(filepath: str) -> None:
    abs_path    = get_absolute_path(filepath)
    permissions = check_permissions(filepath)
    disk        = get_disk_usage(filepath)

    print("=" * 60)
    print("SECTION 1 – Filesystem & Format Diagnostics")
    print("=" * 60)
    print(f"  Absolute path : {abs_path}")
    print(f"  Readable      : {permissions['readable']}")
    print(f"  Writable      : {permissions['writable']}")
    print()
    print("  Disk partition usage:")
    print(f"    Total : {bytes_to_human(disk['total_bytes'])}")
    print(f"    Used  : {bytes_to_human(disk['used_bytes'])}")
    print(f"    Free  : {bytes_to_human(disk['free_bytes'])}")
    print()


