from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama


class LLMChat:
    def __init__(self, config):
        self.openai_api_key = config['openai']['api_key']
        self.openai_model = config['openai']['model']
        self.openai_max_tokens = config['openai']['max_tokens']

        self.ollama_model = config['ollama']['model']
        self.temperature = 0.2  # default

    def build_prompt(self):
        pass

    def load_llm(self, llm_src):
        if llm_src == 'openai':
            model = self.chat_openai()
        elif llm_src == 'ollama':
            model = self.chat_ollama()
        else:
            raise ValueError(f"Invalid LLM source: {llm_src}")

        return model

    def chat_openai(self):
        return ChatOpenAI(
            model=self.openai_model,
            openai_api_key=self.openai_api_key,
            temperature=self.temperature,
            max_tokens=self.openai_max_tokens
        )

    def chat_ollama(self):
        return ChatOllama(model=self.ollama_model)
