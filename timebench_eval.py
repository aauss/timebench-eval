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
"""Evaluation metric for the TimeBench temporal reasoning benchmark."""

import re
from datetime import datetime

import datasets
import evaluate
from dateutil import parser
from dateutil.parser import ParserError

_CITATION = """\
@software{abbood2026timebench_eval,
  title={TimeBench Eval},
  author={Abbood, Auss},
  year={2026},
  url={https://huggingface.co/spaces/aauss/timebench_eval}
}
"""

_DESCRIPTION = """\
Evaluation metric for the TimeBench benchmark, which assesses temporal reasoning
abilities in large language models. Supports multiple task types including TempReason,
TimeQA, MenatQA, Date Arithmetic, and TimeDial.
"""


_KWARGS_DESCRIPTION = """
Calculates evaluation metrics for temporal reasoning tasks.
Args:
    predictions: list of prediction strings from the model. Each prediction
        should contain the marker "Thus, the correct answer is:" followed by the answer.
    references: list of reference answer strings.
    task: the task type, one of "TempReason", "TimeQA", "MenatQA", "Date Arithmetic", or "TimeDial".
Returns:
    exact_match: list of exact match scores (0 or 1) for each prediction.
    f1: list of F1 scores for each prediction (for applicable tasks).
Examples:
    >>> timebench_eval = evaluate.load("aauss/timebench_eval")
    >>> predictions = ["Let me think... Thus, the correct answer is: Aug, 1987."]
    >>> references = ["Aug, 1987"]
    >>> results = timebench_eval.compute(predictions=predictions, references=references, task="Date Arithmetic")
    >>> print(results)
    {'exact_match': [1]}
"""


@evaluate.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class TimebenchEval(evaluate.Metric):
    """Evaluation metric for TimeBench temporal reasoning tasks."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.squad_metric = evaluate.load("squad")

    def _info(self):
        return evaluate.MetricInfo(
            module_type="metric",
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {
                    "predictions": datasets.Value("string"),
                    "references": datasets.Value("string"),
                }
            ),
            homepage="https://huggingface.co/spaces/aauss/timebench_eval",
            codebase_urls=["https://huggingface.co/spaces/aauss/timebench_eval/tree/main"],
            reference_urls=["https://huggingface.co/datasets/ulab-ai/Time-Bench"],
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
        else:
            raise ValueError(
                f"Unknown task: {task}. Expected one of: TempReason, TimeQA, MenatQA, Date Arithmetic, TimeDial"
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
    def _parse_historical_date(date_str: str | None) -> datetime | None:
        """
        Parse a date string and return a datetime object with day set to 1.

        Args:
            date_str: String representation of a date, or None.

        Returns:
            datetime object with day set to 1, or None if parsing fails or input is None.
        """
        if date_str is None:
            return None
        try:
            return parser.parse(date_str).replace(day=1)
        except ParserError:
            return None
