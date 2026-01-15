from timebench_eval import TimebenchEval
import pytest
from conftest import (
    PREDICTION_1,
    PREDICTION_2,
    PREDICTION_3,
    PREDICTION_4,
    PREDICTION_5,
)


@pytest.mark.parametrize(
    "prediction,reference,task,expected_metrics",
    [
        (
            PREDICTION_1,
            "Troyes AC",
            "TempReason",
            {
                "exact_match": [1],
                "f1": [1],
            },
        ),
        (
            PREDICTION_2,
            "Aug, 1804",
            "Date Arithmetic",
            {
                "exact_match": [1],
            },
        ),
        (
            PREDICTION_3,
            "unanswerable",
            "MenatQA",
            {
                "exact_match": [1],
                "f1": [1],
            },
        ),
        (
            PREDICTION_4,
            "Cardiff City",
            "MenatQA",
            {
                "exact_match": [1],
                "f1": [1],
            },
        ),
        (
            PREDICTION_5,
            "B. No more than ten minutes && C. No more than five minutes",
            "TimeDial",
            {
                "exact_match": [1],
                "f1": [1],
            },
        ),
        (
            PREDICTION_5,
            "B.",
            "TimeDial",
            {
                "exact_match": [0],
                "f1": [pytest.approx(2 / 3, rel=1e-6)],
            },
        ),
        (
            PREDICTION_5,
            "A.",
            "TimeDial",
            {
                "exact_match": [0],
                "f1": [0],
            },
        ),
    ],
)
def test_eval(prediction, reference, task, expected_metrics):
    metrics = TimebenchEval()._compute([prediction], [reference], task)
    assert metrics == expected_metrics


def test_eval_many():
    metrics = TimebenchEval()._compute(
        [PREDICTION_3, PREDICTION_4], ["unanswerable", "Cardiff City"], "MenatQA"
    )
    assert metrics == {
        "exact_match": [1, 1],
        "f1": [1, 1],
    }
