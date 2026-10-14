"""
Passli Selenium WebDriver Automated Testing Suite — Main Entry Point
===================================================================
Run either with the interactive Live Tkinter Dashboard or via CLI.

Usage:
    # 1. Interactive Desktop Dashboard (Recommended for Video Presentation):
    python selenium_testing/main.py

    # 2. Command-Line Execution (Full Suite):
    python selenium_testing/main.py --cli --suite normal
    python selenium_testing/main.py --cli --suite demo
    python selenium_testing/main.py --cli --suite all

    # 3. Command-Line Execution (Individual Test with Custom Presentation Delay):
    python selenium_testing/main.py --cli --test TC01 --delay 2.0
    python selenium_testing/main.py --cli --test TC05 --delay 1.5
    python selenium_testing/main.py --cli --test DEMO_FAIL_01
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
        "--test",
        type=str,
        default=None,
        help="Execute an individual test by ID (e.g. TC01, TC05, DEMO_FAIL_02)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=None,
        help="Step pause duration in seconds between browser actions for live explanation (default: 1.5s)",
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

    if args.delay is not None:
        test_config.set_step_delay(args.delay)

    if args.headless:
        test_config.HEADLESS = True

    # If --test is provided, default to CLI mode unless explicitly asked otherwise
    if args.test:
        args.cli = True

    if args.cli:
        suite_type = "single" if args.test else args.suite
        test_label = args.test if args.test else args.suite.upper()

        print("\n" + "=" * 70)
        print("  PASSLI AUTOMATED SELENIUM TEST SUITE — CLI RUNNER")
        print("=" * 70)
        print(f"Target URL:    {test_config.BASE_URL}")
        print(f"Target Run:    {test_label}")
        print(f"Step Pacing:   {test_config.STEP_DELAY}s per action")
        print(f"Headless:      {test_config.HEADLESS}")
        print("=" * 70 + "\n")

        from selenium_testing.test_runner import TestSuiteRunner

        runner = TestSuiteRunner()
        summary = runner.run_suite(
            suite_type=suite_type,
            single_test_id=args.test,
            headless=test_config.HEADLESS,
            step_delay=test_config.STEP_DELAY,
        )

        if not summary:
            sys.exit(1)

        print("\n" + "=" * 70)
        print("  EXECUTION COMPLETE")
        print("=" * 70)
        print(f"Total Tests:   {summary['total_tests']}")
        print(f"Passed:        {summary['passed']}")
        print(f"Failed:        {summary['failed']}")
        print(f"Skipped:       {summary['skipped']}")
        print(f"Duration:      {summary['total_duration_seconds']}s")
        print(f"HTML Report:   {test_config.REPORTS_DIR / 'report.html'}")
        print(f"JSON Report:   {test_config.REPORTS_DIR / 'report.json'}")
        print("=" * 70 + "\n")

        # Exit code reflects genuine failures (ignoring demo failures if running demo suite)
        if suite_type == "normal" and summary["failed"] > 0:
            sys.exit(1)
        sys.exit(0)
    else:
        # Launch Tkinter Dashboard
        from selenium_testing.dashboard import launch_dashboard
        launch_dashboard()


if __name__ == "__main__":
    main()
