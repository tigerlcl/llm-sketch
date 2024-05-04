import re
import json
from tempfile import TemporaryDirectory

from autogen import ConversableAgent, AssistantAgent
from autogen.coding import LocalCommandLineCodeExecutor


class CodeAgent:
    def __init__(self, llm_cfg):
        self.code_writer_system_message = """
        You are a helpful AI Assistant for Python coding
    
        Don't include multiple code blocks in one response. 
        The user can't modify your code. So do not suggest incomplete code which requires users to modify.  
        The user cannot provide any feedback or perform any action beyond executing the code you suggest.  
        Suggest the full code instead of partial code or code changes.
        """

        # Create a temporary directory to store the code files.
        self.temp_dir = TemporaryDirectory()

        # Create a local command line code executor.
        self.executor = LocalCommandLineCodeExecutor(
            timeout=10,  # Timeout for each code execution in seconds.
            work_dir=self.temp_dir.name
        )

        self.code_writer_llm_cfg = {
            "config_list": [
                llm_cfg
            ],
            # No need disk cache
            "cache": None,
            "cache_seed": None,
        }

        self.summary_pattern = r'Code output: ({.*})'

    def agent_chat(self, data, sketch_message):
        code_writer_agent = AssistantAgent(
            "code_writer",
            system_message=self.code_writer_system_message,
            llm_config=self.code_writer_llm_cfg,
            # code_execution_config=False,  # Turn off code execution for this agent.
            max_consecutive_auto_reply=1,
            human_input_mode="NEVER",
        )

        code_executor_agent = ConversableAgent(
            "code_executor",

            llm_config=False,  # Turn off LLM for this agent.
            code_execution_config={"executor": self.executor},  # Use the local command line code executor.
            human_input_mode="NEVER",  # Autonomous
        )

        # Generate a reply.
        chat_result = code_executor_agent.initiate_chat(
            code_writer_agent,
            message=
            f"""Here is the requirement:
            Initialize a Pandas DataFrame object according to the input data. 
            Implement the fixing plan and find the missing value.
            You must print the fixing result in JSON format:
            \u007b"row_index": ..., "column_name": ..., "result": ...\u007b
            
            Here is the input data:\n{data}
            
            Here is the fixing plan:\n{sketch_message}
            """,
            summary_method="last_msg",
        )

        # parse chat_result
        # post-process chat_result
        chat_cost = chat_result.cost['usage_including_cached_inference']
        chat_history = chat_result.chat_history
        if chat_result.summary == "":
            return chat_cost, chat_history, None

        chat_summary = self.parse_chat_summary(chat_result.summary)
        return chat_cost, chat_history, chat_summary

    def parse_chat_summary(self, summary_str):
        # Search for the pattern in the string
        match = re.search(self.summary_pattern, summary_str)
        if match:
            # Extract the JSON object from the matched substring
            json_str = match.group(1)
            json_obj = json.loads(json_str)
            return json_obj
        else:
            return None

