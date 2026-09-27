"""Framework runner with CLI flags.

Usage examples:
    python run.py                          # run all scenarios on dev
    python run.py --tags=@smoke            # only smoke scenarios
    python run.py --env=qa                 # switch environment
    python run.py --allure                 # generate + open Allure report
    python run.py --tags=@database --allure
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ALLURE_RESULTS = ROOT / "reports" / "allure-results"
ALLURE_REPORT = ROOT / "reports" / "allure-report"


def _clean_allure_results() -> None:
    if ALLURE_RESULTS.exists():
        shutil.rmtree(ALLURE_RESULTS)
    ALLURE_RESULTS.mkdir(parents=True, exist_ok=True)


def _run_behave(tags: str | None, extra: list[str]) -> int:
    cmd = [sys.executable, "-m", "behave"]
    if tags:
        cmd += ["--tags", tags]
    cmd += extra
    print(">> " + " ".join(cmd))
    return subprocess.call(cmd, cwd=str(ROOT))


def _generate_allure_report() -> int:
    print(">> Generating Allure report...")
    rc = subprocess.call(
        ["allure.bat", "generate", str(ALLURE_RESULTS), "-o", str(ALLURE_REPORT), "--clean"],
        cwd=str(ROOT),
    )
    if rc == 0:
        print(f">> Report ready: {ALLURE_REPORT}\\index.html")
        print(">> To open in browser:  allure open reports/allure-report")
    return rc


def main() -> int:
    parser = argparse.ArgumentParser(description="API Automation Framework Runner")
    parser.add_argument("--env", default=None, help="Environment: dev | qa | prod")
    parser.add_argument("--tags", default=None, help="Behave tag expression, e.g. @smoke")
    parser.add_argument("--allure", action="store_true", help="Generate Allure HTML report after run")
    parser.add_argument("--clean", action="store_true", help="Clear allure-results before run")
    parser.add_argument("extra", nargs=argparse.REMAINDER, help="Extra args passed to behave")
    args = parser.parse_args()

    if args.env:
        os.environ["ENV"] = args.env
        print(f">> Environment set to: {args.env}")

    if args.clean or args.allure:
        _clean_allure_results()

    rc = _run_behave(args.tags, args.extra)
    if rc != 0:
        print(f">> Behave exited with code {rc}")

    if args.allure:
        _generate_allure_report()

    return rc


if __name__ == "__main__":
    sys.exit(main())