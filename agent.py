import os
from data_cleaner import clean_data
from charts import plot_sales_by_region, plot_profit_by_category, plot_monthly_sales
from query_router import detect_intent
from analysis_tools import (
    get_total_sales,
    get_total_profit,
    get_top_products,
    get_profit_by_category,
    get_sales_by_region,
    get_monthly_sales,
    get_average_profit_margin,
    get_dataset_summary,
)


class DataAnalystAgent:
    def __init__(self, raw_file_path, cleaned_file_path="data/superstore_cleaned.csv"):
        os.makedirs("outputs", exist_ok=True)

        print("Cleaning dataset...")
        self.df = clean_data(raw_file_path, cleaned_file_path)
        print("Dataset is ready.\n")

    def answer(self, query):
        intent = detect_intent(query)
        print(f"Detected intent: {intent}")

        if intent == "total_sales":
            return get_total_sales(self.df)

        elif intent == "total_profit":
            return get_total_profit(self.df)

        elif intent == "top_products":
            return get_top_products(self.df)

        elif intent == "profit_by_category":
            result = get_profit_by_category(self.df)
            chart_path = plot_profit_by_category(self.df)
            return f"{result}\n\nChart saved to: {chart_path}"

        elif intent == "sales_by_region":
            result = get_sales_by_region(self.df)
            chart_path = plot_sales_by_region(self.df)
            return f"{result}\n\nChart saved to: {chart_path}"

        elif intent == "monthly_sales":
            result = get_monthly_sales(self.df)
            chart_path = plot_monthly_sales(self.df)
            return f"{result}\n\nChart saved to: {chart_path}"

        elif intent == "average_profit_margin":
            return get_average_profit_margin(self.df)

        elif intent == "dataset_summary":
            return get_dataset_summary(self.df)

        else:
            return (
                "I do not understand that query yet.\n"
                "Try asking in different ways, like:\n"
                "- show me revenue by region\n"
                "- what is total profit\n"
                "- plot monthly sales trend\n"
                "- which category is most profitable"
            )

if __name__ == "__main__":
    agent = DataAnalystAgent("data/superstore_messy.csv")

    print("Automated Data Analyst")
    print("Type 'exit' to quit.\n")

    while True:
        user_query = input("Ask a question: ")

        if user_query.lower().strip() == "exit":
            print("Goodbye.")
            break

        response = agent.answer(user_query)
        print("\n" + response + "\n")