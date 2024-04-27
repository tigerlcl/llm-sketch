from . import prompt_template

from langchain_openai import ChatOpenAI
from langchain_community.callbacks.manager import get_openai_callback
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser


def _build_prompt(prompt_type):
    if prompt_type == 'cot':
        return prompt_template.cot_prompt()
    elif prompt_type == 'logical':
        return prompt_template.logical_sketch()
    elif prompt_type == 'formula':
        return prompt_template.formula_sketch()
    else:
        raise ValueError(f"Invalid prompt type: {prompt_type}")


class SketchLLM:
    def __init__(self, sketch_cfg, llm_cfg):
        # preload cfg
        self.prompt = _build_prompt(sketch_cfg['prompt_type'])
        self.parser = StrOutputParser()

        self.llm_src = sketch_cfg['llm']
        self.llm_args = llm_cfg[self.llm_src]
        self.model_in_run = self.llm_args['model']

    def chat(self, data):
        if self.llm_src == 'openai':
            llm = ChatOpenAI(**self.llm_args)
            chain = self.prompt | llm | self.parser

            # track token usage
            with get_openai_callback() as cb:
                result = chain.invoke({"table": data})
            return result, repr(cb)

        elif self.llm_src == 'ollama':
            llm = ChatOllama(model=self.model_in_run)
            chain = self.prompt | llm | self.parser
            return chain.invoke({"table": data})

        else:
            raise ValueError(f"Invalid LLM source: {self.llm_src}")




