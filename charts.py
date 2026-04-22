import matplotlib.pyplot as plt

def plot_sales_by_region(df, output_path="outputs/sales_by_region.png"):
    sales_by_region = (
        df.groupby("Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(8, 5))
    sales_by_region.plot(kind="bar")
    plt.title("Sales by Region")
    plt.xlabel("Region")
    plt.ylabel("Sales")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return output_path

def plot_profit_by_category(df, output_path="outputs/profit_by_category.png"):
    profit_by_category = (
        df.groupby("Category")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(8, 5))
    profit_by_category.plot(kind="bar")
    plt.title("Profit by Category")
    plt.xlabel("Category")
    plt.ylabel("Profit")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return output_path

def plot_monthly_sales(df, output_path="outputs/monthly_sales.png"):
    monthly_sales = (
        df.groupby(["Year", "Month"])["Sales"]
        .sum()
        .reset_index()
    )

    monthly_sales["Year-Month"] = (
        monthly_sales["Year"].astype(str) + "-" + monthly_sales["Month"].astype(str).str.zfill(2)
    )

    plt.figure(figsize=(12, 5))
    plt.plot(monthly_sales["Year-Month"], monthly_sales["Sales"])
    plt.title("Monthly Sales")
    plt.xlabel("Year-Month")
    plt.ylabel("Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return output_path