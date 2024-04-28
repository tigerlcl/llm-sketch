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
- llm
  - prompt_template.py: cot, sketch 
  - chat.py: chat with openai, ollama
  - agent.py: code writer & code executor, LLM as backend
- eval
  - metric.py
- utils (helper functions)
  - file_io.py: txt, csv, json
  - logger.py
- preprocessing
  - chunk_table.py
- requirements.txt

## CLI Command
`exp-dir` is to store all tests with related file I/Os
```shell
# preprocess raw tabular data
python preprocessing/chunk_table.py \
--dataset datasets/Flight_Route.csv \
--columns "Source,Destination,Route" \
--exp-dir experiments/s10r7m1 \
--col-slices 10 \
--num-rows 7 \
--num-missing 1

# run pipeline on  experiment directory
 python main.py --config etc/config_private.yaml --exp-dir experiments/output_1

```