import os
import yaml
import argparse

from llm.chat import sketch_llm
from llm.agent import CodeAgent
from utils import file_io, logger
from eval import evaluate


def main(cfg, log):
    # init sketch llm
    log.info(f"Backend LLM: {cfg['openai_config']['model']}")

    # init code agent
    codeAgent = CodeAgent(agent_dir, cfg['openai_config'])

    # output path
    fix_report = list()
    fix_report_fp = os.path.join(exp_dir, 'fix_report.json')

    # Read input data
    for csv_file in os.listdir(input_dir):
        input_fp = os.path.join(input_dir, csv_file)
        tabular_data = file_io.read_csv(input_fp)
        base_name = os.path.splitext(os.path.basename(input_fp))[0]  # keep the same as the input file name
        log.info(f'test init: {base_name}')

        print(f'Running test on file {base_name}...')

        # generate sketch by prompt engineering
        try:
            sketch_fp = os.path.join(sketch_dir, f'{base_name}.txt')
            sketch_result = sketch_llm(tabular_data, cfg)
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
        slice_csv = os.path.join(slice_dir, csv_file)
        fixed_csv = os.path.join(agent_dir, csv_file)

        is_identical, fix_summary = evaluate.compare_csv_files(slice_csv, fixed_csv, log)
        log.info(f'{base_name} imputation validated as: {is_identical}\n')

        # store fix result
        if len(fix_summary) > 0:
            fix_report.extend(fix_summary)
            file_io.write_json_file(fix_report, fix_report_fp)


if __name__ == '__main__':
    # load args
    parser = argparse.ArgumentParser(description="Load Project Configuration")
    parser.add_argument('--config', type=str, default='./etc/config_template.yaml', help="path to config file")
    parser.add_argument('--exp-dir', type=str, default='./experiments/test', help="path to experiment directory")
    args = parser.parse_args()

    # load project-wise config in YAML file
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    # check exp dir, store all tests with related file I/Os
    exp_dir = args.exp_dir
    if not os.path.isdir(exp_dir):
        raise NotADirectoryError

    # init logger
    log_fp = os.path.join(exp_dir, 'run.log')
    logger = logger.setup_logger(fp=log_fp)
    logger.info(f'Config Initialized {exp_dir}, prompt type: {config["prompt_type"]}')

    # check slice dir (original clean data as ground truth)
    slice_dir = str(os.path.join(exp_dir, config['slice_dir']))

    # check table input dir (dirty table input)
    input_dir = str(os.path.join(exp_dir, config['input_dir']))

    # check sketch working dir
    sketch_dir = str(os.path.join(exp_dir, config['sketch_work_dir']))
    file_io.check_directory(sketch_dir)

    # check agent working dir (fixed data will be saved here)
    agent_dir = str(os.path.join(exp_dir, config['agent_work_dir']))
    file_io.check_directory(agent_dir)

    main(config, logger)
