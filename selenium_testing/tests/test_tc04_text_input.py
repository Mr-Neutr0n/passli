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
from ..driver_factory import create_chrome_driver, capture_screenshot, pause


def run_test(driver=None, record_callback=None):
    """
    Execute TC04: Text input insertion, verification, clearing, and empty validation.
    """
    owns_driver = driver is None
    if owns_driver:
        driver = create_chrome_driver()

    wait = WebDriverWait(driver, test_config.DEFAULT_WAIT_TIMEOUT)

    try:
        # Navigate to login page containing text input fields
        driver.get(f"{test_config.BASE_URL}/login/")
        pause()

        # Step 1: Locate real text input field
        username_field = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, test_config.SELECTORS["login_username"]))
        )

        # Step 2: Enter test data
        test_payload = "qa_student_automation_test"
        username_field.clear()
        username_field.send_keys(test_payload)
        pause()

        # Step 3: Verify the entered value
        current_value = username_field.get_attribute("value")
        assert current_value == test_payload, (
            f"Input verification failed: Expected '{test_payload}', got '{current_value}'"
        )

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
