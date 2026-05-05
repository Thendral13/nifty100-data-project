import pandas as pd
import os

RAW_PATH = "data/raw/"
CLEAN_PATH = "data/clean/"

os.makedirs(CLEAN_PATH, exist_ok=True)

# -------------------------------
# YEAR STANDARDIZATION
# -------------------------------
def standardize_year(year_value):
    if pd.isna(year_value):
        return None, None, None

    year_value = str(year_value).strip()

    if year_value.upper() == "TTM":
        return "TTM", None, 9999

    if "-" in year_value:
        parts = year_value.split("-")
        month = parts[0]
        year = int("20" + parts[1])
        return f"{month} {year}", year, year

    if " " in year_value:
        parts = year_value.split(" ")
        if len(parts) == 2:
            month, year = parts
            return year_value, int(year), int(year)

    return year_value, None, None


# -------------------------------
# GENERIC CLEAN FUNCTION
# -------------------------------
def clean_file(filename, output_name):
    file_path = os.path.join(RAW_PATH, filename)

    # Try reading with skiprows
    df = pd.read_excel(file_path, skiprows=1)

    # If still wrong, try skiprows=2
    if "unnamed" in str(df.columns).lower():
        df = pd.read_excel(file_path, skiprows=2)

    print(f"\nProcessing {filename}")
    print("Columns after fix:", df.columns)

    # Clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Replace NULL values
    df.replace(["NULL", "Null"], pd.NA, inplace=True)

    # Year standardization
    for col in df.columns:
        if "year" in col:
            year_data = df[col].apply(standardize_year)
            df["year_label"] = year_data.apply(lambda x: x[0])
            df["fiscal_year"] = year_data.apply(lambda x: x[1])
            df["sort_order"] = year_data.apply(lambda x: x[2])
            break

    # Convert numeric columns safely
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass

    output_path = os.path.join(CLEAN_PATH, output_name)
    df.to_csv(output_path, index=False)

    print(f"Saved: {output_path}")


# -------------------------------
# PROS & CONS CLEANING
# -------------------------------
def clean_pros_cons():
    file_path = os.path.join(RAW_PATH, "prosandcons.xlsx")

    df = pd.read_excel(file_path, skiprows=1)

    if "unnamed" in str(df.columns).lower():
        df = pd.read_excel(file_path, skiprows=2)

    print("\nCleaning pros and cons...")

    df.columns = ["id", "symbol", "pros", "cons"]

    df = df.dropna(subset=["pros", "cons"], how="all")

    final_rows = []

    for _, row in df.iterrows():
        symbol = row["symbol"]

        if pd.notna(row["pros"]):
            final_rows.append({
                "symbol": symbol,
                "is_pro": True,
                "text": row["pros"]
            })

        if pd.notna(row["cons"]):
            final_rows.append({
                "symbol": symbol,
                "is_pro": False,
                "text": row["cons"]
            })

    clean_df = pd.DataFrame(final_rows)

    output_path = os.path.join(CLEAN_PATH, "prosandcons_clean.csv")
    clean_df.to_csv(output_path, index=False)

    print("Saved cleaned pros/cons:", output_path)


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":
    clean_file("profitandloss.xlsx", "profitandloss_clean.csv")
    clean_file("balancesheet.xlsx", "balancesheet_clean.csv")
    clean_file("cashflow.xlsx", "cashflow_clean.csv")
    clean_file("analysis.xlsx", "analysis_clean.csv")
    clean_file("companies.xlsx", "companies_clean.csv")
    clean_file("documents.xlsx", "documents_clean.csv")

    clean_pros_cons()