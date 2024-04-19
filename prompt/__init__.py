from .formula_sketch import FormulaSketch
from .logical_sketch import LogicalSketch
from .cot_prompt import COTPrompt


def get_prompt_class(prompt_name):
    if prompt_name == 'formula_sketch':
        return FormulaSketch
    elif prompt_name == 'logical_sketch':
        return LogicalSketch
    elif prompt_name == 'cot':
        return COTPrompt
    else:
        raise ValueError(f'Invalid generator name: {prompt_name}')
