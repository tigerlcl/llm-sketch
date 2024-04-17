# Topic: LLM-powered Tabular Data Imputation

## Objectives:
- Build imputation pipeline
- Support logical-based imputation (Tiger)
- Support formula-based imputation (Sean)

## Repo Structure:
- main.py
- etc
  - config_template.yaml
  - config_private.yaml (for local only)
- utils
  - file_util.py: process I/O
- prompt
  - base.py
  - cot_prompt.py
  - formula_sketch_prompt.py
  - logical_sketch_prompt.py 
- eval
  - metric.py (to do)
- examples
  - data_test/*.csv
  - output/*.json
- app.log

