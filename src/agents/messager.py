import autogen


class Messager:
    def __init__(self, config_list):
        self.config_list = config_list
        self.agent = self.create_agent()

    def create_agent(self):
        return autogen.AssistantAgent(
            name="stock_market_writer",
            llm_config={"config_list": self.config_list},
            system_message="""You are a Professional Stock Market Message Writer at StockScout. Your task is to write engaging and informative content about {stock_name} based on the analysis provided.
                    Your writing should:
                    1. Be 1 paragraphs long - first paragraph introducing key metrics and data
                    - Be clear and concise
                    - Professional yet accessible
                    - Backed by data and analysis
                    - Well-structured and organized

    
                    Example Output:
                        [Company Name]'s stock has been performing **[adjective]** recently, with a 52-week high of **[$X or "Data not provided"]** and a current price of **[$Y or "Data not provided"]**.
                        The company's market capitalization is **[$Z trillion/billion or "Data not provided"]**,
                        making it one of the **[largest/significant players or "Data not provided"]** in its industry.

                """,
            human_input_mode="NEVER",
            description="Professional Stock Market Messenger at StockScout",
            is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
        )

    def get_agent(self) -> autogen.AssistantAgent:
        return self.agent

    def __str__(self):
        return "Messager"

    def __repr__(self):
        return "Messager"
