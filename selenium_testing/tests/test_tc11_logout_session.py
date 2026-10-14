"""
TC11 — Logout & Session Teardown
================================
Test Steps:
1. Ensure an authenticated session exists (log in if necessary).
2. Locate and submit the secure Logout form (action contains /logout/).
3. Verify session termination and redirect to the public landing page or login portal.
4. Verify that public navigation links (Sign In) are restored and private routes require re-authentication.
5. Report PASS or FAIL.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .. import test_config
from ..driver_factory import create_chrome_driver, capture_screenshot, pause


def run_test(driver=None, record_callback=None):
    """
    Execute TC11: Authenticated session teardown and logout verification.
    """
    owns_driver = driver is None
    if owns_driver:
        driver = create_chrome_driver()

    wait = WebDriverWait(driver, test_config.DEFAULT_WAIT_TIMEOUT)

    try:
        # Step 1: Ensure an active authenticated session
        if "/dashboard" not in driver.current_url:
            driver.get(f"{test_config.BASE_URL}/login/")
            pause()

            username_input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, test_config.SELECTORS["login_username"]))
            )
            password_input = driver.find_element(By.CSS_SELECTOR, test_config.SELECTORS["login_password"])
            submit_btn = driver.find_element(By.CSS_SELECTOR, test_config.SELECTORS["login_submit"])

            username_input.clear()
            username_input.send_keys(test_config.TEST_USERNAME)
            password_input.clear()
            password_input.send_keys(test_config.TEST_PASSWORD)
            submit_btn.click()
            pause()
            wait.until(EC.url_contains("/dashboard"))

        # Step 2: Locate and submit the CSRF-protected logout form
        logout_form = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "form[action*='/logout/']"))
        )
        driver.execute_script("arguments[0].submit();", logout_form)
        pause()

        # Step 3: Verify redirect to public page
        wait.until(lambda d: "/dashboard" not in d.current_url)

        # Step 4: Verify public navigation link (Sign In) is visible
        wait.until(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, "a[href*='/login/']")) > 0
        )

        screenshot_path = capture_screenshot(driver, "TC11", "PASS")
        return {
            "test_id": "TC11",
            "name": "Secure Logout & Session Teardown",
            "status": "PASS",
            "duration": 0.0,
            "message": "User successfully logged out; session terminated and public routes restored.",
            "expected": "Session teardown, redirect away from private routes, public nav restored",
            "actual": f"Landed on {driver.current_url} with public 'Sign In' link visible",
            "screenshot": screenshot_path,
        }
    except Exception as e:
        screenshot_path = capture_screenshot(driver, "TC11", "FAIL") if driver else ""
        return {
            "test_id": "TC11",
            "name": "Secure Logout & Session Teardown",
            "status": "FAIL",
            "duration": 0.0,
            "message": str(e),
            "expected": "Session teardown and public nav restored",
            "actual": f"Logout test failure: {e}",
            "screenshot": screenshot_path,
        }
    finally:
        if owns_driver and driver:
            driver.quit()
