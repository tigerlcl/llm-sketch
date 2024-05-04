from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage


def cot_prompt() -> ChatPromptTemplate:
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage("""
            You are an AI assistant on fixing missing value denoted by a particular character '?' in tabular data.
            Your reply must start with "Let's think step by step 
            """),
            HumanMessagePromptTemplate.from_template("Here is the data: {table}")
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
            [Tuple Sampling]: Randomly select no-issue records based on above columns, and show the result in an array of tuple.
            [Rule Mining]: Find out the rule which is expected to fit in sampled results, and present in code block.
            [Value Normalization]: Check if the returned value from rule strictly aligned with the formats of other values in the same column. If not, add normaliation processing into rule.
            """),
            HumanMessagePromptTemplate.from_template("Here is the data: {table}")
        ]
    )
    return prompt
