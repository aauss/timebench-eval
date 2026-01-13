# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""TODO: Add a description here."""

from dateutil import parser
from dateutil.parser import ParserError


import evaluate
import datasets
import numpy as np


# TODO: Add BibTeX citation
_CITATION = """\
@InProceedings{huggingface:module,
title = {A great new module},
authors={huggingface, Inc.},
year={2020}
}
"""

# TODO: Add description of the module here
_DESCRIPTION = """\
This new module is designed to solve this great ML task and is crafted with a lot of care.
"""


# TODO: Add description of the arguments of the module here
_KWARGS_DESCRIPTION = """
Calculates how good are predictions given some references, using certain scores
Args:
    predictions: list of predictions to score. Each predictions
        should be a string with tokens separated by spaces.
    references: list of reference for each prediction. Each
        reference should be a string with tokens separated by spaces.
Returns:
    accuracy: description of the first score,
    another_score: description of the second score,
Examples:
    Examples should be written in doctest format, and should illustrate how
    to use the function.

    >>> my_new_module = evaluate.load("my_new_module")
    >>> results = my_new_module.compute(references=[0, 1], predictions=[0, 1])
    >>> print(results)
    {'accuracy': 1.0}
"""

# TODO: Define external resources urls if needed
BAD_WORDS_URL = "http://url/to/external/resource/bad_words.txt"


@evaluate.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class TimebenchEval(evaluate.Metric):
    """TODO: Short description of my evaluation module."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.squad_metric = evaluate.load("squad")

    def _info(self):
        # TODO: Specifies the evaluate.EvaluationModuleInfo object
        return evaluate.MetricInfo(
            # This is the description that will appear on the modules page.
            module_type="metric",
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            # This defines the format of each prediction and reference
            features=datasets.Features(
                {
                    "predictions": datasets.Value("int64"),
                    "references": datasets.Value("int64"),
                }
            ),
            # Homepage of the module for documentation
            homepage="http://module.homepage",
            # Additional links to the codebase or references
            codebase_urls=["http://github.com/path/to/codebase/of/new_module"],
            reference_urls=["http://path.to.reference.url/new_module"],
        )

    @staticmethod
    def _extract_answer(response: str) -> str | None:
        """Extract the answer from the response"""
        marker = "Thus, the correct answer is:"

        if marker not in response:
            return None
        answer = response.split(marker)[-1]
        # Take only the first line (stops at newlines if model continues)
        answer = answer.strip().split("\n")[0]
        answer = answer.rstrip(".!?").strip()
        if "unanswerable" in answer.lower():
            return "unanswerable"
        return answer or None

    def _call_squad(self, predictions, references):
        exact_matches = []
        f1_scores = []

        for i, (pred, ref) in enumerate(zip(predictions, references)):
            formatted_pred = [
                {"id": "0", "prediction_text": self._extract_answer(pred)}
            ]
            formatted_ref = [
                {"id": "0", "answers": {"text": [self._extract_answer(ref)], "answer_start": [0]}}
            ]

            results = self.squad_metric.compute(
                predictions=formatted_pred, references=formatted_ref
            )
            exact_matches.append(results["exact_match"] / 100)
            f1_scores.append(results["f1"] / 100)

        return {
            "exact_match": exact_matches,
            "f1": f1_scores,
        }

    @staticmethod
    def _parse_historical_date(date_str):
        try:
            return parser.parse(date_str).replace(day=1)
        except ParserError:
            return None

    def _compare_dates(self, predictions, references):
        predictions = [
            self._parse_historical_date(self._extract_answer(pred))
            for pred in predictions
        ]
        references = [self._parse_historical_date(ref) for ref in references]
        return {
            "exact_match": [
                1 if pred == ref else 0 for pred, ref in zip(predictions, references)
            ],
        }

    def _compute(self, predictions, references, task: str):
        """Returns the scores"""
        if task in [
            "TempReason",
            "TimeQA",
            "MenatQA",
        ]:
            return self._call_squad(predictions, references)
        elif task == "Date Arithmetic":
            return self._compare_dates(predictions, references)
