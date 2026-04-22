def get_total_sales(df):
    total_sales = df["Sales"].sum()
    return f"Total sales: ${total_sales:,.2f}"


def get_total_profit(df):
    total_profit = df["Profit"].sum()
    return f"Total profit: ${total_profit:,.2f}"


def get_top_products(df):
    result = (
        df.groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )
    return f"Top 5 products by sales:\n{result.to_string()}"


def get_profit_by_category(df):
    result = (
        df.groupby("Category")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )
    return f"Profit by category:\n{result.to_string()}"


def get_sales_by_region(df):
    result = (
        df.groupby("Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )
    return f"Sales by region:\n{result.to_string()}"


def get_monthly_sales(df):
    result = (
        df.groupby(["Year", "Month"])["Sales"]
        .sum()
        .sort_index()
    )
    return f"Monthly sales:\n{result.to_string()}"


def get_average_profit_margin(df):
    avg_margin = df["Profit Margin"].mean()
    return f"Average profit margin: {avg_margin:.2%}"


def get_dataset_summary(df):
    rows, cols = df.shape
    return (
        f"Dataset summary:\n"
        f"Rows: {rows}\n"
        f"Columns: {cols}\n"
        f"Categories: {df['Category'].nunique()}\n"
        f"Regions: {df['Region'].nunique()}\n"
        f"Date range: {df['Order Date'].min().date()} to {df['Order Date'].max().date()}"
    )