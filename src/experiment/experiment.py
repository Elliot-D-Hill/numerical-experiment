from pandas import DataFrame, concat
from typing import Any, Iterable, Callable


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


def make_parameters(variables: dict, fixed_parameters: dict) -> DataFrame:
    fixed_parameters = DataFrame(fixed_parameters, index=[0])
    experiment_parameters = [
        make_parameter_rows(variable, name, fixed_parameters)
        for name, variable in variables.items()
    ]
    return concat(experiment_parameters).reset_index()


def apply_parameters(
    df: DataFrame, variable_names: Iterable, experiment_fn: Callable
) -> DataFrame:
    return df.assign(
        predicted_value=df.apply(
            lambda row: experiment_fn(*row[variable_names]), axis=1
        )
    )


def organize_results(results: DataFrame, variable_names: Iterable) -> DataFrame:
    experiment_columns = ["experiment", "variable", "predicted_value"]
    return results[experiment_columns + list(variable_names)]


def run_experiment(
    experiment_fn: Callable, variables: dict, fixed_parameters: dict
) -> DataFrame:
    variable_names = fixed_parameters.keys()
    parameters = make_parameters(variables, fixed_parameters)
    results = apply_parameters(parameters, variable_names, experiment_fn)
    return organize_results(results, variable_names)
