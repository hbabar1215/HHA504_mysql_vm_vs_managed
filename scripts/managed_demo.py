# managed_demo.py — Linear, step-by-step demo for managed MySQL (Azure/GCP/OCI)
# Run this file top-to-bottom OR run it cell-by-cell in VS Code.
# Prereqs:
#   pip install sqlalchemy pymysql pandas python-dotenv
#
# Env vars (populate a local .env):
#   MAN_DB_HOST, MAN_DB_PORT, MAN_DB_USER, MAN_DB_PASS, MAN_DB_NAME

import os, time
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


# --- 0) Load environment ---
load_dotenv("assignment_4/.env")  # reads .env in current working directory

MAN_DB_HOST = os.getenv("MAN_DB_HOST")
MAN_DB_PORT = os.getenv("MAN_DB_PORT", "3306")
MAN_DB_USER = os.getenv("MAN_DB_USER")
MAN_DB_PASS = os.getenv("MAN_DB_PASS")
MAN_DB_NAME = os.getenv("MAN_DB_NAME")

print("[ENV] MAN_DB_HOST:", MAN_DB_HOST)
print("[ENV] MAN_DB_PORT:", MAN_DB_PORT)
print("[ENV] MAN_DB_USER:", MAN_DB_USER)
print("[ENV] MAN_DB_NAME:", MAN_DB_NAME)

# --- 1) Connect to server (no DB) and ensure database exists ---
server_url = f"mysql+pymysql://{MAN_DB_USER}:{MAN_DB_PASS}@{MAN_DB_HOST}:{MAN_DB_PORT}"
print("[STEP 1] Connecting to Managed MySQL (no DB):", server_url.replace(MAN_DB_PASS, "*****"))
t0 = time.time()

# Quick sanity-check for required env vars
required = {
    "MAN_DB_HOST": MAN_DB_HOST,
    "MAN_DB_USER": MAN_DB_USER,
    "MAN_DB_PASS": MAN_DB_PASS,
    "MAN_DB_NAME": MAN_DB_NAME,
}
missing = [k for k, v in required.items() if not v]
if missing:
    print("[ERROR] Missing required environment variables:", ", ".join(missing))
    print("Please create or update assignment_4/.env with MAN_DB_HOST, MAN_DB_USER, MAN_DB_PASS, MAN_DB_NAME")
    raise SystemExit(1)

# Create engine and protect connection with helpful error messages on failure
try:
    engine_server = create_engine(
        server_url,
        pool_pre_ping=True,
        connect_args={"ssl": {"ssl": True, "check_hostname": False, "ca": None}},
    )
    with engine_server.connect() as conn:
        with open("sql/init.sql", "r") as f:
            init_sql = f.read()
        # Execute each SQL command
        for command in init_sql.split(';'):
            if command.strip():  # Skip empty commands
                conn.execute(text(command))
        conn.commit()
        # conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{MAN_DB_NAME}`"))
        # conn.execute(text(f"GRANT ALL PRIVILEGES ON '{MAN_DB_NAME}'.* TO '{MAN_DB_USER}'@'%' WITH GRANT OPTION;"))        
        # conn.commit()
    print(f"[OK] Ensured database `{MAN_DB_NAME}` exists on managed instance.")
except Exception:
    import traceback

    print("[ERROR] Failed to connect to Managed MySQL server.")
    # show masked URL to avoid leaking password
    print("Masked server URL:", server_url.replace(MAN_DB_PASS, "*****"))
    print("Common reasons: incorrect username/password, user not allowed from your client IP, network/firewall rules, or SSL mismatch.")
    print("If this is a cloud managed DB, ensure the DB user is allowed to connect from your client IP (or '%' host), and that the password is correct.")
    print("You can also try connecting with the mysql client or cloud console to verify credentials and allowed hosts.")
    traceback.print_exc()
    raise

# --- 2) Connect to the target database ---
db_url = f"mysql+pymysql://{MAN_DB_USER}:{MAN_DB_PASS}@{MAN_DB_HOST}:{MAN_DB_PORT}/{MAN_DB_NAME}"
engine = create_engine(db_url, connect_args={"ssl": {"ssl": True, "check_hostname": False, "ca": None}})

# --- 3) Create a DataFrame and write to a table ---
table_name = "visits"
df = pd.DataFrame(
    [
        {"patient_id": 10, "visit_date": "2025-10-01", "bp_sys": 117, "bp_dia": 75},
        {"patient_id": 11, "visit_date": "2025-10-02", "bp_sys": 131, "bp_dia": 86},
        {"patient_id": 12, "visit_date": "2025-10-03", "bp_sys": 122, "bp_dia": 80},
        {"patient_id": 13, "visit_date": "2025-10-04", "bp_sys": 111, "bp_dia": 71},
        {"patient_id": 14, "visit_date": "2025-10-05", "bp_sys": 126, "bp_dia": 83},
    ]
)
print("[STEP 3] Writing DataFrame to table:", table_name)
with engine.begin() as conn:
    df.to_sql(table_name, con=conn, if_exists="replace", index=False)
print("[OK] Wrote DataFrame to table.")

# --- 4) Read back a quick check ---
print("[STEP 4] Reading back row count ...")
with engine.connect() as conn:
    count_df = pd.read_sql(f"SELECT COUNT(*) AS n_rows FROM `{table_name}`", con=conn)
print(count_df)

elapsed = time.time() - t0
print(f"[DONE] Managed path completed in {elapsed:.1f}s at {datetime.utcnow().isoformat()}Z")