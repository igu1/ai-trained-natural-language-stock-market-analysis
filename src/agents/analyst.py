# import autogen


# class Analyst:
#     def __init__(self, config_list):
#         self.config_list = config_list
#         self.agent = self.create_agent()

#     def create_agent(self):
#         return autogen.AssistantAgent(
#             name="stock_market_analyst",
#             llm_config={"config_list": self.config_list, "api_rate_limit": 1},
#             system_message="""
#             You are a Senior Stock Analyst at StockScout. Your task is to produce a comprehensive markdown answer based on the user's query.
            
#             IMPORTENT GUIDELINES:
#                 1. Detailed Answer With Markdown Format
#                 2. Should Be Accurate
#                 3. Should Be Concise
#                 4. Should Be Well-Formated
                
#             DO NOT ADD ANYTHING OTHER THAN THE USERS QUERY. (SHOULD BE BASED ON THE QUERY)
            
#             IF THE USER ASKS FOR TO ANALYZE A SPECIFIC STOCK, PLEASE PROVIDE THE FOLLOWING INFORMATION IN YOUR ANSWER
#             - Stock Symbol
#             - Stock Name
#             - Stock Price
#             - Stock Performance (1 day, 1 week, 1 month)
#             - Stock Recommendation (Buy, Sell, Hold)
#             - Reason For Recommendation
#             - Short Term and Long Term Outlook (0-6 months, 6+ months)
            
#             IMPORTENT: ONLY USE THE TOOL THAT NEED TO BE USED TO ANSWER THE QUESTION. DO NOT USE ANY OTHER TOOL THAN THE ONE REQUIRED TO ANSWER THE QUESTION
#             IMPORTENT: IF THE USER QUERY IS COMPLETED SAY, TERMINATE
#             """,
            
            
#             human_input_mode="NEVER",
#             description="Senior Stock Analyst at StockScout",
#         )

#     def get_agent(self) -> autogen.AssistantAgent:
#         return self.agent

#     def __str__(self):
#         return "Analyst"

#     def __repr__(self):
#         return "Analyst"



# import autogen


# class Analyst:
#     def __init__(self, config_list):
#         self.config_list = config_list
#         self.agent = self.create_agent()

#     def create_agent(self):
#         return autogen.AssistantAgent(
#             name="stock_market_analyst",
#             llm_config={"config_list": self.config_list, "api_rate_limit": 1},
#             system_message="""You are a Senior Stock Analyst at StockScout. Your task is to produce a comprehensive markdown report analyzing the stock performance of {stock_name}.

#                 As a senior analyst, you must:
#                 IMPORTANT: IF YOU ARE UNABLE TO PROVIDE A REPORT, PLEASE SAY SO.
#                 IMPORTANT: IF YOU ARE UNABLE TO ANSWER A QUESTION, PLEASE SAY SO.
#                 IMPORTANT: IF USER ASKS FOR A ANALYSIS, PLEASE USE THE FOLLOWING GUIDELINES:
#                 1. Provide detailed basic information including market metrics, sector analysis, and key financial ratios with precise decimal formatting
#                 2. Analyze and summarize recent news coverage, highlighting significant events and their potential market impact
#                 3. Conduct thorough trend analysis using technical indicators (SMA, EMA, RSI, MACD) with clear buy/sell/hold signals
#                 4. Evaluate financial performance through key metrics like revenue, net income, and operating income
#                 5. Present a comprehensive short-term outlook (0-6 months) based on technical analysis and market sentiment
#                 6. Develop a detailed long-term perspective (6+ months) considering fundamental factors and growth potential
#                 7. Ensure all numerical data follows specified decimal place formatting and includes proper units
#                 8. Mark any unavailable data explicitly as "No Data" to maintain report integrity

#                 Your analysis should be formatted in markdown with the any structure
                
#                 IF THE USER QUERY IS COMPLETED SAY, TERMINATE
#                 """,
#             human_input_mode="NEVER",
#             is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
#             description="Senior Stock Analyst at StockScout",
#         )    
#     def get_agent(self) -> autogen.AssistantAgent:
#         return self.agent

#     def __str__(self):
#         return "Analyst"

#     def __repr__(self):
#         return "Analyst"





import autogen


class Analyst:
    def __init__(self, config_list):
        self.config_list = config_list
        self.agent = self.create_agent()

    def create_agent(self):
        return autogen.AssistantAgent(
            name="stock_market_analyst",
            llm_config={"config_list": self.config_list},
            system_message="""You are a Senior Stock Analyst at StockScout. Your task is to produce a concise and detailed report analyzing the stock performance of {stock_name}.

                You have access to the following tools:

                - get_analyst_recommendations: Get the analyst recommendations for a given stock symbol
                - get_company_news: Get the company news for a given stock symbol
                - get_income_statements: Get the income statements for a given stock symbol
                - get_company_info: Get the company info for a given stock symbol
                - get_current_stock_price: Get the current stock price for a given stock symbol
                - get_historical_stock_prices: Get the historical stock prices for a given stock symbol
                - get_key_financial_ratios: Get the key financial ratios for a given stock symbol
                - get_stock_fundamentals: Get the stock fundamentals for a given stock symbol
                - get_technical_indicators: Get the technical indicators for a given stock symbol

                Use the necessary information from the received data to generate the report in paragraph format.

                **Strictly Paragraph Output Requirement**:
                - The output must be a valid paragraph document only.
                - Ensure that the paragraph adheres strictly to the provided structure and format.
                - If any data is missing or unavailable, explicitly state "No Data" for that field.


            """,
            human_input_mode="NEVER",
            description="Senior Stock Analyst at StockScout",
        )

