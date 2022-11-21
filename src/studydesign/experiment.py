from itertools import product
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


def make_interactions(interactions, experiment, variables, fixed_parameters):
    interaction_parameters = []
    for name_a, name_b in interactions:
        for a, b in product(variables[name_a], variables[name_b]):
            parameters = deepcopy(fixed_parameters)
            parameters[name_a] = a
            parameters[name_b] = b
            parameters = (
                {"variable": name_a + "_" + name_b}
                | parameters
                | experiment(**parameters)
            )
            interaction_parameters.append(parameters)
    return interaction_parameters


def run_experiment(
    experiment: Callable,
    variables: dict,
    fixed_parameters: dict,
    interactions: list[tuple[str]] = None,
    exclude: list[str] = None,
) -> DataFrame:
    variables = exclude_variables(variables, exclude)
    results = []
    for name, variable in variables.items():
        for run, value in tqdm(atleast_1d(variable), total=len(variable), desc=name):
            parameters = deepcopy(fixed_parameters)
            parameters[name] = value
            parameters = {"variable": name} | parameters | experiment(**parameters)
            results.append(parameters)
    if interactions is not None:
        iteraction_results = make_interactions(
            interactions, experiment, variables, fixed_parameters
        )
        results = results + iteraction_results
    return DataFrame(results)
