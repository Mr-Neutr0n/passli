"""
TC04 — Text Input Testing
=========================
Test Steps:
1. Locate a real text input field (Login username input #login-username).
2. Enter valid test data.
3. Verify the entered value using DOM attribute check.
4. Clear the field.
5. Verify that the field is empty.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .. import test_config
from ..driver_factory import create_chrome_driver, capture_screenshot, pause, wait_for_page_ready


def run_test(driver=None, record_callback=None):
    """
    Execute TC04: Text input insertion, verification, clearing, and empty validation.
    """
    owns_driver = driver is None
    if owns_driver:
        driver = create_chrome_driver()

    wait = WebDriverWait(driver, test_config.DEFAULT_WAIT_TIMEOUT)

    try:
        if record_callback:
            record_callback("Navigating to login portal...")

        driver.get(f"{test_config.BASE_URL}/login/")
        wait_for_page_ready(driver, step_reporter=record_callback, step_msg="Stabilizing login form elements...")
        pause()

        if record_callback:
            record_callback("Locating username input field...")

        # Step 1: Locate real text input field, scroll into view, and highlight
        username_field = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, test_config.SELECTORS["login_username"]))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest', behavior: 'smooth'});", username_field)
        pause()

        test_payload = "qa_student_automation_test"
        if record_callback:
            record_callback(f"Typing test string: '{test_payload}'...")

        # Step 2: Enter test data
        username_field.clear()
        username_field.send_keys(test_payload)
        pause()

        if record_callback:
            record_callback("Verifying input value via DOM property...")

        # Step 3: Verify the entered value
        current_value = username_field.get_attribute("value")
        assert current_value == test_payload, (
            f"Input verification failed: Expected '{test_payload}', got '{current_value}'"
        )

        if record_callback:
            record_callback("Clearing input field and validating empty state...")

        # Step 4: Clear the field
        username_field.clear()
        pause()

        # Step 5: Verify that the field is empty
        cleared_value = username_field.get_attribute("value")
        assert cleared_value == "", f"Field not empty after clear! Found: '{cleared_value}'"

        screenshot_path = capture_screenshot(driver, "TC04", "PASS")
        return {
            "test_id": "TC04",
            "name": "Text Input (Entry, Value Verification, and Clear)",
            "status": "PASS",
            "duration": 0.0,
            "message": "Text entered, verified via DOM property, and successfully cleared.",
            "expected": f"Field accepts '{test_payload}', reflects value, and clears to ''",
            "actual": f"Entered '{current_value}', then cleared to empty string '{cleared_value}'",
            "screenshot": screenshot_path,
        }
    except Exception as e:
        screenshot_path = capture_screenshot(driver, "TC04", "FAIL") if driver else ""
        return {
            "test_id": "TC04",
            "name": "Text Input (Entry, Value Verification, and Clear)",
            "status": "FAIL",
            "duration": 0.0,
            "message": str(e),
            "expected": "Field accepts value, reflects value, and clears cleanly",
            "actual": f"Failure: {e}",
            "screenshot": screenshot_path,
        }
    finally:
        if owns_driver and driver:
            driver.quit()
