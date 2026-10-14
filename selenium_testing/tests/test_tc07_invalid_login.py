"""
TC07 — Invalid Input / Form Submission
======================================
Test Steps:
1. Navigate to the login portal (/login/) and wait for full readiness.
2. Enter intentionally non-existent credentials (invalid_student_user, WrongPassword123!).
3. Submit the form.
4. Verify that authentication fails securely and displays the error alert box
   (data-testid="auth-error-box") with "Invalid username or password. Please try again."
5. Report PASS or FAIL.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .. import test_config
from ..driver_factory import create_chrome_driver, capture_screenshot, pause, wait_for_page_ready


def run_test(driver=None, record_callback=None):
    """
    Execute TC07: Negative authentication test with invalid credentials.
    """
    owns_driver = driver is None
    if owns_driver:
        driver = create_chrome_driver()

    wait = WebDriverWait(driver, test_config.DEFAULT_WAIT_TIMEOUT)

    try:
        if record_callback:
            record_callback("Opening login portal...")

        driver.get(f"{test_config.BASE_URL}/login/")
        wait_for_page_ready(driver, step_reporter=record_callback, step_msg="Stabilizing login page...")
        pause()

        # Step 1: Locate inputs
        username_input = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, test_config.SELECTORS["login_username"]))
        )
        password_input = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, test_config.SELECTORS["login_password"]))
        )
        submit_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, test_config.SELECTORS["login_submit"]))
        )

        fake_user = "invalid_student_qa"
        fake_pass = "DefectivePass2026!"
        if record_callback:
            record_callback(f"Entering fake invalid credentials: '{fake_user}'...")

        # Step 2: Input invalid credentials
        username_input.clear()
        username_input.send_keys(fake_user)
        password_input.clear()
        password_input.send_keys(fake_pass)
        pause()

        if record_callback:
            record_callback("Submitting invalid credentials...")

        # Step 3: Submit form
        submit_btn.click()

        if record_callback:
            record_callback("Waiting for server error response alert...")

        # Step 4: Verify authentication error alert box is displayed
        wait_for_page_ready(driver, step_reporter=record_callback)
        error_box = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, test_config.SELECTORS["auth_error_box"]))
        )
        error_text = error_box.text.strip()
        assert "Invalid username or password" in error_text, (
            f"Expected error message not found. Got: '{error_text}'"
        )
        pause()

        screenshot_path = capture_screenshot(driver, "TC07", "PASS")
        return {
            "test_id": "TC07",
            "name": "Invalid Authentication Handling",
            "status": "PASS",
            "duration": 0.0,
            "message": f"Negative auth triggered expected error alert: '{error_text}'",
            "expected": "Error alert displayed containing 'Invalid username or password'",
            "actual": f"Error alert visible with text: '{error_text}'",
            "screenshot": screenshot_path,
        }
    except Exception as e:
        screenshot_path = capture_screenshot(driver, "TC07", "FAIL") if driver else ""
        return {
            "test_id": "TC07",
            "name": "Invalid Authentication Handling",
            "status": "FAIL",
            "duration": 0.0,
            "message": str(e),
            "expected": "Error alert displayed containing 'Invalid username or password'",
            "actual": f"Error handling failure: {e}",
            "screenshot": screenshot_path,
        }
    finally:
        if owns_driver and driver:
            driver.quit()
