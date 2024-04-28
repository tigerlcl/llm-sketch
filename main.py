import os
import yaml
import argparse

from llm.chat import SketchLLM
from llm.agent import CodeAgent
from utils import file_io, logger
from eval.metric import compare_csv_files


def main(cfg, log):
    # init sketch llm
    sketchLLM = SketchLLM(cfg['sketch_config'], cfg['llm_config'])

    # init code agent
    codeAgent = CodeAgent(agent_dir, cfg['agent_config'], cfg['llm_config'])

    # Read input data
    for csv_file in os.listdir(cfg['input_dir']):
        input_fp = os.path.join(cfg['input_dir'], csv_file)
        tabular_data = file_io.read_csv(input_fp)
        base_name = os.path.splitext(os.path.basename(input_fp))[0]  # keep the same as the input file name
        log.info(f'test init: {base_name}')

        # generate sketch by prompt engineering
        try:
            sketch_fp = os.path.join(sketch_dir, f'{base_name}_{sketchLLM.model_in_run}.txt')
            sketch_result = sketchLLM.chat(tabular_data)
            if isinstance(sketch_result, tuple):
                # expect LangChain.ChatOpenAI response
                sketch_result, sketch_cost = sketch_result
                log.info(f'Sketch cost: {sketch_cost}')

            # store the LLM response
            file_io.write_txt_file(sketch_result, sketch_fp)
            log.info(f'Sketch result saved: {base_name}')

        except Exception as e:
            log.error(f"sketch {base_name} failed with error {e}", exc_info=True)
            continue

        # run code agent
        try:
            chat_history, chat_cost = codeAgent.agent_chat(csv_file, tabular_data, sketch_result)
            log.info(f'Agent cost: {chat_cost}')

            file_io.write_json_file(chat_history, os.path.join(agent_dir, f'{base_name}_agent.json'))
            log.info(f'Agent executed: {base_name}')

        except Exception as e:
            log.error(f"agent {base_name} failed with error {e}", exc_info=True)
            continue

        # validate the agent result
        raw_csv = os.path.join(config['raw_data_dir'], csv_file)
        fixed_csv = os.path.join(agent_dir, csv_file)
        validate_msg = f'{base_name} validate as: {compare_csv_files(raw_csv, fixed_csv)}\n'
        log.info(validate_msg)


if __name__ == '__main__':
    # load args
    parser = argparse.ArgumentParser(description="Load Project Configuration")
    parser.add_argument('--config', '-c', type=str, default='./etc/config_template.yaml', help="path to config file")
    args = parser.parse_args()

    # load project-wise config in YAML file
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    # check output_0418 dir
    file_io.check_directory(config['output_dir'])

    # init logger
    log_fp = os.path.join(config['output_dir'], 'run.log')
    logger = logger.setup_logger(fp=log_fp)
    logger.info(f'Config Initialized {config["experiment_name"]}')

    # check input dir
    if not os.path.isdir(config['input_dir']):
        raise FileNotFoundError(f'input data: {config["input_dir"]} does not exist')

    # check sketch working dir
    sketch_dir = str(os.path.join(config['output_dir'], config['sketch_config']['work_dir']))
    file_io.check_directory(sketch_dir)

    # check agent working dir
    agent_dir = str(os.path.join(config['output_dir'], config['agent_config']['work_dir']))
    file_io.check_directory(agent_dir)

    main(config, logger)
