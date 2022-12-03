from itertools import product
from copy import deepcopy
from typing import Callable, Iterable
from dataclasses import dataclass

from numpy import atleast_1d
from pandas import DataFrame
from tqdm import tqdm


@dataclass
class Experiment:
    f: Callable
    variables: dict
    fixed_parameters: dict

    def __post_init__(self):
        self.variables = self.make_variables_iterable()

    def make_variables_iterable(self) -> dict:
        return {key: atleast_1d(values) for key, values in self.variables.items()}

    def make_parameters(self, manipulated: dict) -> dict:
        parameters = deepcopy(self.fixed_parameters)
        parameters.update(manipulated)
        return parameters

    def run_trial(self, manipulated: dict) -> dict:
        variable_names = list(manipulated.keys())
        parameters = self.make_parameters(manipulated=manipulated)
        outcome = self.f(**parameters)
        return {"manipulated": variable_names} | parameters | outcome

    def run_univariate(self, exclude: list = None) -> DataFrame:
        if exclude is None:
            exclude = []
        return DataFrame(
            [
                self.run_trial(manipulated={name: value})
                for name, variable in self.variables.items()
                if name not in exclude
                for value in tqdm(variable, total=len(variable), desc=name)
            ]
        )

    def make_pair_product(self, pair: tuple[str, str]) -> Iterable:
        variable_pair = [self.variables[key] for key in pair]
        pair_product = product(*variable_pair)
        n_values = len(variable_pair[0]) * len(variable_pair[1])
        return tqdm(pair_product, total=n_values, desc=", ".join(pair))

    def run_bivariate(self, pairs: list[tuple[str, str]]) -> DataFrame:
        return DataFrame(
            [
                self.run_trial(manipulated=dict(zip(pair, values)))
                for pair in pairs
                for values in self.make_pair_product(pair=pair)
            ]
        )
