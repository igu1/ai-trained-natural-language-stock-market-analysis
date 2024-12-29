from autogen import register_function, ConversableAgent
from src.agents.assistent import Assistent
from src.agents.analyst import Analyst
from src.agents.writer import Writer
from src.utils.config_loader import load_config
from src.tools.yfinance import (
    get_analyst_recommendations,
    get_company_info,
    get_company_news,
    get_income_statements,
    get_historical_stock_prices,
    get_key_financial_ratios,
    get_stock_fundamentals,
    get_technical_indicators,
    get_current_stock_price,
    get_ticker_by_name,
)
import os

project_folder = os.path.dirname(__file__)
work_dir = os.path.join(project_folder, "test")

os.makedirs(work_dir, exist_ok=True)

# venv_dir = ".autovenv"
# venv_context = create_virtual_env(venv_dir)


class StockAgentInitializer:
    def __init__(self, config_path: str = "config/GROQ_CONFIG_LIST"):
        llm_config = load_config(config_path)
        self.analyst = Analyst(llm_config).agent
        self.writer = Writer(llm_config).agent
        self.assistent = Assistent(llm_config).agent
        self.user_proxy = ConversableAgent(
            name="User",
            llm_config={"config_list": llm_config},
            is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
            human_input_mode="NEVER",
        )
        self.stock_finder = ConversableAgent(
            name="Stock finder",
            system_message="""
            You read the message and use the tool to find the stock symbol from the message by calling the function 'get_ticker_by_name'.
            For example, if the message is 'I want to know about the stock of Apple', you should call the function with the argument 'Apple' and return the result.
            """,
            llm_config={"config_list": llm_config},
            human_input_mode="NEVER",
        )

        self.register_functions()

    def register_functions(self):

        register_function(
            get_ticker_by_name,
            caller=self.stock_finder,
            executor=self.user_proxy,
            name="get_ticker_by_name",
            description="Get the stock symbol or Ticker for a given company name",
        )

        register_function(
            get_analyst_recommendations,
            caller=self.analyst,
            executor=self.user_proxy,
            name="get_analyst_recommendations",
            description="Get the analyst recommendations for a given stock symbol",
        )

        register_function(
            get_company_news,
            caller=self.analyst,
            executor=self.user_proxy,
            name="get_company_news",
            description="Get the company news for a given stock symbol",
        )

        register_function(
            get_income_statements,
            caller=self.analyst,
            executor=self.user_proxy,
            name="get_income_statements",
            description="Get the income statements for a given stock symbol",
        )

        register_function(
            get_company_info,
            caller=self.analyst,
            executor=self.user_proxy,
            name="get_company_info",
            description="Get the company info for a given stock symbol",
        )

        register_function(
            get_current_stock_price,
            caller=self.analyst,
            executor=self.user_proxy,
            name="get_current_stock_price",
            description="Get the current stock price for a given stock symbol",
        )

        # ? For Analyst
        register_function(
            get_historical_stock_prices,
            caller=self.analyst,
            executor=self.user_proxy,
            name="get_historical_stock_prices",
            description="Get the historical stock prices for a given stock symbol",
        )

        register_function(
            get_key_financial_ratios,
            caller=self.analyst,
            executor=self.user_proxy,
            name="get_key_financial_ratios",
            description="Get the key financial ratios for a given stock symbol",
        )

        register_function(
            get_stock_fundamentals,
            caller=self.analyst,
            executor=self.user_proxy,
            name="get_stock_fundamentals",
            description="Get the stock fundamentals for a given stock symbol",
        )

        register_function(
            get_technical_indicators,
            caller=self.analyst,
            executor=self.user_proxy,
            name="get_technical_indicators",
            description="Get the technical indicators for a given stock symbol",
        )

        # Predictor
        register_function(
            get_analyst_recommendations,
            caller=self.writer,
            executor=self.user_proxy,
            name="get_analyst_recommendations",
            description="Get the analyst recommendations for a given stock symbol",
        )

        register_function(
            get_technical_indicators,
            caller=self.writer,
            executor=self.user_proxy,
            name="get_technical_indicators",
            description="Get the technical indicators for a given stock symbol",
        )

        register_function(
            get_company_news,
            caller=self.writer,
            executor=self.user_proxy,
            name="get_company_news",
            description="Get the company news for a given stock symbol",
        )
        register_function(
            get_historical_stock_prices,
            caller=self.writer,
            executor=self.user_proxy,
            name="get_historical_stock_prices",
            description="Get the historical stock prices for a given stock symbol",
        )
