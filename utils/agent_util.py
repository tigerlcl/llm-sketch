from autogen import ConversableAgent
from autogen.coding import LocalCommandLineCodeExecutor

local_llm_config = {
    "config_list": [
        # {
        #     "model": "NotRequired",  # Loaded with LiteLLM command
        #     "api_key": "NotRequired",  # Not needed
        #     "base_url": "http://0.0.0.0:4000"  # Your LiteLLM URL
        # },
        {"model": "gpt-4-turbo",
         "api_key": "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"
        }
    ],
    "temperature": 0,
}


def pycode_agent(sketch_message, work_dir, data):
    code_writer_system_message = """
    You have been given coding capability to solve tabular data imputation using Python code only.

    Don't include multiple code blocks in one response. 
    The user can't modify your code. So do not suggest incomplete code which requires users to modify.  
    The user cannot provide any feedback or perform any action beyond executing the code you suggest. 
    Check the execution result returned by the user. If the result indicates there is an error, fix the error and output the code again. 
    Suggest the full code instead of partial code or code changes.
    
    """

    code_writer_agent = ConversableAgent(
        "code_writer",
        system_message=code_writer_system_message,
        llm_config=local_llm_config,
        code_execution_config=False,  # Turn off code execution for this agent.
        max_consecutive_auto_reply=2,  # Limit the number of consecutive auto-replies.
        human_input_mode="NEVER",
    )

    # Create a local command line code executor.
    executor = LocalCommandLineCodeExecutor(
        timeout=10,  # Timeout for each code execution in seconds.
        work_dir=work_dir.name,  # Use the temporary directory to store the code files.
    )

    # Create an agent with code executor configuration.
    code_executor_agent = ConversableAgent(
        "code_executor",
        llm_config=False,  # Turn off LLM for this agent.
        code_execution_config={"executor": executor},  # Use the local command line code executor.
        human_input_mode="NEVER",  # Autonomous
    )

    csv_output = "test_003.csv"

    # Generate a reply for the given code.
    chat_result = code_executor_agent.initiate_chat(
        code_writer_agent,
        message=
        f"""Here is the requirement: 
        Initialize a Pandas DataFrame object according to the input data. 
        Implement the fixing plan and update the missing value.
        Save the dataframe as CSV file by 'pd.to_csv' function, file_name={csv_output}  and set index=False.
        
        Here is the input data:\n{data}\nHere is the fixing plan:\n{sketch_message}
        """,
    )

    return chat_result
