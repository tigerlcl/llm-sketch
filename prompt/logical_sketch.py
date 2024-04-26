from prompt.base import LLMChat
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.prompts import HumanMessagePromptTemplate


class LogicalSketch(LLMChat):
    def build_prompt(self):
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=("""
            You are an AI assistant on fixing missing value denoted by a particular character '?' in tabular data.
            
            The first row represents the header row. Please draft solution according to the following instruction
            [Related Columns]: Locate the problematic columns and related columns that can help fix the issue. Show all together in an array.
            [Tuple Sampling]: Randomly select no-issue records based on above columns, and show the result in an array of tuple.
            [Rule Mining]: Find out the rule which is expected to fit in sampled results, and present in code block
            
            Don't include the updated result in your response
            """)),
                HumanMessagePromptTemplate.from_template("Here is the data: {table}")
            ]
        )

        return prompt
