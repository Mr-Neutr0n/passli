"""
Passli Selenium WebDriver Automated Testing Suite — Main Entry Point
===================================================================
Run either with the interactive Live Tkinter Dashboard or via CLI.

Usage:
    # 1. Interactive Desktop Dashboard (Recommended for Video Presentation):
    python selenium_testing/main.py

    # 2. Command-Line Execution (Headless or Terminal):
    python selenium_testing/main.py --cli --suite normal
    python selenium_testing/main.py --cli --suite demo
    python selenium_testing/main.py --cli --suite all
"""

import sys
import argparse
from pathlib import Path

# Add project root to sys.path so modules resolve cleanly
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from selenium_testing import test_config


def main():
    parser = argparse.ArgumentParser(
        description="Passli Selenium WebDriver Automated Testing Suite"
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Run tests in CLI mode without launching the Tkinter dashboard GUI",
    )
    parser.add_argument(
        "--suite",
        choices=["normal", "demo", "all"],
        default="normal",
        help="Which test suite to execute in CLI mode (default: normal)",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode",
    )
    parser.add_argument(
        "--url",
        type=str,
        default=None,
        help=f"Target application URL (defaults to {test_config.BASE_URL})",
    )

    args = parser.parse_args()

    if args.url:
        test_config.BASE_URL = args.url.rstrip("/")

    if args.headless:
        test_config.HEADLESS = True

    if args.cli:
        print("\n" + "=" * 70)
        print("  PASSLI AUTOMATED SELENIUM TEST SUITE — CLI RUNNER")
        print("=" * 70)
        print(f"Target URL: {test_config.BASE_URL}")
        print(f"Suite:      {args.suite.upper()}")
        print(f"Headless:   {test_config.HEADLESS}")
        print("=" * 70 + "\n")

        from selenium_testing.test_runner import TestSuiteRunner

        runner = TestSuiteRunner()
        summary = runner.run_suite(suite_type=args.suite, headless=test_config.HEADLESS)

        print("\n" + "=" * 70)
        print("  EXECUTION COMPLETE")
        print("=" * 70)
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed:      {summary['passed']}")
        print(f"Failed:      {summary['failed']}")
        print(f"Skipped:     {summary['skipped']}")
        print(f"Duration:    {summary['total_duration_seconds']}s")
        print(f"HTML Report: {test_config.REPORTS_DIR / 'report.html'}")
        print(f"JSON Report: {test_config.REPORTS_DIR / 'report.json'}")
        print("=" * 70 + "\n")

        # Exit code reflects genuine failures (ignoring demo failures if running demo suite)
        if args.suite == "normal" and summary["failed"] > 0:
            sys.exit(1)
        sys.exit(0)
    else:
        # Launch Tkinter Dashboard
        from selenium_testing.dashboard import launch_dashboard
        launch_dashboard()


if __name__ == "__main__":
    main()
