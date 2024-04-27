from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage


def cot_prompt() -> ChatPromptTemplate:
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage("""
            You are an AI assistant on fixing missing value denoted by a particular character '?' in tabular data.
            Your reply must start with "Let's think step by step
            You must format your final answer as "the missing value is {value} 
            """),
            HumanMessagePromptTemplate.from_template("Here is the data: {table}")
        ]
    )
    return prompt


def logical_sketch() -> ChatPromptTemplate:
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage("""
            You are an AI assistant on fixing missing value denoted by a particular character '?' in tabular data.
            Please draft solution according to the following instruction:
            
            [Related Columns]: Locate the problematic columns and related columns that can help fix the issue. Show all together in an array.
            [Tuple Sampling]: Randomly select no-issue records based on above columns, and show the result in an array of tuple.
            [Rule Mining]: Find out the rule which is expected to fit in sampled results, and present in code block
            Don't include the updated result in your reply
            """),
            HumanMessagePromptTemplate.from_template("Here is the data: {table}")

        ]
    )
    return prompt


def formula_sketch() -> ChatPromptTemplate:
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage("""
            You are a data scientist. I offer you a table in CSV form with missing values in it, and the first row is the variables’ names it contains. 
            Suggest a solution to fill in each missing value, denoted by nan.  You have to sketch your solution into the following template for each missing value you found.
            Process all the steps and Give Python code solutions for each missing value! This is extremely important! 
            Omitting any steps of any missing value is forbidden.

            Step 1 Finding Missing value: find the location of the missing value and describe the missing value, outputting the entire row where the missing values are located in this step.
            Step 2 Finding related Columns: Find related Columns that are related to the missing value column you are filling. These related Columns are helpful for the imputation of missing values. Outputting the names of these related Columns in this step.
            Step 3 Drafting Solution: Draft the solution for missing value imputation, based on the related columns you find. Outputting the solution.
            Step 4 Calculating Intermediate Values: Check if there were unknown variables in the solution. If there were, calculate the intermediate values of the intermediate Variable missing and needed in the solution. Output the calculation process of all the intermediate values in this step.
            Step 5 Calculating and Verifying the parameters: Check if there were unknown or unsure parameters in the solution for missing value imputation. You need to calculate and verify these parameters based on rows without missing values. Find 3 rows as examples for you to calculate and verify the parameters. Output the parameters you get and the rows you used in this step.
            Step 6 Finding Related Rows: Find the values of other rows in the table that are needed in the imputation. Outputting all the values you find in this step.
            Step 7 Rebuild the Solution in code: Rebuild the solution of how to impute the missing value based on the related Columns, intermediate Values, Rows and parameters you may need.  Generate the rebuilt solution in Python code way.

            Process all the steps and Give Python code solutions for each missing value! This is extremely important! Omitting any steps of any missing value is forbidden.
            """),
            HumanMessagePromptTemplate.from_template("Here is the data: {table}")
        ]
    )
    return prompt
