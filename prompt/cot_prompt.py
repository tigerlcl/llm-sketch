from prompt.base import LLMChat
from langchain.prompts import PromptTemplate


class COTPrompt(LLMChat):
    def build_prompt(self) -> PromptTemplate:
        prompt = PromptTemplate.from_template(
            template="""
            You will act as a helpful assistant on fixing missing value issue on tabular data. You will be given a dirty table in CSV format, where the missing value is denoted by a particular character '?'. There could be more than one missing value in a dirty table. The first row represents the header row. 
            
            Please start the solution with "Let's think step by step"
            
            Here is the data:
            {table} 
            """
        )

        return prompt
