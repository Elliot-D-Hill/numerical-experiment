from dataclasses import dataclass, field
from pandas import DataFrame


@dataclass
class FormatResultsCases:
    default_input: list[dict] = field(init=False, default_factory=list)
    default_output: DataFrame = DataFrame(
        {
            "variable": {0: "x1", 1: "x1", 2: "x2", 3: "x2", 4: "x2"},
            "run": {0: 1, 1: 2, 2: 1, 3: 2, 4: 3},
            "x1": {0: 1, 1: 2, 2: 1, 3: 1, 4: 1},
            "x2": {0: 2, 1: 2, 2: 3, 3: 4, 4: 5},
            "result": {0: 3, 1: 4, 2: 4, 3: 5, 4: 6},
            "true_value": {0: 5, 1: 5, 2: 5, 3: 5, 4: 5},
        }
    )

    def __post_init__(self):
        self.default_input = [
            {
                "x1": 1,
                "x2": 2,
                "result": 3,
                "true_value": 5,
                "variable": "x1",
                "run": 1,
            },
            {
                "x1": 2,
                "x2": 2,
                "result": 4,
                "true_value": 5,
                "variable": "x1",
                "run": 2,
            },
            {
                "x1": 1,
                "x2": 3,
                "result": 4,
                "true_value": 5,
                "variable": "x2",
                "run": 1,
            },
            {
                "x1": 1,
                "x2": 4,
                "result": 5,
                "true_value": 5,
                "variable": "x2",
                "run": 2,
            },
            {
                "x1": 1,
                "x2": 5,
                "result": 6,
                "true_value": 5,
                "variable": "x2",
                "run": 3,
            },
        ]


@dataclass
class ExcludeVariablesCases:
    exclude_single_output: dict = field(init=False, default_factory=dict)
    exclude_multiple_output: dict = field(init=False, default_factory=dict)

    def __post_init__(self):
        self.exclude_single_output = {"x1": [1, 2], "x3": [6, 7, 8]}
        self.exclude_multiple_output = {"x2": [3, 4, 5]}


@dataclass
class RunExperimentCases:
    default_output: DataFrame = DataFrame(
        {
            "variable": {
                0: "x1",
                1: "x1",
                2: "x2",
                3: "x2",
                4: "x2",
                5: "x3",
                6: "x3",
                7: "x3",
            },
            "run": {0: 1, 1: 2, 2: 1, 3: 2, 4: 3, 5: 1, 6: 2, 7: 3},
            "x1": {0: 1, 1: 2, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1},
            "x2": {0: 2, 1: 2, 2: 3, 3: 4, 4: 5, 5: 2, 6: 2, 7: 2},
            "x3": {0: 3, 1: 3, 2: 3, 3: 3, 4: 3, 5: 6, 6: 7, 7: 8},
            "result": {0: 6, 1: 7, 2: 7, 3: 8, 4: 9, 5: 9, 6: 10, 7: 11},
            "true_value": {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5},
            "error": {0: 1, 1: 2, 2: 2, 3: 3, 4: 4, 5: 4, 6: 5, 7: 6},
        }
    )
    exclude_single_output: DataFrame = DataFrame(
        {
            "variable": {0: "x1", 1: "x1", 2: "x3", 3: "x3", 4: "x3"},
            "run": {0: 1, 1: 2, 2: 1, 3: 2, 4: 3},
            "x1": {0: 1, 1: 2, 2: 1, 3: 1, 4: 1},
            "x2": {0: 2, 1: 2, 2: 2, 3: 2, 4: 2},
            "x3": {0: 3, 1: 3, 2: 6, 3: 7, 4: 8},
            "result": {0: 6, 1: 7, 2: 9, 3: 10, 4: 11},
            "true_value": {0: 5, 1: 5, 2: 5, 3: 5, 4: 5},
            "error": {0: 1, 1: 2, 2: 4, 3: 5, 4: 6},
        }
    )
    exclude_multiple_output: DataFrame = DataFrame(
        {
            "variable": {0: "x2", 1: "x2", 2: "x2"},
            "run": {0: 1, 1: 2, 2: 3},
            "x1": {0: 1, 1: 1, 2: 1},
            "x2": {0: 3, 1: 4, 2: 5},
            "x3": {0: 3, 1: 3, 2: 3},
            "result": {0: 7, 1: 8, 2: 9},
            "true_value": {0: 5, 1: 5, 2: 5},
            "error": {0: 2, 1: 3, 2: 4},
        }
    )
