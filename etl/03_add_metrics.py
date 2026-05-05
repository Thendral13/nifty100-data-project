import pandas as pd
import os

CLEAN_PATH = "data/clean/"
OUTPUT_PATH = "data/clean/"

# ---------------------------
# PROFIT & LOSS METRICS
# ---------------------------
def add_profit_metrics():
    df = pd.read_csv(os.path.join(CLEAN_PATH, "profitandloss_clean.csv"))

    print("\nAdding profit metrics...")

    # Avoid division errors
    df["net_profit_margin_pct"] = (df["net_profit"] / df["sales"]) * 100
    df["expense_ratio_pct"] = (df["expenses"] / df["sales"]) * 100

    if "operating_profit" in df.columns and "interest" in df.columns:
        df["interest_coverage"] = df["operating_profit"] / df["interest"]

    df.to_csv(os.path.join(OUTPUT_PATH, "profitandloss_final.csv"), index=False)
    print("Saved: profitandloss_final.csv")


# ---------------------------
# BALANCE SHEET METRICS
# ---------------------------
def add_balance_metrics():
    df = pd.read_csv(os.path.join(CLEAN_PATH, "balancesheet_clean.csv"))

    print("\nAdding balance sheet metrics...")

    df["debt_to_equity"] = df["borrowings"] / (df["equity_capital"] + df["reserves"])
    df["equity_ratio"] = (df["equity_capital"] + df["reserves"]) / df["total_assets"]

    df.to_csv(os.path.join(OUTPUT_PATH, "balancesheet_final.csv"), index=False)
    print("Saved: balancesheet_final.csv")


# ---------------------------
# CASHFLOW METRICS
# ---------------------------
def add_cashflow_metrics():
    df = pd.read_csv(os.path.join(CLEAN_PATH, "cashflow_clean.csv"))

    print("\nAdding cashflow metrics...")

    df["free_cash_flow"] = df["operating_activity"] + df["investing_activity"]

    df.to_csv(os.path.join(OUTPUT_PATH, "cashflow_final.csv"), index=False)
    print("Saved: cashflow_final.csv")


# ---------------------------
# RUN ALL
# ---------------------------
if __name__ == "__main__":
    add_profit_metrics()
    add_balance_metrics()
    add_cashflow_metrics()