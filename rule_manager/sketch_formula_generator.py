import json
import requests
from langchain.prompts import PromptTemplate
from langchain.llms import HuggingFaceHub
from langchain.chains import LLMChain
from langchain.prompts import load_prompt
import pandas as pd

class SketchGeneratorFormula:
    def __init__(self, sketch_formula_json_path, dirty_data_path, API_file_path, API_URL, temperature=0.8):
        """
        初始化函数
        :param sketch_formula_json_path: sketch JSON文件的路徑
        :param dirty_data_path: 未清理的數據文件路徑
        :param API_file_path: API文件的路徑
        :param API_URL: API的URL
        :param temperature: 用於生成文本的溫度,控制生成結果的隨機性和可讀性,默认值為0.8
        """
        self.sketch_formula_json_path = sketch_formula_json_path
        self.dirty_data_path = dirty_data_path
        self.API_file_path = API_file_path
        self.API_URL = API_URL
        self.temperature = temperature



    def sketch_generate(self):
        """
        从给定的JSON文件路径加载草图公式,并返回加载的内容。
        
        返回值:
        - self.sketch_formula_prompt: 字典,从指定JSON文件加载的草图公式内容。
        """
        with open(self.sketch_formula_json_path, 'r') as f:
            # 加载指定路径的JSON文件内容到self.sketch_formula_prompt
            self.sketch_formula_prompt = load_prompt(self.sketch_formula_json_path)

        return self.sketch_formula_prompt

    def query_generate(self):

        dirty_data = pd.read_csv(self.dirty_data_path, dtype=str)
        self.formatted_query = self.sketch_formula_prompt.format(data=dirty_data)
        return self.formatted_query

    def answer(self):
            """
            Reads the API configuration, sends a request, receives the response, and saves it as a JSON file.

            Returns:
                dict: The API response saved as a JSON object.
            """
            with open(self.API_file_path, 'r') as f:
                api_config = f.read()

            # Simplified API handling; adjust according to your actual API requirements
            headers = { 
                        "Content-Type": "application/json", 
                        "Authorization": api_config
                        } 

            data = { 
                        "model": "gpt-4", 
                        "messages": [{"role": "user", "content": self.formatted_query}], 
                        "temperature": self.temperature 
                        } 
            self.response = requests.post(self.API_URL, headers=headers, data=json.dumps(data))
            self.response = self.response.json()
            # Save the response as a JSON file (optional)
            answer_file_path = "output_answer_impute_bajaj.json"
            with open(answer_file_path, "w") as f:
                json.dump(self.response, f)

            return self.response
    

if __name__ == "__main__":
    llm = SketchGeneratorFormula(
        sketch_formula_json_path="/hpc2hdd/home/yzhang269/FormulaImputaton/llm-sketch/prompt_templates/sketch_formula.json",
        dirty_data_path="/hpc2hdd/home/yzhang269/FormulaImputaton/llm-sketch/examples/data_test/bajaj_test_gemma.csv",
        API_file_path="/hpc2hdd/home/yzhang269/FormulaImputaton/llm-sketch/examples/API/api_ust_gpt.txt",
        API_URL="https://gpt-api.hkust-gz.edu.cn/v1/chat/completions"
    )
    print(llm.sketch_generate())
    print(llm.query_generate())
    print(llm.answer())