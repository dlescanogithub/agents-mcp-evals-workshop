# Changelog

## Unreleased

- Translated the remaining Spanish into English. `docs/HOW_IT_WORKS.md` is an English walkthrough for engineers and buyers. The demo script and the former Spanish subtitle cues are English. The dialect label on the How it works link is gone. The demo video binary was not edited. Docs only.
- Removed first-person interview framing from the authorship note and from the business-value competency sentence. Docs only.

## 0.1.2 - 2026-10-22

- Set the package version to 0.1.2 in `pyproject.toml` and `__version__`.
- Added [docs/BUSINESS_VALUE.md](docs/BUSINESS_VALUE.md) and a README section that links to it. The workshop has not been delivered. Delivery cost 4,200 USD, rates, and ROI rows are [EST], with the incident term [SYN]. Docs only.
- Expanded the README: a three-line Start here, the lab agenda, learning outcomes, exercise architecture, per-lab commands, and a "What this does NOT prove" section. Docs only.
- Re-measured on 2026-10-22, package 0.1.1, Python 3.12.3, main commit `9d10f1d4d4dc8045ccb85749204a926bc2dba912`: `python -m pytest --cov=workshop --cov-report=term-missing --cov-fail-under=80` printed 48 passed and 92.79% total coverage (1456 statements, 105 missed). The same day: eval 6 of 6, checker vs author reference labels 5/6, demo SIMULATED cost 0.00012000 and SIMULATED latency 15 ms, solution modules 1–8 fail=0, secretscan findings=0, ruff clean, mypy clean on 79 files, eval-regression exit 1, llm-judge exit 2 without configuration. These counts match the 2026-10-18 run on `496a705e1a21a1d533b57be2160d93e29496d233`. This docs change does not edit `src/`.
- Bumped `actions/setup-python` from 5 to 7.
- Added a three-line TL;DR under the README title and badges. Docs only.
- Bumped `actions/checkout` from 4 to 7.
- Added `docs/demo/`: a narrated recording of a real offline run, with English and Spanish subtitles and a number trace. Docs only.
- Added an Authorship section to the README. Docs only.
- Docs only. Security describes a teaching repo and points vulnerability reports at GitHub private vulnerability reporting.
- Re-measured on 2026-10-18, package 0.1.1, Python 3.12.3, main commit `496a705e1a21a1d533b57be2160d93e29496d233`: eval 6 of 6, checker vs author reference labels 5/6, pytest 48 passed at 92.79% coverage, demo simulated cost 0.00012000 USD and simulated latency 15 ms, solution modules 1–8 fail=0, secretscan findings=0, ruff clean, mypy clean on 79 files, eval-regression exit 1, llm-judge exit 2 without configuration. The original workshop is PR #1, squash `c590b91` on main. A live LLM-judge call was not re-measured.

## 0.1.1 - 2026-10-17

- Renamed the phrase check to deterministic checker. The 5/6 figure is checker vs reference labels written by the author.
- Added an optional LLM-judge client. It is off unless `LIVE_MODE=1` and the `LLM_*` variables are set, it exits 2 without that configuration, and CI does not run it.
- Added optional module 8 and an empty human-label CSV. The results table is empty. No live comparison is recorded.
- Aligned the secret scanner with the vendored pattern list and recorded its sha256.
- Stated that the planned 2×3 h duration is [EST] and that the workshop has not been delivered. The official MCP SDK is not used. The cited spec revision remains 2026-07-28, accessed 2026-10-17.

## 0.1.0 - 2026-10-17

- Initial teaching repo: seven modules, fake provider, cassette, stdio MCP subset, invariant gate, forced regression, CI.
- No live provider calls in the default path.

This version is the workshop material. It is not a release of a hosted product, and this changelog is not a GitHub Release.
