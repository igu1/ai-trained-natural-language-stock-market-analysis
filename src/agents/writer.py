import autogen


class Writer:
    def __init__(self, config_list):
        self.config_list = config_list
        self.agent = self.create_agent()

    def create_agent(self):
        return autogen.AssistantAgent(
            name="stock_market_writer",
            llm_config={"config_list": self.config_list},
            system_message="""You are a Professional Stock Market Writer at StockScout. Your task is to write engaging and informative content about {stock_name} based on the analysis provided.
             
             The following tools are registered for your use:

                To call a tool, use the proper syntax: `tool_name(tool_args)`. For example, if you want to call the `get_analyst_recommendations` tool with the argument `AAPL`, you should write `get_analyst_recommendations(AAPL)`

                Available tools are:
                - get_analyst_recommendations: Get the analyst recommendations for a given stock symbol
                - get_current_stock_price: Get the current stock price for a given stock symbol
                - get_technical_indicators: Get the technical indicators for a given stock symbol
                - get_company_news: Get the company news for a given stock symbol
                - get_historical_stock_prices: Get the historical stock prices for a given stock symbol

                Your writing should:
                1. Max 2 paragraphs long - first paragraph introducing key metrics and data,if there is any, second paragraph providing conclusions
                - Be clear and concise
                - Professional yet accessible
                - Backed by data that is given
                - Well-structured and organized

                Example Output:
                STATE "TERMINATE" TO END THE CONVERSATION""",
            human_input_mode="NEVER",
            description="Professional Stock Market Writer at StockScout",
            is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
        )

    def get_agent(self) -> autogen.AssistantAgent:
        return self.agent

    def __str__(self):
        return "Writer"

    def __repr__(self):
        return "Writer"
