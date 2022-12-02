import pytest
from pandas.testing import assert_frame_equal

from studydesign.experiment import Experiment, Trial
from cases import ExperimentCases


def fake_experiment(x1, x2, x3):
    result = x1 + x2 + x3
    true_value = 5
    error = abs(result - true_value)
    return {"result": result, "true_value": true_value, "error": error}


class TestExperiment:
    @pytest.fixture(scope="class")
    def cases(self):
        return ExperimentCases()

    @pytest.fixture(scope="function")
    def experiment(self):
        return Experiment(
            f=fake_experiment,
            variables={"x1": [1, 2], "x2": [3, 4, 5], "x3": [6, 7, 8]},
            fixed_parameters={"x1": 1, "x2": 2, "x3": 3},
        )

    def test_run_univariate(self, experiment, cases):
        experiment_output = experiment.run_univariate()
        assert_frame_equal(experiment_output, cases.run_univariate_output)

    def test_run_univariate_exclude_single(self, experiment, cases):
        experiment_output = experiment.run_univariate(exclude=["x2"])
        assert_frame_equal(experiment_output, cases.exclude_single_output)

    def test_run_univariate_exclude_multiple(self, experiment, cases):
        experiment_output = experiment.run_univariate(exclude=["x1", "x3"])
        assert_frame_equal(experiment_output, cases.exclude_multiple_output)

    def test_run_bivariate(self, experiment, cases):
        experiment_output = experiment.run_bivariate(variable_pairs=[("x2", "x3")])
        assert_frame_equal(experiment_output, cases.run_interactions_output)


class TestTrial:
    @pytest.fixture(scope="function")
    def trial_kwargs(self):
        return {
            "variable_name": "name",
            "parameters": {"x1": 1, "x2": 2},
            "outcome": {"result": 0},
        }

    def test_trial(self, trial_kwargs):
        trial = Trial(**trial_kwargs)
        assert trial.to_dict() == {"variable": "name", "x1": 1, "x2": 2, "result": 0}
