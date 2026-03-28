# Big Data Tools – Workshop 1

**Universidad de la Sabana · M.Sc. Program in Applied Analytics**  
**Professor:** Hugo Franco, Ph.D. · **March 2026**
**Axel Bedoya**
**María José García**
**Sara Nicol Zuluaga**

---

## Overview

This repository contains the solution for Workshop 1, which covers five core data engineering competencies using Python and PostgreSQL:

1. Filesystem & format diagnostics
2. Data exploration and cleansing
3. Performance benchmarking (iterrows vs apply vs vectorization)
4. PostgreSQL integration via bulk COPY
5. Biomechanical joint-angle visualization

---

## Repository Structure

```
.
├── main.py              # Orchestration script – runs all 5 sections in order
├── bdt_utils.py         # Support library – one report_*() function per section
├── Workshop1_Report.docx
└── README.md
```

---

## Requirements

- Python 3.11+
- PostgreSQL container running on `localhost:5433` (database `bigdatatools1`, user `psqluser`)

Install dependencies:

```bash
pip install pandas psycopg2-binary matplotlib
```

---

## Configuration

Open `main.py` and adjust the two constants at the top:

```python
DATA_FILE = "kinematics_data.csv"   # path to your CSV file

QUERY_PARAMS = {
    "subject_id": "S01",
    "date":       "2024-01-15",
    "trial":      1,
    "protocol":   "walking",
}
```

If your PostgreSQL password differs from the default, update `DB_CONFIG` inside `bdt_utils.py`:

```python
DB_CONFIG = {
    "host":     "localhost",
    "port":     5433,
    "dbname":   "bigdatatools1",
    "user":     "psqluser",
    "password": "your_password_here",
}
```

---

## Usage

```bash
python main.py
```

The script will print a labelled output block for each section and save `joint_angles.png` in the working directory.

---

## Section Summary

| # | Section | Key functions |
|---|---------|--------------|
| 1 | Filesystem diagnostics | `get_absolute_path`, `check_permissions`, `get_disk_usage`, `bytes_to_human` |
| 2 | Data cleansing | `validate_dtypes`, `missing_value_report`, `drop_missing_values` |
| 3 | Performance benchmark | `time_iterrows`, `time_apply`, `time_vectorized` |
| 4 | Database integration | `create_table`, `load_dataframe`, `query_for_visualization` |
| 5 | Visualization | `plot_joint_angles` |

---

## Output

- **Console** – diagnostic tables and timing comparisons printed for every section.
- **`joint_angles.png`** – three stacked subplots (Hip / Knee / Ankle) with Left side in red and Right side in blue.
