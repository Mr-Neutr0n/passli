"""
TC02 — Verify Page Title
========================
Test Steps:
1. Open the application and wait for page to settle.
2. Read the actual browser title.
3. Compare it with the expected title obtained from the project.
4. Report PASS if the assertion succeeds.
5. Report FAIL if the assertion fails.
"""

from .. import test_config
from ..driver_factory import get_shared_driver, capture_screenshot, pause, wait_for_page_ready


def run_test(driver=None, record_callback=None):
    """
    Execute TC02: Verify Page Title matches expected brand title.
    """
    owns_driver = driver is None
    if owns_driver:
        driver = get_shared_driver()

    try:
        if record_callback:
            record_callback("Opening application and checking page readiness...")

        # Step 1: Open application and wait for readiness
        driver.get(test_config.BASE_URL)
        wait_for_page_ready(driver, step_reporter=record_callback)
        pause()

        if record_callback:
            record_callback("Reading browser document title...")

        # Step 2: Read actual browser title
        actual_title = driver.title.strip()
        expected_title = test_config.EXPECTED_HOME_TITLE

        # Step 3: Compare titles with assertion
        assert actual_title == expected_title, (
            f"Title mismatch! Expected '{expected_title}', but got '{actual_title}'."
        )

        screenshot_path = capture_screenshot(driver, "TC02", "PASS")
        return {
            "test_id": "TC02",
            "name": "Verify Page Title",
            "status": "PASS",
            "duration": 0.0,
            "message": f"Page title matches expected value: '{actual_title}'",
            "expected": expected_title,
            "actual": actual_title,
            "screenshot": screenshot_path,
        }
    except Exception as e:
        screenshot_path = capture_screenshot(driver, "TC02", "FAIL") if driver else ""
        return {
            "test_id": "TC02",
            "name": "Verify Page Title",
            "status": "FAIL",
            "duration": 0.0,
            "message": str(e),
            "expected": test_config.EXPECTED_HOME_TITLE,
            "actual": driver.title if driver else "Unknown",
            "screenshot": screenshot_path,
        }
    finally:
        if not test_config.KEEP_BROWSER_OPEN and owns_driver and driver:
            try:
                driver.quit()
            except Exception:
                pass
