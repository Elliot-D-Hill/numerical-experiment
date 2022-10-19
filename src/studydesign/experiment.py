from pandas import DataFrame, concat
from typing import Any, Iterable, Callable


#%%
import pandas as pd

n_rows = 10
fixed = {"A": 0, "B": 0}
variables = {"A": [1, 2], "B": [3, 4, 5]}
rows = []
for name, variable in variables.items():
    for value in variable:
        row = fixed.copy()
        row[name] = value
        rows.append(row)
pd.DataFrame(rows)
#%%


def duplicate_rows(df: DataFrame, n_rows: int) -> DataFrame:
    return df.loc[df.index.repeat(n_rows)].reset_index(drop=True)


def make_parameter_rows(variable: Iterable, name: Any, fixed_parameters: DataFrame):
    n_rows = len(variable)
    parameters = duplicate_rows(fixed_parameters, n_rows)
    parameters[name] = variable
    parameters["variable"] = name
    parameters.index.rename("experiment", inplace=True)
    parameters.index += 1
    return parameters


def make_parameters(
    variables: dict, fixed_parameters: dict, exclude: list[str]
) -> DataFrame:
    fixed_parameters = DataFrame(fixed_parameters, index=[0])
    experiment_parameters = [
        make_parameter_rows(variable, name, fixed_parameters)
        for name, variable in variables.items()
        if name not in exclude
    ]
    return concat(experiment_parameters).reset_index()


# FIXME in next refactor, use dictionary when applying results to function
# instead of a dataframe then convert results to a dataframe
def apply_parameters(f: Callable, df: DataFrame, variable_names: Iterable) -> DataFrame:
    return df.assign(result=df.apply(lambda row: f(*row[variable_names]), axis=1))


def organize_results(results: DataFrame, variable_names: Iterable) -> DataFrame:
    experiment_columns = ["experiment", "variable", "result"]
    return results[experiment_columns + list(variable_names)]


def run_experiment(
    f: Callable, variables: dict, fixed_parameters: dict, exclude: list[str] = None
) -> DataFrame:
    if exclude is None:
        exclude = []
    variable_names = fixed_parameters.keys()
    parameters = make_parameters(variables, fixed_parameters, exclude)
    results = apply_parameters(f, parameters, variable_names)
    return organize_results(results, variable_names)
