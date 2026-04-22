import pandas as pd

def clean_data(file_path, output_path="data/superstore_cleaned.csv"):
    df = pd.read_csv(file_path)

    #remove duplicates
    df = df.drop_duplicates()

    # handle missing values
    df['Profit'] = df['Profit'].fillna(df['Profit'].median())
    df['Region'] = df['Region'].fillna("Unknown")

    # fix date formats
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], errors='coerce')

    # drop rows where Order Date couldn't be parsed
    df = df.dropna(subset=['Order Date'])

    # standardize categories 
    df['Category'] = df['Category'].astype(str).str.lower().str.strip()

    df['Category'] = df['Category'].replace({
        'tech': 'technology',
        'furn': 'furniture'
    })

    # create new features 
    df['Month'] = df['Order Date'].dt.month
    df['Year'] = df['Order Date'].dt.year

    # safe profit margin
    df['Profit Margin'] = df['Profit'] / df['Sales']
    df['Profit Margin'] = df['Profit Margin'].replace([float('inf'), -float('inf')], 0)
    df['Profit Margin'] = df['Profit Margin'].fillna(0)

    # save cleaned file
    df.to_csv(output_path, index=False)

    print(f"Cleaned data saved to: {output_path}")
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    return df


if __name__ == "__main__":
    clean_data("data/superstore_messy.csv")