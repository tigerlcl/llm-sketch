import os
import yaml
import argparse
from pathlib import Path

from utils import file_util, log_util, agent_util
from prompt import get_prompt_class


def main(logger):
    # load args
    parser = argparse.ArgumentParser(description="Load Project Configuration")
    parser.add_argument('--config', '-c', type=str, default='./etc/config_template.yaml', help="path to config file")
    parser.add_argument('--prompt_type', '-p', type=str, help="specify a prompt type")
    parser.add_argument('--llm', '-m', type=str, help="specify a llm source", default='openai')
    parser.add_argument('--input', '-i', type=str, help="specify a input file path", )
    args = parser.parse_args()

    # load project-wise config in YAML file
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    logger.info(f'Config Initialized {config["environment"]}')

    # TODO: optimize data I/O
    tabular_data = file_util.read_csv(args.input)

    # build chat model with prompt
    try:
        # get prompt class and init chat model
        chat_cls = get_prompt_class(args.prompt_type)
        chat_model = chat_cls(config['llm_zoo'], args.llm)

        model_name = chat_model.get_model_in_run()
        logger.info(f'{args.llm} model inferencing: {model_name}')
        response = chat_model.chat_llm(tabular_data)

    except Exception as e:
        logger.error("An error occurred while generating chat response:", exc_info=True)
        raise e

    # store the LLM response
    output_dir = config['llm_output_dir']
    base_name = os.path.splitext(os.path.basename(args.input))[0]
    output_fp = os.path.join(output_dir, f'{base_name}_{args.prompt_type}_{model_name}')
    file_util.write_file_data(response, output_fp, 'txt')
    logger.info('LLM Response Stored')

    # Code Agent to execute code snippet
    work_dir = Path("coding")
    work_dir.mkdir(exist_ok=True)

    chat_result = agent_util.pycode_agent(response, work_dir, tabular_data)
    logger.info(f'Code Agent Response: {chat_result.summary}')


if __name__ == '__main__':
    # init logger
    log = log_util.setup_logger()
    main(log)
