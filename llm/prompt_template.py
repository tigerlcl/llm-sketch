from langchain.prompts import ChatPromptTemplate


def un_prompt() -> ChatPromptTemplate:
    prompt = ChatPromptTemplate.from_template(
            template=("""
            Please help fix missing value. Here is the data: {table}
            
            Present the answer in the end and you must format the result in a string: the missing value is ##your answer##, 
            You must wrap the answer with double '#' symbol
            """)
    )
    return prompt


def cot_prompt() -> ChatPromptTemplate:
    prompt = ChatPromptTemplate.from_template(
            template=("""
            Please help fix missing value. Here is the data: {table}
            You must reply starting with: Let's think step by step
            
            Present the answer in the end and you must format the result in a string: the missing value is ##your answer##, 
            you must wrap the answer with double '#' symbol
            """)
    )
    return prompt


def sketch_prompt() -> ChatPromptTemplate:
    prompt = ChatPromptTemplate.from_template(
            template=("""
            Please help fix missing value. Here is the data: {table}
            You must draft solution according to the following instruction:
            [Issue targeting]: Scan through the data and identify the missing value issue.
            [Columns Filtering]: Locate column where the issue occurred and other columns that can help fix the issue.
            [Entry Sampling]: Randomly select several no-issue entries based on the filtered columns.
            [Rule Mining]: Learn from the above samples. The rule can be constrained calculation, conditional logic, or in freeform.
            Make sure the result must align with the same pattern of field value where the issue occurred.
            [Rule Formulation]: Formulate the rule as a function code block and use it to impute missing value.
            """)
    )
    return prompt
