from autogen import ConversableAgent
from autogen.coding import LocalCommandLineCodeExecutor


class CodeAgent:
    def __init__(self, agent_dir, agent_cfg, llm_cfg):
        code_writer_system_message = """
        You have been given coding capability to solve tabular data imputation using Python code only.
    
        Don't include multiple code blocks in one response. 
        The user can't modify your code. So do not suggest incomplete code which requires users to modify.  
        The user cannot provide any feedback or perform any action beyond executing the code you suggest. 
        
        Check the execution result returned by the user.
        If the result indicates there is an error, fix the error and output_0418 the code again. 
        Suggest the full code instead of partial code or code changes.
        """

        self.code_writer_agent = ConversableAgent(
            "code_writer",
            system_message=code_writer_system_message,
            llm_config=llm_cfg[agent_cfg['llm']],
            code_execution_config=False,  # Turn off code execution for this agent.
            max_consecutive_auto_reply=1,  # Limit the number of consecutive auto-replies.
            human_input_mode="NEVER",
        )

        # Create a local command line code executor.
        self.executor = LocalCommandLineCodeExecutor(
            timeout=agent_cfg['timeout'],  # Timeout for each code execution in seconds.
            work_dir=agent_dir  # fixed csv saved here
        )

        # Create an agent with code executor configuration.
        self.code_executor_agent = ConversableAgent(
            "code_executor",
            llm_config=False,  # Turn off LLM for this agent.
            code_execution_config={"executor": self.executor},  # Use the local command line code executor.
            human_input_mode="NEVER",  # Autonomous
        )

    def agent_chat(self, csv_fp, data, sketch_message):
        # Generate a reply for the given code.
        chat_result = self.code_executor_agent.initiate_chat(
            self.code_writer_agent,
            message=
            f"""Here is the requirement:
            Initialize a Pandas DataFrame object according to the input data. 
            Implement the fixing plan and update the missing value.
            You must save the dataframe as CSV file by 'pd.to_csv(path_or_buf={csv_fp}, index=False)' function
            
            
            Here is the input data:\n{data}
            
            Here is the fixing plan:\n{sketch_message}
            """,
        )

        # post-process chat_result
        history_json = chat_result.chat_history
        cost = chat_result.cost['usage_including_cached_inference']

        # reset the code executor agent
        self.code_executor_agent.reset()

        return history_json, cost
