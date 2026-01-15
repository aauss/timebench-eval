import pytest
from timebench_eval import TimebenchEval
from conftest import (
    PREDICTION_1,
    PREDICTION_2,
    PREDICTION_3,
    PREDICTION_4,
    PREDICTION_5,
)


@pytest.mark.parametrize(
    "prediction,extracted_answer",
    [
        (PREDICTION_1, "Troyes AC"),
        (PREDICTION_2, "August 1804"),
        (PREDICTION_3, "unanswerable"),
        (PREDICTION_4, "Cardiff City"),
        (PREDICTION_5, "B, C"),
    ],
)
def test_answer_extraction(prediction, extracted_answer):
    assert TimebenchEval._extract_answer(prediction) == extracted_answer
