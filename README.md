---
title: TimeBench Eval
datasets:
- TimeBench
tags:
- evaluate
- metric
- temporal reasoning
description: Evaluation metric for the TimeBench temporal reasoning benchmark by Chu et al. (2023).
sdk: gradio
sdk_version: 6.3.0
app_file: app.py
pinned: false
emoji: ⏰
colorFrom: purple
colorTo: red
---

# Metric Card for TimeBench Eval

## Metric Description

This metric is designed for the **TimeBench** benchmark (Chu et al., 2023), which evaluates temporal reasoning abilities in large language models. It uses modified prompts from the [ADeLe paper by Zhou et al., 2025](https://arxiv.org/abs/2503.06378). It supports multiple task types with different evaluation strategies:

- **TempReason, TimeQA, MenatQA**: Uses SQuAD-style exact match and F1 scoring
- **Date Arithmetic**: Parses and compares dates for exact match
- **TimeDial**: Set-based comparison of selected multiple-choice options (A-D)

The metric expects model outputs to contain the answer in the format `"Thus, the correct answer is: <answer>"`.

It performs the following steps:

1. Extracts the answer from the model's prediction string using the marker `"Thus, the correct answer is:"`.
2. Applies task-specific evaluation:
   - For QA tasks: Computes SQuAD exact match and F1 scores
   - For Date Arithmetic: Parses dates and compares them (day is normalized to 1)
   - For TimeDial: Extracts option letters (A-D) and computes set-based exact match and F1

## How to Use

You can load the metric using the `evaluate` library:

```python
import evaluate

metric = evaluate.load("aauss/timebench_eval")

# Example for Date Arithmetic task
predictions = [
    "Let me solve this step by step... Thus, the correct answer is: Aug, 1987.",
    "Calculating the date... Thus, the correct answer is: January 2020.",
]
references = ["Aug, 1987", "Feb, 2020"]

result = metric.compute(
    predictions=predictions,
    references=references,
    task="Date Arithmetic",
)
print(result)
>>> {"exact_match": [1, 0]}

# Example for TempReason/TimeQA/MenatQA tasks
predictions = [
    "Based on the context... Thus, the correct answer is: Cardiff City.",
    "The answer cannot be determined. Thus, the correct answer is: unanswerable",
]
references = ["Cardiff City", "unanswerable"]

result = metric.compute(
    predictions=predictions,
    references=references,
    task="MenatQA",
)
print(result)
>>> {"exact_match": [1.0, 1.0], "f1": [1.0, 1.0]}

# Example for TimeDial task (multiple choice)
predictions = [
    "Options B and C are correct. Thus, the correct answer is: B, C.",
]
references = ["B. No more than ten minutes && C. No more than five minutes"]

result = metric.compute(
    predictions=predictions,
    references=references,
    task="TimeDial",
)
print(result)
>>> {"exact_match": [1], "f1": [1.0]}
```

### Inputs

- **predictions** (`list` of `str`): List of predictions to score. Each prediction should be a string containing the model's response, which must include the answer after the marker `"Thus, the correct answer is:"`.
- **references** (`list` of `str`): List of reference answers.
- **task** (`str`): The task type being evaluated. Must be one of:
  - `"TempReason"`: Temporal reasoning QA
  - `"TimeQA"`: Time-based QA
  - `"MenatQA"`: Multiple Sensitive Factors Time QA
  - `"Date Arithmetic"`: Date calculation tasks
  - `"TimeDial"`: Dialogue-based temporal multiple choice

### Output Values

The metric returns a dictionary with the following keys (depending on task):

- **exact_match** (`list` of `float` or `int`): Exact match scores for each prediction (0 or 1).
- **f1** (`list` of `float`): F1 scores for each prediction (0.0 to 1.0). Returned for all tasks except Date Arithmetic.

Scores range from 0.0 to 1.0, with higher values indicating better performance.

#### Values from Popular Papers

Refer to the [original TimeBench paper](https://arxiv.org/abs/2311.17667) for baseline performance values across various language models.

## Limitations and Bias

- The metric relies on the marker `"Thus, the correct answer is:"` to extract answers. If the model output does not follow this exact format, extraction will fail and return `None`.
- For Date Arithmetic, dates are parsed using `dateutil.parser` with day normalized to 1. Unparseable dates will result in `None` comparisons.
- For TimeDial, only options A-D are recognized. The extraction looks for standalone letters at word boundaries.
- The metric assumes predictions and references are properly aligned (same length lists).

## Citation

```bibtex
@software{abbood2026timebench_eval,
  title={TimeBench Eval},
  author={Abbood, Auss},
  year={2026},
  url={https://huggingface.co/spaces/aauss/timebench_eval}
}
```

## Further References

- [TimeBench Paper](https://arxiv.org/abs/2311.17667)
- [ADeLe paper which adopts TimeBench](https://huggingface.co/datasets/CFI-Kinds-of-Intelligence/ADeLe_battery_v1dot0)