from prompt.base import LLMChat
from langchain.prompts import PromptTemplate


class LogicalSketch(LLMChat):
    def build_prompt(self):
        prompt = PromptTemplate.from_template(
            template="""
            You will act as a helpful assistant on fixing missing value issue on tabular data. You will be given a dirty table in CSV format, where the missing value is denoted by a particular character '?'. There could be more than one missing value in a dirty table. The first row represents the header row. 
            Please sketch your solution according to the following instruction for each issue you found

            [Related Columns]: Locate the problematic columns and related columns that can help fix the issue. Show all together in an array.
            [Tuple Sampling]: Randomly select several no-issue records based on above columns, and show the result in an array of tuple.
            [Rule Mining]: Find out the rule which is expected to fit in sampled results, and show the rule in Python code style. 
            
            Here is the data:
            {table}
            """
        )

        return prompt

