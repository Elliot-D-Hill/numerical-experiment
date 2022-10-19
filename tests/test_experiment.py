import pytest
from dataclasses import asdict, dataclass
from typing import Callable
from pandas.testing import assert_frame_equal

from studydesign.experiment import run_experiment
from cases import RunExperimentOutputCases


@dataclass
class ExperimentInput:
    f: Callable
    variables: dict
    fixed_parameters: dict
    exclude: list[str] | None = None


class TestRunExperiment:
    @pytest.fixture(scope="class")
    def output_cases(self):
        return RunExperimentOutputCases()

    @pytest.fixture(scope="function")
    def make_experiment(self):
        """A fixture factory"""

        # TODO fixture within fixture for these arguments? Move them to cases.py
        # as part of the dataclass?
        def make(
            f=lambda x1, x2, x3: x1 + x2 + x3,
            variables={"x1": [1, 2], "x2": [3, 4, 5], "x3": [6, 7, 8]},
            fixed_parameters={"x1": 1, "x2": 2, "x3": 3},
            exclude=None,
        ):
            experiment_input = ExperimentInput(f, variables, fixed_parameters, exclude)
            return asdict(experiment_input)

        return make

    def test_run_experiment(self, make_experiment, output_cases):
        experiment_input = make_experiment()
        experiment_output = run_experiment(**experiment_input)
        assert_frame_equal(experiment_output, output_cases.default)

    def test_run_experiment_exclude_single(self, make_experiment, output_cases):
        experiment_input = make_experiment(exclude=["x2"])
        experiment_output = run_experiment(**experiment_input)
        assert_frame_equal(experiment_output, output_cases.exclude_single)

    def test_run_experiment_exclude_multiple(self, make_experiment, output_cases):
        experiment_input = make_experiment(exclude=["x1", "x3"])
        experiment_output = run_experiment(**experiment_input)
        assert_frame_equal(experiment_output, output_cases.exclude_multiple)
