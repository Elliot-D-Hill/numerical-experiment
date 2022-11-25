from itertools import product
from copy import deepcopy
from typing import Callable
from dataclasses import dataclass, field

from numpy import atleast_1d
from pandas import DataFrame
from tqdm import tqdm


@dataclass
class Trial:
    variable_name: str
    parameters: dict
    outcome: dict

    def to_dict(self):
        return {"variable": self.variable_name} | self.parameters | self.outcome


@dataclass
class Experiment:
    f: Callable
    variables: dict
    fixed_parameters: dict
    trials: list[Trial] = field(default_factory=list)

    def run_univariate(self, exclude: list = None) -> DataFrame:
        if exclude is None:
            exclude = []
        trials = []
        for name, variable in self.variables.items():
            if name in exclude:
                continue
            values = atleast_1d(variable)
            for value in tqdm(values, total=len(values), desc=name):
                parameters = deepcopy(self.fixed_parameters)
                parameters[name] = value
                outcome = self.f(**parameters)
                trials.append(Trial(name, parameters, outcome))
        return self.to_dataframe(trials)

    def run_interactions(self, interactions: list[tuple[str, str]]) -> DataFrame:
        trials = []
        for name_a, name_b in interactions:
            name = name_a + "_" + name_b
            variable_a = self.variables[name_a]
            variable_b = self.variables[name_b]
            n_values = len(variable_a) * len(variable_b)
            values = product(variable_a, variable_b)
            for value_a, value_b in tqdm(values, total=n_values, desc=name):
                parameters = deepcopy(self.fixed_parameters)
                parameters[name_a] = value_a
                parameters[name_b] = value_b
                outcome = self.f(**parameters)
                trials.append(Trial(name, parameters, outcome))
        return self.to_dataframe(trials)

    def to_dataframe(self, trials: list[Trial]) -> DataFrame:
        return DataFrame([trial.to_dict() for trial in trials])
