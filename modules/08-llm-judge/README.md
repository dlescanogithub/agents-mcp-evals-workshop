# Module 8 — Checker, LLM judge, reference labels (optional)

This module is not part of the planned two sessions of three hours. That duration is [EST]. The workshop has not been delivered.

## Goal

Count how often a deterministic checker and an optional LLM judge agree with reference labels. The reference labels in `src/workshop/evalkit/checker.py` were written by the author. They are not a panel of raters, and they are not a model score.

## Concepts

The deterministic checker returns true when a phrase occurs in the text. On the six author-written items it disagrees once: the text says "located in B-1" and the phrase is "bin B-1", while the reference label says pass. `python -m workshop eval` prints that comparison as `checker_vs_reference`. That line is checker vs reference labels written by the author.

The LLM judge is a separate client. It speaks an OpenAI-compatible `chat/completions` body to whatever base URL you set. It is off unless every one of these is set:

| Variable | Role |
| --- | --- |
| `LIVE_MODE` | Must be `1` |
| `LLM_BASE_URL` | Endpoint origin. The client appends `/chat/completions` |
| `LLM_MODEL` | Model name sent in the body |
| `LLM_API_KEY` | Sent as a bearer token. Never commit it |
| `MAX_LIVE_SPEND_USD` | Refuse the call when this is `0`. Drop the label if the priced usage is above it |
| `LLM_INPUT_USD_PER_TOKEN` | Price you read for input tokens, on the day you run |
| `LLM_OUTPUT_USD_PER_TOKEN` | Price you read for output tokens, on the day you run |
| `LLM_PRICE_DATE` | The date you read those prices |

Without that configuration, `python -m workshop llm-judge` prints `llm_judge=not_configured` and exits 2. CI does not set these variables and does not run this command. Tests pass a fake HTTP transport. No live comparison has been run for this repo.

`templates/human_labels.csv` is a header and no data rows. Copy it if you want to add your own labels and compare them with the reference column. Do not commit a key, and do not treat an empty file as a measured agreement.

## Results

No live run is recorded. Leave this table empty.

| item_id | checker | llm_judge | reference_label | human_label |
| --- | --- | --- | --- | --- |

## Files

- Edit `exercises/module_08/exercise.py`
- Checker `src/workshop/evalkit/checker.py`
- Optional client `src/workshop/evalkit/llm_judge.py`
- Label CSV helper `src/workshop/evalkit/labels.py`
- Template `templates/human_labels.csv`

## Run

```bash
PYTHONPATH=src python -m workshop check module-8
PYTHONPATH=src python -m workshop llm-judge
```

The second command exits 2 until you configure it on your own machine.

## What this module does not do

It does not call a model in CI. It does not publish a quality score. It does not fill the results table.
