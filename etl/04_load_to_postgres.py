import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:Urmine%40251124@localhost:5000/nifty100_dw")

files = {
    "fact_profit_loss": "data/clean/profitandloss_clean.csv",
    "fact_balance_sheet": "data/clean/balancesheet_clean.csv",
    "fact_cash_flow": "data/clean/cashflow_clean.csv",
    "dim_companies": "data/clean/companies_clean.csv",
    "dim_analysis": "data/clean/analysis_clean.csv",
    "dim_documents": "data/clean/documents_clean.csv",
    "dim_pros_cons": "data/clean/prosandcons_clean.csv"
}

for table, path in files.items():
    try:
        df = pd.read_csv(path)
        df.to_sql(table, engine, if_exists="replace", index=False)
        print(f"✅ Loaded {table}")
    except Exception as e:
        print(f"❌ Failed {table}:", e)