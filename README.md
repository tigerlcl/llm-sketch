# Topic: LLM-powered Tabular Data Imputation

## Objectives:
- Construct imputation pipeline
- Support logical-based imputation
- Support formula-based imputation

## Repo Structure:
- main.py
- configs
  - private.yaml
  - llm_config.yaml
- dataset_loader:
  - chunk_data.py: prepare test sample and store at local
  - dirty_manipulator.py: add noise to data with fixed error rate, report of generated imputation task
- utils
  - llm_chat.py: for chat completion, parse output
  - table_serializer.py: for data serialization
- rule_manager
  - cot_generator.py: for COT 
  - sketch_generator.py: for sketch
  - verification.py: verify the rule
  - cache.py: cache and save the rule for possible re-use
  - summarization.py: summarize the rule
- prompt_templates (should specify the output format)
  - cot.json
  - sketch_logical.json
  - sketch_formula.json
- eval
  - metric.py 
- output
  - clean_report.json
  - cleaned_table.csv

