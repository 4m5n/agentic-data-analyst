from data_cleaner import clean_data

def main():
    input_file = "data/superstore.csv"
    output_file = "data/superstore_cleaned.csv"

    df = clean_data(input_file)

    # Save cleaned dataset (does NOT overwrite original)
    df.to_csv(output_file, index=False)

    print("\nCleaned Data Preview:")
    print(df.head())

    print("\nData Info:")
    print(df.info())

    print(f"\nCleaned file saved to: {output_file}")

if __name__ == "__main__":
    main()