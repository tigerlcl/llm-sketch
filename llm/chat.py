from . import prompt_template

from langchain_openai import ChatOpenAI
from langchain_community.callbacks.manager import get_openai_callback
from langchain_core.output_parsers import StrOutputParser


def _build_prompt(prompt_type):
    if prompt_type == 'cot':
        return prompt_template.cot_prompt()
    elif prompt_type == 'sketch':
        return prompt_template.sketch_prompt()
    else:
        raise ValueError(f"Invalid prompt type: {prompt_type}")


def sketch_llm(data, cfg):
    prompt = _build_prompt(cfg['prompt_type'])
    llm = ChatOpenAI(**cfg['openai_config'])
    parser = StrOutputParser()
    chain = prompt | llm | parser

    # track token usage
    with get_openai_callback() as cb:
        result = chain.invoke({"table": data})
        cost_summary = {
            'total_cost': round(cb.total_cost, 5),
            'prompt_tokens': cb.prompt_tokens,
            'completion_tokens': cb.completion_tokens,
            'total_tokens': cb.total_tokens,
        }
        return result, cost_summary
