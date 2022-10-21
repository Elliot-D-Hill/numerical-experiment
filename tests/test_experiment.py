import pytest
from pandas.testing import assert_frame_equal

from studydesign.experiment import exclude_variables, format_results, run_experiment
from cases import RunExperimentCases, FormatResultsCases, ExcludeVariablesCases


def fake_experiment(x1, x2, x3):
    result = x1 + x2 + x3
    true_value = 5
    error = abs(result - true_value)
    return {"result": result, "true_value": true_value, "error": error}


class TestRunExperiment:
    @pytest.fixture(scope="class")
    def cases(self):
        return RunExperimentCases()

    @pytest.fixture(scope="function")
    def make_input(self):
        """A fixture factory"""

        def make(
            experiment=fake_experiment,
            variables={"x1": [1, 2], "x2": [3, 4, 5], "x3": [6, 7, 8]},
            fixed_parameters={"x1": 1, "x2": 2, "x3": 3},
            exclude=None,
        ):
            return {
                "experiment": experiment,
                "variables": variables,
                "fixed_parameters": fixed_parameters,
                "exclude": exclude,
            }

        return make

    def test_run_experiment(self, make_input, cases):
        experiment_input = make_input()
        experiment_output = run_experiment(**experiment_input)
        assert_frame_equal(experiment_output, cases.default_output)

    def test_run_experiment_exclude_single(self, make_input, cases):
        experiment_input = make_input(exclude=["x2"])
        experiment_output = run_experiment(**experiment_input)
        assert_frame_equal(experiment_output, cases.exclude_single_output)

    def test_run_experiment_exclude_multiple(self, make_input, cases):
        experiment_input = make_input(exclude=["x1", "x3"])
        experiment_output = run_experiment(**experiment_input)
        assert_frame_equal(experiment_output, cases.exclude_multiple_output)


class TestFormatResults:
    @pytest.fixture(scope="class")
    def cases(self):
        return FormatResultsCases()

    def test_format_results(self, cases):
        formatted_results = format_results(cases.default_input)
        assert_frame_equal(formatted_results, cases.default_output)


class TestExcludeVariables:
    @pytest.fixture(scope="class")
    def cases(self):
        return ExcludeVariablesCases()

    @pytest.fixture(scope="function")
    def make_input(self):
        """A fixture factory"""

        def make(
            variables={"x1": [1, 2], "x2": [3, 4, 5], "x3": [6, 7, 8]}, exclude="x2"
        ):
            return {"variables": variables, "exclude": exclude}

        return make

    def test_exclude_variables_single(self, make_input, cases):
        exclude_variables_input = make_input(exclude="x2")
        excluded_variables = exclude_variables(**exclude_variables_input)
        assert excluded_variables == cases.exclude_single_output

    def test_exclude_variables_multiple(self, make_input, cases):
        exclude_variables_input = make_input(exclude=["x1", "x3"])
        excluded_variables = exclude_variables(**exclude_variables_input)
        assert excluded_variables == cases.exclude_multiple_output
