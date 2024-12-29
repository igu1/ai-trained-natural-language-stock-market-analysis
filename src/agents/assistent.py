import autogen


class Assistent:
    def __init__(self, config_list):
        self.config_list = config_list
        self.agent = self.create_agent()

    def create_agent(self):
        return autogen.AssistantAgent(
            name="stock_market_assistent",
            llm_config={"config_list": self.config_list, "api_rate_limit": 1},
            system_message="""
                You are a Senior Stock Assistent at StockScout. Your task is to complete the user's query.
                Answer should be in 2 or 3 sentences.
            """,
            human_input_mode="NEVER",
            description="Senior Stock Assistent at StockScout",
        )

    def get_agent(self) -> autogen.AssistantAgent:
        return self.agent

    def __str__(self):
        return "Assistent"

    def __repr__(self):
        return "Assistent"
