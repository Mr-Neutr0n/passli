"""
TC10 — Authentication & Session Authorization (Valid Login)
===========================================================
Test Steps:
1. Navigate to the login portal (/login/) and wait for full readiness.
2. Enter valid account credentials (qa_test_user).
3. Submit the authentication form.
4. Verify successful authentication redirect to /dashboard/.
5. Verify that authenticated user interface controls (Dashboard title and header) are rendered.
6. Report PASS or FAIL.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .. import test_config
from ..driver_factory import get_shared_driver, capture_screenshot, pause, wait_for_page_ready


def run_test(driver=None, record_callback=None):
    """
    Execute TC10: Full valid authentication and authenticated session verification.
    """
    owns_driver = driver is None
    if owns_driver:
        driver = get_shared_driver()

    wait = WebDriverWait(driver, test_config.DEFAULT_WAIT_TIMEOUT)

    try:
        if record_callback:
            record_callback("Opening login portal...")

        driver.get(f"{test_config.BASE_URL}/login/")
        wait_for_page_ready(driver, step_reporter=record_callback, step_msg="Stabilizing login page & inputs...")
        pause()

        if record_callback:
            record_callback(f"Entering credentials for '{test_config.TEST_USERNAME}'...")

        # Step 1 & 2: Fill valid credentials
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
        username_input.send_keys(test_config.TEST_USERNAME)
        password_input.clear()
        password_input.send_keys(test_config.TEST_PASSWORD)
        pause()

        if record_callback:
            record_callback("Submitting credentials and waiting for dashboard authorization...")

        # Step 3: Submit login form
        submit_btn.click()

        # Step 4: Verify redirect to authenticated dashboard and settle
        wait.until(EC.url_contains("/dashboard"))
        wait_for_page_ready(driver, step_reporter=record_callback, step_msg="Stabilizing authenticated vault dashboard...")
        assert "/dashboard" in driver.current_url, (
            f"Expected redirect to dashboard, current URL is: {driver.current_url}"
        )

        if record_callback:
            record_callback("Verifying private dashboard header and security status bar...")

        # Step 5: Verify authenticated dashboard interface elements
        dashboard_header = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="dashboard-header"], .dashboard-title, h1'))
        )
        assert "Dashboard" in dashboard_header.text or "Personal Vault" in dashboard_header.text, (
            f"Expected dashboard heading, but found: '{dashboard_header.text}'"
        )
        pause()

        screenshot_path = capture_screenshot(driver, "TC10", "PASS")
        return {
            "test_id": "TC10",
            "name": "User Authentication & Dashboard Access",
            "status": "PASS",
            "duration": 0.0,
            "message": f"Successfully authenticated user '{test_config.TEST_USERNAME}' to {driver.current_url}",
            "expected": "HTTP 302 redirect to /dashboard/ with active authenticated session controls",
            "actual": f"Landed on {driver.current_url} with header: '{dashboard_header.text.strip()}'",
            "screenshot": screenshot_path,
        }
    except Exception as e:
        screenshot_path = capture_screenshot(driver, "TC10", "FAIL") if driver else ""
        return {
            "test_id": "TC10",
            "name": "User Authentication & Dashboard Access",
            "status": "FAIL",
            "duration": 0.0,
            "message": str(e),
            "expected": "HTTP 302 redirect to /dashboard/ with active authenticated session",
            "actual": f"Authentication test failure: {e}",
            "screenshot": screenshot_path,
        }
    finally:
        if not test_config.KEEP_BROWSER_OPEN and owns_driver and driver:
            try:
                driver.quit()
            except Exception:
                pass
