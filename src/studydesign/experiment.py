from numpy import atleast_1d
from pandas import DataFrame
from typing import Callable
from copy import deepcopy
from tqdm import tqdm


def exclude_variables(variables: dict, exclude: list) -> dict:
    if exclude is None:
        exclude = []
    return {
        name: variable for name, variable in variables.items() if name not in exclude
    }


def format_results(results: dict) -> DataFrame:
    results = DataFrame(results)
    columns = results.columns.tolist()
    return results[columns[-2:] + columns[:-2]]


def run_experiment(
    experiment: Callable,
    variables: dict,
    fixed_parameters: dict,
    exclude: list[str] = None,
) -> DataFrame:
    variables = exclude_variables(variables, exclude)
    results = []
    for name, variable in variables.items():
        variable = atleast_1d(variable)
        n_values = len(variable)
        values = enumerate(variable)
        for run, value in tqdm(values, total=n_values, desc=name):
            parameters = deepcopy(fixed_parameters)
            parameters[name] = value
            parameters = parameters | experiment(**parameters)
            parameters["variable"] = name
            parameters["run"] = run + 1
            results.append(parameters)
    return format_results(results)
