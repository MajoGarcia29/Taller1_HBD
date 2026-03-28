# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4 – Database Integration & Retrieval
# ─────────────────────────────────────────────────────────────────────────────
"""
src/database.py
===============
Big Data Tools – Workshop 1  |  Section 4
Database Integration & Retrieval
"""

import io
import pandas as pd
import psycopg2

DB_CONFIG = {
    "host":     "localhost",
    "port":     5433,
    "dbname":   "bigdatatools1",
    "user":     "psqluser",
    "password": "psqlpassword",
}

TABLE_NAME = "kinematics_data"


# ─────────────────────────────────────────────────────────────────────────────

def get_connection(config: dict = DB_CONFIG):
    return psycopg2.connect(**config)


def create_table(conn, df: pd.DataFrame, table: str = TABLE_NAME) -> None:
    type_map = {
        "float64": "DOUBLE PRECISION",
        "float32": "DOUBLE PRECISION",
        "int64":   "BIGINT",
        "int32":   "INTEGER",
        "object":  "TEXT",
        "bool":    "BOOLEAN",
    }
    col_defs = [
        f'"{col}" {type_map.get(str(dtype), "TEXT")}'
        for col, dtype in df.dtypes.items()
    ]
    ddl = (
        f"DROP TABLE IF EXISTS {table};\n"
        f"CREATE TABLE {table} (\n  "
        + ",\n  ".join(col_defs)
        + "\n);"
    )
    with conn.cursor() as cur:
        cur.execute(ddl)
    conn.commit()
    print(f"  Table '{table}' created successfully.")


def load_dataframe(conn, df: pd.DataFrame, table: str = TABLE_NAME) -> None:
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    sql = f"COPY {table} FROM STDIN WITH (FORMAT CSV, HEADER)"
    with conn.cursor() as cur:
        cur.copy_expert(sql, buffer)
    conn.commit()
    print(f"  {len(df):,} rows loaded into '{table}' via COPY.")


def detect_query_params(df: pd.DataFrame) -> dict:
 
    filter_cols = ["subject_id", "date", "trial", "protocol"]
    available = (
        df[df["joint"].isin(["Hip", "Knee", "Ankle"])]
        .groupby(filter_cols)["joint"]
        .nunique()
        .reset_index()
        .rename(columns={"joint": "n_joints"})
        .sort_values("n_joints", ascending=False)
    )

    print("  Available filter combinations (top 5):")
    print(f"    {'subject_id':<15} {'date':<12} {'trial':>5} {'protocol':<10} {'joints':>6}")
    print(f"    {'-'*15} {'-'*12} {'-'*5} {'-'*10} {'-'*6}")
    for _, row in available.head(5).iterrows():
        sid = str(row["subject_id"])[:14]  
        print(
            f"    {sid:<15} {str(row['date']):<12} "
            f"{int(row['trial']):>5} {str(row['protocol']):<10} {int(row['n_joints']):>6}"
        )
    print()

    best = available.iloc[0]
    params = {
        "subject_id": best["subject_id"],
        "date":       best["date"],
        "trial":      int(best["trial"]),
        "protocol":   best["protocol"],
    }
    print(f"  Auto-selected: subject={params['subject_id'][:14]}…  "
          f"date={params['date']}  trial={params['trial']}  protocol={params['protocol']}")
    return params


def query_for_visualization(
    conn,
    subject_id,
    date,
    trial,
    protocol,
    table: str = TABLE_NAME,
) -> pd.DataFrame:

    sql = f"""
        SELECT side, joint, value_x, value_y, value_z
        FROM   {table}
        WHERE  subject_id = %(subject_id)s
          AND  date       = %(date)s
          AND  trial      = %(trial)s
          AND  protocol   = %(protocol)s
          AND  joint IN ('Hip', 'Knee', 'Ankle')
        ORDER BY joint, side;
    """
    df_plot = pd.read_sql_query(
        sql, conn,
        params={"subject_id": subject_id, "date": date,
                "trial": trial, "protocol": protocol},
    )
    print(f"  Query returned {len(df_plot):,} rows for visualization.")
    return df_plot


def report_database(
    df: pd.DataFrame,
    subject_id=None,
    date=None,
    trial=None,
    protocol=None,
) -> pd.DataFrame:

    print("=" * 60)
    print("SECTION 4 – Database Integration & Retrieval")
    print("=" * 60)

  
    if any(v is None for v in [subject_id, date, trial, protocol]):
        print("  QUERY_PARAMS not set – auto-detecting from dataset...\n")
        p = detect_query_params(df)
        subject_id, date, trial, protocol = (
            p["subject_id"], p["date"], p["trial"], p["protocol"]
        )

    conn = get_connection()
    try:
        create_table(conn, df)
        load_dataframe(conn, df)
        df_plot = query_for_visualization(conn, subject_id, date, trial, protocol)

       
        if df_plot.empty:
            print("  WARNING: 0 rows returned. Auto-detecting valid params...\n")
            p = detect_query_params(df)
            df_plot = query_for_visualization(
                conn, p["subject_id"], p["date"], p["trial"], p["protocol"]
            )
    finally:
        conn.close()

    print()
    return df_plot