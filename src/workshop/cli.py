"""Command line. `python -m workshop demo` is the offline demo."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from workshop import __version__
from workshop.budget import SIMULATED_USD_PER_TOKEN
from workshop.capstone import demo_result
from workshop.evalkit.cases import HAPPY_QUESTION
from workshop.evalkit.gate import run_gate, run_regression
from workshop.evalkit.judge import calibrate
from workshop.grading import grade
from workshop.logging_setup import configure
from workshop.secretscan import scan_path

MODULES = ("1", "2", "3", "4", "5", "6", "7")


def normalize_module(raw: str) -> str | None:
    text = raw.strip().lower().replace("_", "-")
    if text.startswith("module-"):
        text = text[len("module-") :]
    if text == "all":
        return "all"
    if text in MODULES:
        return text
    return None


def _cmd_check(module: str, impl: str) -> int:
    selected = MODULES if module == "all" else (module,)
    failed = False
    for module_id in selected:
        report = grade(module_id, impl)
        names = ",".join(report.failed_names)
        print(f"module={module_id} impl={impl} pass={report.passed} fail={report.failed} failed={names}")
        for name, ok, detail in report.checks:
            if not ok and detail:
                print(f"  {name}: {detail}")
        if report.failed:
            failed = True
    return 1 if failed else 0


def _cmd_eval() -> int:
    report = run_gate()
    for item in report.results:
        failed = ",".join(item.failed_invariants)
        print(
            f"case={item.case_id} pass={'yes' if item.passed else 'no'} "
            f"stop={item.stop_reason} model_calls={item.model_calls} "
            f"simulated_cost_usd={item.spent_usd:.8f} failed={failed}"
        )
    status = "pass" if report.failed == 0 else "fail"
    calibration = calibrate()
    print(f"gate={status} cases={len(report.results)} failed={report.failed}")
    print(
        f"calibration_agreement={calibration.agreements}/{calibration.items} "
        f"disagreements={calibration.disagreements}"
    )
    print(f"simulated_price_usd_per_token={SIMULATED_USD_PER_TOKEN}")
    print("provider=fake")
    return 0 if report.failed == 0 else 1


def _cmd_regression() -> int:
    case_result, run = run_regression()
    names = ",".join(case_result.failed_invariants)
    print(
        f"case={case_result.case_id} pass={'yes' if case_result.passed else 'no'} "
        f"stock_unchanged={run.stock_unchanged} failed={names}"
    )
    red = (
        not case_result.passed
        and not run.stock_unchanged
        and "no_harmful_effect" in case_result.failed_invariants
    )
    if red:
        print("regression_result=gate_red")
        return 1
    print("regression_result=gate_green_unexpected")
    return 0


def _cmd_demo() -> int:
    result = demo_result()
    effects = ",".join(f"{effect.kind}:{effect.tool}" for effect in result.effects) or "none"
    print(f"question: {HAPPY_QUESTION}")
    print(f"answer: {result.final_text}")
    print(f"stop_reason: {result.stop_reason}")
    print(f"model_calls: {result.model_calls}")
    print(f"effects: {effects}")
    print(f"simulated_cost_usd: {result.spent_usd:.8f}")
    print(f"simulated_latency_ms: {result.latency_ms}")
    print("provider: fake")
    print("network: none")
    return 0 if result.stop_reason == "final" and result.stock_unchanged else 1


def _cmd_secretscan(path: str) -> int:
    findings = scan_path(Path(path))
    for finding in findings:
        print(f"{finding.path}:{finding.line}:{finding.rule}")
    print(f"findings={len(findings)}")
    return 1 if findings else 0


def main(argv: list[str] | None = None) -> int:
    configure()
    parser = argparse.ArgumentParser(prog="workshop")
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command", required=True)

    check = commands.add_parser("check", help="grade a module by invariants")
    check.add_argument("module", help="module-1 .. module-7, or all")
    check.add_argument("--impl", choices=("exercise", "solution"), default="exercise")

    commands.add_parser("demo", help="run the scripted shift-assistant demo")
    commands.add_parser("eval", help="run the offline eval gate")
    commands.add_parser("eval-regression", help="prove the gate can go red")

    scan = commands.add_parser("secretscan", help="scan a tree for token-shaped strings")
    scan.add_argument("path", nargs="?", default=".")

    args = parser.parse_args(argv)
    if args.command == "check":
        module = normalize_module(args.module)
        if module is None:
            print(f"unknown module {args.module}", file=sys.stderr)
            return 2
        return _cmd_check(module, args.impl)
    if args.command == "demo":
        return _cmd_demo()
    if args.command == "eval":
        return _cmd_eval()
    if args.command == "eval-regression":
        return _cmd_regression()
    if args.command == "secretscan":
        return _cmd_secretscan(args.path)
    print(f"unknown command {args.command}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
