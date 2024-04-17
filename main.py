import os

import yaml
import argparse
import logging
import logging.config

from utils import file_util
from prompt import get_prompt_class


def main():
    # load args
    parser = argparse.ArgumentParser(description="Load Project Configuration")
    parser.add_argument('--config', '-c', type=str, default='./etc/config_template.yaml', help="path to config file")
    parser.add_argument('--prompt_type', '-p', type=str, help="specify a prompt type")
    parser.add_argument('--llm', '-m', type=str, help="specify a llm source", default='openai')
    parser.add_argument('--input', '-i', type=str, help="specify a input file path",)
    args = parser.parse_args()

    # load project-wise config
    # Load YAML file
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
        logging.config.dictConfig(config['log'])

    # create a logger
    logger = logging.getLogger('run')
    logger.info('Config Initialized')

    # TODO: optimize data I/O
    tabular_data = file_util.read_csv(args.input)

    # build chat model with prompt
    try:
        chat_cls = get_prompt_class(args.prompt_type)
        chat_model = chat_cls(config['llm_zoo'])
        model = chat_model.load_llm(args.llm)
        model_name = chat_model.get_model_in_use()
        logger.info(f'{args.llm} model inferencing: {model_name}')

        response = chat_model.chat_llm(model, tabular_data)
        logger.info(response.response_metadata)
    except Exception as e:
        logger.error("An error occurred while generating chat response:", exc_info=True)
        raise e

    # store the LLM response
    output_dir = config['llm_output_dir']
    base_name = os.path.splitext(os.path.basename(args.input))[0]
    output_fp = os.path.join(output_dir, f'{base_name}_{args.prompt_type}_{model_name}.json')

    json_data = {
      'meta': response.response_metadata,
      'content': response.content
    }
    file_util.write_json_data(json_data, output_fp)
    logger.info('LLM Response Stored')


if __name__ == '__main__':
    main()
