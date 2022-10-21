# studydesign: a harness for running univariate numerical experiments in python

## Usage

The package `studydesign` is based on a single function `run_experiment`. This function takes 4 parameters:

- `experiment` - a function which returns the results of the experiment as a dictionary
- `variables` - a dictionary containing the variables of the experiment. The keys must match the arguments of the `experiment` function
- `fixed_parameters` - a dictionary containing the fixed values that will be held constant while each variable is varied. The keys of `fixed_parameters` must match the keys of `variables` and `experiment`
- `exclude` - (optional) a list of variables to exclude from the experiment

```python
from studydesign.experiment import run_experiment

# an example experiment function to generate fake results
def experiment(x1, x2, x3):
    result = x1 + x2 + x3
    true_value = 5
    error = abs(result - true_value)
    return {"result": result, "true_value": true_value, "error": error}

variables = {
    "x1": [1, 2],
    "x2": [3, 4, 5],
    "x3": [6, 7, 8]
}
fixed_parameters = {
    "x1": 1,
    "x2": 2,
    "x3": 3
}
results = run_experiment(experiment, variables, fixed_parameters)
print(results)
```
|      | variable |  run |   x1 |   x2 |   x3 | result | true_value | error |
| ---: | :------- | ---: | ---: | ---: | ---: | -----: | ---------: | ----: |
|    0 | x1       |    1 |    1 |    2 |    3 |      6 |          5 |     1 |
|    1 | x1       |    2 |    2 |    2 |    3 |      7 |          5 |     2 |
|    2 | x2       |    1 |    1 |    3 |    3 |      7 |          5 |     2 |
|    3 | x2       |    2 |    1 |    4 |    3 |      8 |          5 |     3 |
|    4 | x2       |    3 |    1 |    5 |    3 |      9 |          5 |     4 |
|    5 | x3       |    1 |    1 |    2 |    6 |      9 |          5 |     4 |
|    6 | x3       |    2 |    1 |    2 |    7 |     10 |          5 |     5 |
|    7 | x3       |    3 |    1 |    2 |    8 |     11 |          5 |     6 |


You can optionally exclude variables with the `exclude` argument.

```python
results_subset = run_experiment(experiment, variables, fixed, exclude=["x1", "x3"])
print(results_subset)
```
|      | variable |  run |   x1 |   x2 |   x3 | result | true_value | error |
| ---: | :------- | ---: | ---: | ---: | ---: | -----: | ---------: | ----: |
|    0 | x2       |    1 |    1 |    3 |    3 |      7 |          5 |     2 |
|    1 | x2       |    2 |    1 |    4 |    3 |      8 |          5 |     3 |
|    2 | x2       |    3 |    1 |    5 |    3 |      9 |          5 |     4 |
