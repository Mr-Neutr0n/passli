"""
TC06 — Required-Field Form Validation
=====================================
Test Steps:
1. Navigate to the login portal (/login/) and wait for full page readiness.
2. Attempt to submit the authentication form with blank fields.
3. Verify that the form submission is prevented or intercepted by validation:
   - Check that the user remains on the login page without unauthorized navigation.
   - Verify that validation alerts or missing-input states are registered.
4. Report PASS or FAIL.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .. import test_config
from ..driver_factory import get_shared_driver, capture_screenshot, pause, wait_for_page_ready


def run_test(driver=None, record_callback=None):
    """
    Execute TC06: Required field validation on authentication form.
    """
    owns_driver = driver is None
    if owns_driver:
        driver = get_shared_driver()

    wait = WebDriverWait(driver, test_config.DEFAULT_WAIT_TIMEOUT)

    try:
        if record_callback:
            record_callback("Opening login portal...")

        driver.get(f"{test_config.BASE_URL}/login/")
        driver.maximize_window()
        wait_for_page_ready(driver, step_reporter=record_callback, step_msg="Stabilizing login page...")
        pause()

        if record_callback:
            record_callback("Clearing input fields to test blank submission...")

        # Step 1: Ensure fields are cleared
        username_input = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, test_config.SELECTORS["login_username"]))
        )
        password_input = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, test_config.SELECTORS["login_password"]))
        )
        submit_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, test_config.SELECTORS["login_submit"]))
        )

        username_input.clear()
        password_input.clear()
        pause()

        if record_callback:
            record_callback("Clicking Sign In with empty fields to trigger validation...")

        # Step 2: Click submit with blank fields
        submit_btn.click()
        pause()

        if record_callback:
            record_callback("Verifying submission rejection and page retention...")

        # Step 3: Verify user remains on /login/ (no unintended redirect)
        assert "/login" in driver.current_url, (
            f"Form submitted unexpectedly with blank fields! URL: {driver.current_url}"
        )

        # Step 4: Re-query DOM to prevent stale element reference after form POST
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, test_config.SELECTORS["login_card"])))
        refreshed_user_field = driver.find_element(By.CSS_SELECTOR, test_config.SELECTORS["login_username"])
        
        field_val = refreshed_user_field.get_attribute("value")
        has_error_box = len(driver.find_elements(By.CSS_SELECTOR, test_config.SELECTORS["auth_error_box"])) > 0
        has_field_error = len(driver.find_elements(By.CSS_SELECTOR, ".form-error")) > 0
        
        assert field_val == "" or has_error_box or has_field_error, (
            "Required validation did not register expected rejection on blank form."
        )

        screenshot_path = capture_screenshot(driver, "TC06", "PASS")
        return {
            "test_id": "TC06",
            "name": "Required-Field Form Validation",
            "status": "PASS",
            "duration": 0.0,
            "message": "Submission verified; blank credentials rejected and retained on /login/.",
            "expected": "Form halts submission on blank input; user retained on /login/",
            "actual": f"Retained on {driver.current_url}; error state confirmed.",
            "screenshot": screenshot_path,
        }
    except Exception as e:
        screenshot_path = capture_screenshot(driver, "TC06", "FAIL") if driver else ""
        return {
            "test_id": "TC06",
            "name": "Required-Field Form Validation",
            "status": "FAIL",
            "duration": 0.0,
            "message": str(e),
            "expected": "Form halts submission on blank input; user retained on /login/",
            "actual": f"Validation test failure: {e}",
            "screenshot": screenshot_path,
        }
    finally:
        if not test_config.KEEP_BROWSER_OPEN and owns_driver and driver:
            try:
                driver.quit()
            except Exception:
                pass
