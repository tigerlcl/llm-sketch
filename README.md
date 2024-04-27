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
  - metric.py (to do)
- utils (helper functions)
  - file_io.py: txt, csv, json
  - logger.py
- requirements.txt

## CLI Command
```shell
# configure YAML file correspondingly, execute pipeline
python main.py -c etc/config_private.yaml
```