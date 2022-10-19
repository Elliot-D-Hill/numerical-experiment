from dataclasses import dataclass
from pandas import DataFrame


@dataclass
class RunExperimentOutputCases:
    default: DataFrame = DataFrame(
        {
            "experiment": {0: 1, 1: 2, 2: 1, 3: 2, 4: 3, 5: 1, 6: 2, 7: 3},
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
            "result": {0: 6, 1: 7, 2: 7, 3: 8, 4: 9, 5: 9, 6: 10, 7: 11},
            "x1": {0: 1, 1: 2, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1},
            "x2": {0: 2, 1: 2, 2: 3, 3: 4, 4: 5, 5: 2, 6: 2, 7: 2},
            "x3": {0: 3, 1: 3, 2: 3, 3: 3, 4: 3, 5: 6, 6: 7, 7: 8},
        }
    )

    exclude_single: DataFrame = DataFrame(
        {
            "experiment": {0: 1, 1: 2, 2: 1, 3: 2, 4: 3},
            "variable": {0: "x1", 1: "x1", 2: "x3", 3: "x3", 4: "x3"},
            "result": {0: 6, 1: 7, 2: 9, 3: 10, 4: 11},
            "x1": {0: 1, 1: 2, 2: 1, 3: 1, 4: 1},
            "x2": {0: 2, 1: 2, 2: 2, 3: 2, 4: 2},
            "x3": {0: 3, 1: 3, 2: 6, 3: 7, 4: 8},
        }
    )

    exclude_multiple: DataFrame = DataFrame(
        {
            "experiment": {0: 1, 1: 2, 2: 3},
            "variable": {0: "x2", 1: "x2", 2: "x2"},
            "result": {0: 7, 1: 8, 2: 9},
            "x1": {0: 1, 1: 1, 2: 1},
            "x2": {0: 3, 1: 4, 2: 5},
            "x3": {0: 3, 1: 3, 2: 3},
        }
    )
