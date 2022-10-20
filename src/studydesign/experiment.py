from numpy import atleast_1d
from pandas import DataFrame
from typing import Callable
from copy import deepcopy


def make_replicates(
    f: Callable, variables: dict, fixed_parameters: dict, exclude: list[str]
) -> dict:
    replicates = []
    for name, variable in variables.items():
        if name not in exclude:
            for i, value in enumerate(atleast_1d(variable)):
                replicate = deepcopy(fixed_parameters)
                replicate[name] = value
                replicate["result"] = f(**replicate)
                replicate["variable"] = name
                replicate["run"] = i + 1
                replicates.append(replicate)
    return replicates


def run_experiment(
    f: Callable, variables: dict, fixed_parameters: dict, exclude: list[str] = None
) -> DataFrame:
    if exclude is None:
        exclude = []
    replicates = make_replicates(f, variables, fixed_parameters, exclude)
    results = DataFrame(replicates)
    results = results[["run", "variable", "result"] + list(fixed_parameters.keys())]
    return results
