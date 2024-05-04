# Topic: LLM-powered Tabular Data Imputation

## Keywords:
Data Preprocessing, Large Language Models, Tabular Data, Data Imputation

## Objectives:
This project is to impute missing values in tabular data using LLM. We acknowledge that the data cleaning takes up a lot of time in a data science project 
and LLM can be a good solution attributed to its ability to in-contextual learning and prompt engineering. Therefore, we will explore the LLM as a tool for tabular data cleanup.
To begin with, we will focus on the missing value imputation task, which is a common issue among tables. Meanwhile, this project served as a project for my course 5002, Spring 24 @HKUST-GZ.


## Repo Structure:
- main.py
- etc
  - config_template.yaml
  - config_private.yaml (for local only)
- llm
  - prompt_template.py: cot, sketch 
  - chat.py: chat with openai models
  - agent.py: code writer & code executor, LLM as backend
- utils (helper functions)
  - file_io.py: txt, csv, json
  - logger.py
- preprocessing
  - chunk_table.py
- demo: experiment details for demonstration
  - slice-data: raw data
  - input-data: the noise added data as the input
  - agent: agent chat history
  - sketch: the prompt-based sketched fixing plan for solving the problem
  - run.log: the log of the experiment
  - slice_report.json: the report indicates where the missing values are located
  - fix_report.json: the report indicates the imputation result
- requirements.txt

## CLI Command
`exp-dir` is to store all tests with related file I/Os on sketch, agent result and imputation evaluation

`dataset` is downloaded from Kaggle for demonstration purposes. Here is the [link](https://www.kaggle.com/datasets/jillanisofttech/flight-price-prediction-dataset).

`columns` indicates the column fields where the missing values are took from the raw data.

`prompt-type` decides the prompting strategy. currently, we support `sketch` and `cot`.

```shell
# preprocess raw tabular data to mimic the missing value problem
python preprocessing/chunk_table.py \
--dataset datasets/Flight_Route.csv \
--columns "Route,Total_Stops" \
--exp-dir demo_sketch \
--num-slices 20 \
--num-rows 6

# run imputation pipeline on experiment directory
 python main.py \
 --config etc/config_private.yaml \
 --prompt-type sketch \
 --exp-dir demo_sketch
```

> Note: the `etc/config_private.yaml` is for local use only. You should configure some fields like `openai_config`. After the experiment is done, 
> you can find report and log files in the experiment directory. Make a copy before running the next experiment if using the same data slices.
> Default setting will override the previous experiment output.

## Related Resources
- [OpenAI](https://platform.openai.com/) for backend serving LLM.
- [LangChain-Model I/O](https://python.langchain.com/docs/modules/model_io/) by LangChain. It is a powerful framework for LLM-based applications.
- [AutoGen](https://github.com/microsoft/autogen) by Microsoft. It is a programming framework for agentic AI. We use it to convert sketch to code and execute it.