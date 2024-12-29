from src.main import StockAgentInitializer
from autogen import GroupChat
from autogen import GroupChatManager
import json

class Agent:
    def __init__(self, config_list):
        self.config_list = config_list
        self.initializer = StockAgentInitializer()
        self.stock_finder = self.initializer.stock_finder
        self.analyst = self.initializer.analyst
        self.writer = self.initializer.writer
        self.assistent = self.initializer.assistent
        self.user_proxy = self.initializer.user_proxy

    def start(self, message):
        try:
            allowed_transitions = {
                self.user_proxy: [self.stock_finder],
                self.stock_finder: [self.analyst, self.writer, self.assistent],
                self.analyst: [self.writer],
                self.writer: [self.assistent, self.analyst],
            }

            group_chat = GroupChat(
                agents=[self.user_proxy, self.stock_finder, self.analyst, self.writer],
                messages=[],
                allowed_or_disallowed_speaker_transitions=allowed_transitions,
                speaker_transitions_type="allowed",
                send_introductions=True,
            )

            group_chat_manager = GroupChatManager(
                groupchat=group_chat,
                llm_config={"config_list": self.config_list},
            )

            chat_result = self.user_proxy.initiate_chat(
                group_chat_manager,
                message=message,
                summary_method="reflection_with_llm",
            )
            print('--------------------------------------------------------------')
            print(group_chat.messages)
            print('--------------------------------------------------------------')
            return chat_result.summary['content']

        except Exception as e:
            # Return an error message in case of exceptions
            return {"error": f"An error occurred: {str(e)}"}