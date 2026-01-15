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

import re
from datetime import datetime

from dateutil import parser
from dateutil.parser import ParserError

import evaluate
import datasets


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
                    "predictions": datasets.Value("string"),
                    "references": datasets.Value("string"),
                }
            ),
            # Homepage of the module for documentation
            homepage="http://module.homepage",
            # Additional links to the codebase or references
            codebase_urls=["http://github.com/path/to/codebase/of/new_module"],
            reference_urls=["http://path.to.reference.url/new_module"],
        )

    def _compute(
        self, predictions: list[str], references: list[str], task: str
    ) -> dict[str, list[float]]:
        """
        Compute evaluation metrics for the given predictions and references.

        Args:
            predictions: List of prediction strings to evaluate.
            references: List of reference strings to compare against.
            task: Task type, one of: "TempReason", "TimeQA", "MenatQA", "Date Arithmetic", "TimeDial".

        Returns:
            Dictionary containing metric scores (exact_match and/or f1) as lists of floats.
        """
        if task in [
            "TempReason",
            "TimeQA",
            "MenatQA",
        ]:
            return self._call_squad(predictions, references)
        elif task == "Date Arithmetic":
            return self._compare_dates(predictions, references)
        elif task == "TimeDial":
            return self._compute_timedial(predictions, references)

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

    def _extract_selected_options(self, text: str) -> set[str]:
        """
        Extract selected option letters (A, B, C, D) from various formats:
        - "B, C"
        - "B and C"
        - "B & C"
        - "B && C"
        - "B. No more than ten minutes && C. No more than five minutes"
        - "Options B and C"
        - "The answer is B, C"
        """
        if not text:
            return set()

        # Pattern matches option letters that appear:
        # 1. At word boundary followed by period, comma, space, &, or end: \b[A-D](?=[.\s,&]|$)
        # 2. This avoids matching letters inside words like "CAD" or "BAD"

        # Find all A, B, C, D that look like option selections
        # They should be at a word boundary and followed by typical delimiters
        pattern = r"\b([A-D])(?:\.|,|\s|&|$)"

        matches = re.findall(pattern, text)
        return set(matches)

    def _call_squad(
        self, predictions: list[str], references: list[str]
    ) -> dict[str, list[float]]:
        """
        Compute SQuAD metrics (Exact Matchand F1) for predictions and references.

        Args:
            predictions: List of prediction strings.
            references: List of reference answer strings.

        Returns:
            Dictionary with "exact_match" and "f1" keys, each containing a list of scores.
        """
        exact_matches = []
        f1_scores = []

        for i, (pred, ref) in enumerate(zip(predictions, references)):
            formatted_pred = [
                {"id": "0", "prediction_text": self._extract_answer(pred) or ""}
            ]
            formatted_ref = [
                {"id": "0", "answers": {"text": [ref], "answer_start": [0]}}
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

    def _compare_dates(
        self, predictions: list[str], references: list[str]
    ) -> dict[str, list[int]]:
        """
        Parses and compares dates in predictions and references for exact match.

        Args:
            predictions: List of prediction strings containing dates.
            references: List of reference date strings.

        Returns:
            Dictionary with "exact_match" key containing a list of 0/1 scores.
        """
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

    def _compute_timedial(
        self, predictions: list[str], references: list[str]
    ) -> dict[str, list[float]]:
        """
        Compute TimeDial metrics (Exact Match and F1) using set-based comparison of selected options.

        Args:
            predictions: List of prediction strings.
            references: List of reference strings containing selected options.

        Returns:
            Dictionary with "exact_match" and "f1" keys, each containing a list of scores.
        """
        exact_matches = []
        f1_scores = []

        for pred, ref in zip(predictions, references):
            pred_answer = self._extract_answer(pred)  # Get text after marker
            pred_options = (
                self._extract_selected_options(pred_answer) if pred_answer else set()
            )
            ref_options = self._extract_selected_options(ref)

            # Exact match: sets must be identical
            em = 1 if pred_options == ref_options else 0
            exact_matches.append(em)

            # F1: set-based
            if not pred_options and not ref_options:
                f1 = 1.0  # Both empty = perfect match
            elif not pred_options or not ref_options:
                f1 = 0.0  # One empty, one not
            else:
                tp = len(pred_options & ref_options)
                precision = tp / len(pred_options)
                recall = tp / len(ref_options)
                f1 = (
                    2 * precision * recall / (precision + recall)
                    if (precision + recall) > 0
                    else 0.0
                )
            f1_scores.append(f1)

        return {"exact_match": exact_matches, "f1": f1_scores}

    @staticmethod
    def _parse_historical_date(date_str: str) -> datetime | None:
        """
        Parse a date string and return a datetime object with day set to 1.

        Args:
            date_str: String representation of a date.

        Returns:
            datetime object with day set to 1, or None if parsing fails.
        """
        try:
            return parser.parse(date_str).replace(day=1)
        except ParserError:
            return None
