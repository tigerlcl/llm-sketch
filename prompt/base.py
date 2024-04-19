from abc import abstractmethod
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser


class LLMChat:
    def __init__(self, config, llm_src):
        self.ctx_token = config['common']['ctx_token']
        self.temperature = config['common']['temperature']

        self.openai_api_key = config['openai']['api_key']
        self.openai_model = config['openai']['model']
        self.ollama_model = config['ollama']['model']

        # preload llm
        self.llm_src = llm_src
        self.llm, self._model_name_in_run = self._load_llm_in_run()

        self.parser = StrOutputParser()

    @abstractmethod
    def build_prompt(self):
        pass

    def get_model_in_run(self):
        return self._model_name_in_run

    def _load_llm_in_run(self):
        if self.llm_src == 'openai':
            return ChatOpenAI(
                model=self.openai_model,
                openai_api_key=self.openai_api_key,
                temperature=self.temperature,
                max_tokens=self.ctx_token
            ), self.openai_model

        elif self.llm_src == 'ollama':
            return ChatOllama(
                model=self.ollama_model,
                temperature=self.temperature,
            ), self.ollama_model

        else:
            raise ValueError(f"Invalid LLM source: {self.llm_src}")

    def chat_llm(self, data):
        chain = self.build_prompt() | self.llm | self.parser
        return chain.invoke({"table": data})
