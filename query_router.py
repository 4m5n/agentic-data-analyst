def detect_intent(query):
    query = query.lower().strip()

    if any(phrase in query for phrase in [
        "total sales", "total revenue", "overall sales", "overall revenue"
    ]):
        return "total_sales"

    elif any(phrase in query for phrase in [
        "total profit", "overall profit"
    ]):
        return "total_profit"

    elif any(phrase in query for phrase in [
        "top products", "best products", "highest selling products"
    ]):
        return "top_products"

    elif any(phrase in query for phrase in [
        "profit by category", "most profitable category", "category profit"
    ]):
        return "profit_by_category"

    elif any(phrase in query for phrase in [
        "sales by region",
        "revenue by region",
        "region sales",
        "which region sells the most",
        "which region has the most sales",
        "best region by sales",
        "top region by sales"
    ]):
        return "sales_by_region"

    elif any(phrase in query for phrase in [
        "monthly sales", "monthly revenue", "sales trend", "revenue trend"
    ]):
        return "monthly_sales"

    elif any(phrase in query for phrase in [
        "average profit margin", "profit margin"
    ]):
        return "average_profit_margin"

    elif any(phrase in query for phrase in [
        "summary", "dataset summary", "overview of dataset"
    ]):
        return "dataset_summary"

    return "unknown"