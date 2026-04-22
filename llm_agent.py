import json
import os

from openai import OpenAI
from dotenv import load_dotenv

from data_cleaner import clean_data
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
from charts import (
    plot_sales_by_region,
    plot_profit_by_category,
    plot_monthly_sales,
)

load_dotenv()

class LLMDataAnalystAgent:
    def __init__(self, raw_file_path, cleaned_file_path="data/superstore_cleaned.csv"):
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY is not set in your environment.")

        os.makedirs("outputs", exist_ok=True)

        print("Cleaning dataset...")
        self.df = clean_data(raw_file_path, cleaned_file_path)
        print("Dataset is ready.\n")

        self.client = OpenAI()

        self.tools = [
            {
                "type": "function",
                "name": "get_total_sales",
                "description": "Get total sales or total revenue across the dataset.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                    "additionalProperties": False,
                },
            },
            {
                "type": "function",
                "name": "get_total_profit",
                "description": "Get total profit across the dataset.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                    "additionalProperties": False,
                },
            },
            {
                "type": "function",
                "name": "get_top_products",
                "description": "Get the top 5 products by sales.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                    "additionalProperties": False,
                },
            },
            {
                "type": "function",
                "name": "get_profit_by_category",
                "description": "Get profit by category. Useful for identifying the most or least profitable category.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "make_chart": {
                            "type": "boolean",
                            "description": "Whether to also generate a chart."
                        }
                    },
                    "required": [],
                    "additionalProperties": False,
                },
            },
            {
                "type": "function",
                "name": "get_sales_by_region",
                "description": "Get sales by region. Useful for identifying the best or worst performing region.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "make_chart": {
                            "type": "boolean",
                            "description": "Whether to also generate a chart."
                        }
                    },
                    "required": [],
                    "additionalProperties": False,
                },
            },
            {
                "type": "function",
                "name": "get_monthly_sales",
                "description": "Get monthly sales trend over time.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "make_chart": {
                            "type": "boolean",
                            "description": "Whether to also generate a chart."
                        }
                    },
                    "required": [],
                    "additionalProperties": False,
                },
            },
            {
                "type": "function",
                "name": "get_average_profit_margin",
                "description": "Get the average profit margin across the dataset.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                    "additionalProperties": False,
                },
            },
            {
                "type": "function",
                "name": "get_dataset_summary",
                "description": "Get a high-level summary of the dataset including rows, columns, categories, regions, and date range.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                    "additionalProperties": False,
                },
            },
        ]

    def run_tool(self, tool_name, arguments):
        arguments = arguments or {}

        if tool_name == "get_total_sales":
            return get_total_sales(self.df)

        elif tool_name == "get_total_profit":
            return get_total_profit(self.df)

        elif tool_name == "get_top_products":
            return get_top_products(self.df)

        elif tool_name == "get_profit_by_category":
            result = get_profit_by_category(self.df)
            if arguments.get("make_chart"):
                chart_path = plot_profit_by_category(self.df)
                return f"{result}\n\nChart saved to: {chart_path}"
            return result

        elif tool_name == "get_sales_by_region":
            result = get_sales_by_region(self.df)
            if arguments.get("make_chart"):
                chart_path = plot_sales_by_region(self.df)
                return f"{result}\n\nChart saved to: {chart_path}"
            return result

        elif tool_name == "get_monthly_sales":
            result = get_monthly_sales(self.df)
            if arguments.get("make_chart"):
                chart_path = plot_monthly_sales(self.df)
                return f"{result}\n\nChart saved to: {chart_path}"
            return result

        elif tool_name == "get_average_profit_margin":
            return get_average_profit_margin(self.df)

        elif tool_name == "get_dataset_summary":
            return get_dataset_summary(self.df)

        return f"Unknown tool: {tool_name}"

    def ask(self, user_query, max_steps=5):
        response = self.client.responses.create(
            model="gpt-5.4-mini",
            instructions=(
                "You are an automated business data analyst.\n"
                "You may call tools multiple times if needed.\n"
                "For complex questions, break the problem into steps.\n"
                "Use tool results to reason before answering.\n"
                "Be concise, analytical, and business-focused.\n"
                "Do not ask follow-up questions.\n"
                "Do not offer extra formats such as executive summaries, bullet lists, or next steps.\n"
                "Do not end with offers like 'If you want, I can...'\n"
                "Return only the answer to the user's question.\n"
            ),
            input=user_query,
            tools=self.tools,
        )

        for step in range(max_steps):
            tool_calls = [item for item in response.output if item.type == "function_call"]

            if not tool_calls:
                return response.output_text

            tool_outputs = []
            for call in tool_calls:
                tool_name = call.name
                arguments = json.loads(call.arguments) if call.arguments else {}

                print(f"Tool called: {tool_name} | args: {arguments}")

                result = self.run_tool(tool_name, arguments)

                tool_outputs.append(
                    {
                        "type": "function_call_output",
                        "call_id": call.call_id,
                        "output": result,
                    }
                )

            response = self.client.responses.create(
                model="gpt-5.4-mini",
                instructions=(
                    "Continue the analysis using the tool outputs.\n"
                    "Call another tool if needed.\n"
                    "If you already have enough information, give the final answer.\n"
                    "Be concise and business-focused.\n"
                    "Do not ask follow-up questions.\n"
                    "Do not offer additional formatting options, summaries, bullet lists, or next steps.\n"
                    "Do not end with phrases like 'If you want, I can...'\n"
                    "Return only the final answer.\n"
                    ),
                input=tool_outputs,
                previous_response_id=response.id,
                tools=self.tools,
            )

        return "I reached the maximum reasoning steps before finishing the analysis."

if __name__ == "__main__":
    agent = LLMDataAnalystAgent("data/superstore_messy.csv")

    print("LLM Automated Data Analyst")
    print("Type 'exit' to quit.\n")

    while True:
        user_query = input("Ask a question: ")

        if user_query.lower().strip() == "exit":
            print("Goodbye.")
            break

        try:
            answer = agent.ask(user_query)
            print("\n" + answer + "\n")
        except Exception as e:
            print(f"\nError: {e}\n")