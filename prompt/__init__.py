from .formula_sketch import FormulaSketch


def get_prompt_class(prompt_name):
    if prompt_name == 'formula_sketch':
        return FormulaSketch
    else:
        raise ValueError(f'Invalid generator name: {prompt_name}')
