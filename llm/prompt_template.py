from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage


def cot_prompt() -> ChatPromptTemplate:
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage("""
            You are an AI assistant on fixing missing value denoted by a particular character '?' in tabular data.
            Your reply must start with "Let's think step by step 
            """),
            HumanMessagePromptTemplate.from_template("Here is the data: {table}\nPresent the answer in the end and you must format the result in a string: the missing value is ##your answer##, you must wrap the answer with double '#' symbol")
        ]
    )
    return prompt


def sketch_prompt() -> ChatPromptTemplate:
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage("""
            You are an AI assistant on fixing missing value denoted by a particular character '?' in tabular data.
            Please draft solution according to the following instruction:
            
            [Related Columns]: Locate the problematic columns and related columns that can help fix the issue. Show all together in an array.
            [Tuple Sampling]: Randomly select several no-issue records based on above columns, and show the result in an array of tuple.
            [Rule Mining]: Find out the rule that describes the relationship of sampled results. Present it in Python code block. 
            """),
            HumanMessagePromptTemplate.from_template("Here is the data: {table}")
        ]
    )
    return prompt
