from abc import abstractmethod

from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama


class LLMChat:
    def __init__(self, config):
        self.openai_api_key = config['openai']['api_key']
        self.openai_model = config['openai']['model']
        self.openai_max_tokens = config['openai']['max_tokens']

        self.ollama_model = config['ollama']['model']
        self.temperature = 0.2  # default

        self._model_in_use = None

    @abstractmethod
    def build_prompt(self):
        pass

    def get_model_in_use(self):
        return self._model_in_use

    def chat_llm(self, llm, data):
        prompt = self.build_prompt()
        chain = prompt | llm

        return chain.invoke({"table": data})

    def load_llm(self, llm_src):
        if llm_src == 'openai':
            model = self._chat_openai()
        elif llm_src == 'ollama':
            model = self._chat_ollama()
        else:
            raise ValueError(f"Invalid LLM source: {llm_src}")

        return model

    def _chat_openai(self):
        self._model_in_use = self.openai_model
        return ChatOpenAI(
            model=self._model_in_use,
            openai_api_key=self.openai_api_key,
            temperature=self.temperature,
            max_tokens=self.openai_max_tokens
        )

    def _chat_ollama(self):
        self._model_in_use = self.ollama_model
        return ChatOllama(model=self._model_in_use)
