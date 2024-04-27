import os
import yaml
import argparse

from utils import file_io, logger
from llm.chat import SketchLLM
from llm.agent import CodeAgent


def main(cfg, logger):
    # init sketch llm
    sketchLLM = SketchLLM(cfg['sketch_config'], cfg['llm_config'])

    # init code agent
    codeAgent = CodeAgent(cfg['agent_config'], cfg['llm_config'])

    # Read input data
    for csv_file in os.listdir(cfg['input_dir']):
        input_fp = os.path.join(cfg['input_dir'], csv_file)
        tabular_data = file_io.read_csv(input_fp)

        # keep the same as the input file name
        base_name = os.path.splitext(os.path.basename(input_fp))[0]
        sketch_fname = f'{base_name}_{sketchLLM.model_in_run}_sketch.txt'
        sketch_fp = os.path.join(config['output_dir'], sketch_fname)

        # generate sketch by prompt engineering
        try:
            logger.info(f'model inferencing: {sketchLLM.model_in_run}')
            sketch_result = sketchLLM.chat(tabular_data)
            if isinstance(sketch_result, tuple):  # expect ChatOpenAI response
                sketch_result, sketch_cost = sketch_result
                sketch_cost_fname = f'{base_name}_{sketchLLM.model_in_run}_cost.txt'
                file_io.write_txt_file(sketch_cost, os.path.join(config['output_dir'], sketch_cost_fname))
                logger.info(f'Sketch cost: {sketch_cost}')

            # store the LLM response
            file_io.write_txt_file(sketch_result, sketch_fp)
            logger.info('Sketch result saved')

        except Exception as e:
            logger.error("An error occurred while generation sketch:", exc_info=True)
            raise e

        try:
            fixed_csv_fname = f'{base_name}_agent.csv'
            chat_result = codeAgent.agent_chat(fixed_csv_fname, tabular_data, sketch_result)

            # store the agent chat result
            agent_fname = f'{base_name}_agent.json'
            agent_fp = os.path.join(config['output_dir'], agent_fname)
            chat_js = {
                'agent_chat': chat_result.chat_history,
                'agent_cost': chat_result.cost["usage_excluding_cached_inference"],  # see doc
            }
            file_io.write_json_file(chat_js, agent_fp)
            logger.info(f'Agent result saved: {chat_result.cost["usage_excluding_cached_inference"]}')

        except Exception as e:
            logger.error("An error occurred while running agent:", exc_info=True)
            raise e

        # validate the agent result


if __name__ == '__main__':
    # init logger
    log = logger.setup_logger()

    # load args
    parser = argparse.ArgumentParser(description="Load Project Configuration")
    parser.add_argument('--config', '-c', type=str, default='./etc/config_template.yaml', help="path to config file")
    args = parser.parse_args()

    # load project-wise config in YAML file
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    log.info(f'Config Initialized {config["experiment_name"]}')

    # check input dir
    if os.path.isdir(config['input_dir']):
        log.info(f'Input data: {config["input_dir"]}')
    else:
        log.error(f'Input data: {config["input_dir"]} does not exist')
        raise FileNotFoundError

    # check output dir
    file_io.check_directory(config['output_dir'])

    # check agent working dir
    file_io.check_directory(config['agent_config']['work_dir'])

    main(config, log)
