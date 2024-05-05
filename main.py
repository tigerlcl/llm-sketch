import os
import yaml
import argparse

from llm.sketch import sketch_llm, parse_cot_summary
from llm.agent import CodeAgent
from utils import file_io, logger


def main(cfg, log):
    log.info(f"Backend LLM: {cfg['openai_config']['model']}")

    # output path
    fix_report = list()
    fix_report_fp = os.path.join(exp_dir, 'fix_report.json')

    # Read input data
    for csv_file in os.listdir(input_dir):
        input_fp = os.path.join(input_dir, csv_file)
        tabular_data = file_io.read_csv(input_fp)
        base_name = os.path.splitext(os.path.basename(input_fp))[0]  # keep the same as the input file name
        print(f'Running test on file {base_name}...')
        log.info(f'test init: {base_name}')

        # generate solution by prompt engineering
        sketch_fp = os.path.join(sketch_dir, f'{base_name}.txt')
        sketch_result, sketch_cost = sketch_llm(tabular_data, cfg)

        # store the Sketch response
        file_io.write_txt_file(sketch_result, sketch_fp)
        log.info(f'Sketch result saved with cost: {sketch_cost}')

        if cfg['prompt_type'] == "cot":
            fixed_value = parse_cot_summary(sketch_result)
        elif cfg['prompt_type'] == "sketch":
            # check agent working dir (fixed data will be saved here)
            agent_dir = str(os.path.join(exp_dir, config['agent_work_dir']))
            file_io.check_directory(agent_dir)

            # convert sketch output as PyCode for imputation test
            codeAgent = CodeAgent(cfg['openai_config'])
            agent_cost, chat_history, fixed_value = codeAgent.agent_chat(tabular_data, sketch_result)
            file_io.write_json_file(chat_history, os.path.join(agent_dir, f'{base_name}.json'))
            log.info(f'Agent result saved with cost: {agent_cost}')
        else:
            raise ValueError("Invalid prompt type")

        # validate the agent result
        raw_result = slice_report.get(csv_file)
        value = raw_result["value"]
        # compare the value in str
        is_fixed = str(value) == str(fixed_value)

        fix_summary = raw_result.copy()
        fix_summary.update({
            'fixed_value': fixed_value,
            'is_fixed': is_fixed,
            'slice': csv_file,
        })
        fix_report.append(fix_summary)
        log.info(f'{base_name} imputation validated as: {is_fixed}\n')

        # store fix result
        file_io.write_json_file(fix_report, fix_report_fp)


if __name__ == '__main__':
    # load args
    parser = argparse.ArgumentParser(description="Load Project Configuration")
    parser.add_argument('--config', type=str, default='./etc/config_template.yaml', help="path to config file")
    parser.add_argument('--exp-dir', type=str, default='./experiments/test', help="path to experiment directory")
    parser.add_argument('--prompt-type', type=str, help="prompt type: cot or sketch")
    args = parser.parse_args()

    # load project-wise config in YAML file
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    # assert prompt type
    config['prompt_type'] = args.prompt_type

    # check exp dir, store all tests with related file I/Os
    exp_dir = args.exp_dir
    if not os.path.isdir(exp_dir):
        raise NotADirectoryError

    # load slice report
    slice_report = file_io.read_json_file(os.path.join(exp_dir, 'slice_report.json'))

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

    main(config, logger)
