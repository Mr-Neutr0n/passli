"""
TC10 — Authentication & Session Authorization (Valid Login)
===========================================================
Test Steps:
1. Navigate to the login portal (/login/).
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
from ..driver_factory import create_chrome_driver, capture_screenshot, pause


def run_test(driver=None, record_callback=None):
    """
    Execute TC10: Full valid authentication and authenticated session verification.
    """
    owns_driver = driver is None
    if owns_driver:
        driver = create_chrome_driver()

    wait = WebDriverWait(driver, test_config.DEFAULT_WAIT_TIMEOUT)

    try:
        driver.get(f"{test_config.BASE_URL}/login/")
        pause()

        # Step 1 & 2: Fill valid credentials
        username_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, test_config.SELECTORS["login_username"]))
        )
        password_input = driver.find_element(By.CSS_SELECTOR, test_config.SELECTORS["login_password"])
        submit_btn = driver.find_element(By.CSS_SELECTOR, test_config.SELECTORS["login_submit"])

        username_input.clear()
        username_input.send_keys(test_config.TEST_USERNAME)
        password_input.clear()
        password_input.send_keys(test_config.TEST_PASSWORD)
        pause()

        # Step 3: Submit login form
        submit_btn.click()
        pause()

        # Step 4: Verify redirect to authenticated dashboard
        wait.until(EC.url_contains("/dashboard"))
        assert "/dashboard" in driver.current_url, (
            f"Expected redirect to dashboard, current URL is: {driver.current_url}"
        )

        # Step 5: Verify authenticated dashboard interface elements
        dashboard_header = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="dashboard-header"], .dashboard-title, h1'))
        )
        assert "Dashboard" in dashboard_header.text or "Personal Vault" in dashboard_header.text, (
            f"Expected dashboard heading, but found: '{dashboard_header.text}'"
        )

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
        if owns_driver and driver:
            driver.quit()
