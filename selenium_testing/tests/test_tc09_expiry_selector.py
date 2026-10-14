"""
TC09 — Expiration Timer Selection
=================================
Test Steps:
1. Navigate to the landing page sandbox.
2. Locate the expiration timer selector buttons (.expiry-btn).
3. Click a different expiration tier (e.g. '15 mins' or '2 hours').
4. Verify that the countdown telemetry card (#sim-expiry-text) reflects the selected duration.
5. Report PASS or FAIL.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .. import test_config
from ..driver_factory import create_chrome_driver, capture_screenshot, pause


def run_test(driver=None, record_callback=None):
    """
    Execute TC09: Expiration selector pill click and countdown label synchronization.
    """
    owns_driver = driver is None
    if owns_driver:
        driver = create_chrome_driver()

    wait = WebDriverWait(driver, test_config.DEFAULT_WAIT_TIMEOUT)

    try:
        driver.get(test_config.BASE_URL)
        pause()

        # Step 1: Scroll to sandbox
        sandbox = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, test_config.SELECTORS["interactive_sandbox"]))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", sandbox)
        pause()

        # Step 2: Locate expiry buttons
        expiry_btns = driver.find_elements(By.CSS_SELECTOR, test_config.SELECTORS["sim_expiry_btns"])
        assert len(expiry_btns) >= 3, f"Expected at least 3 expiration options, found {len(expiry_btns)}"

        expiry_label = driver.find_element(By.CSS_SELECTOR, test_config.SELECTORS["sim_expiry_text"])

        # Step 3: Click the '15 mins' button
        target_btn = None
        for btn in expiry_btns:
            if "15" in btn.text:
                target_btn = btn
                break
        
        assert target_btn is not None, "Target '15 mins' button not found"
        driver.execute_script("arguments[0].click();", target_btn)
        pause()

        # Step 4: Verify expiry label reflects '15 mins'
        current_expiry = expiry_label.text.strip()
        assert "15 mins" in current_expiry, (
            f"Expected expiration label '15 mins', but found '{current_expiry}'"
        )

        screenshot_path = capture_screenshot(driver, "TC09", "PASS")
        return {
            "test_id": "TC09",
            "name": "Cryptographic Expiration Timer Selection",
            "status": "PASS",
            "duration": 0.0,
            "message": f"Expiration timer switched successfully to '{current_expiry}'",
            "expected": "Telemetry card reflects selected duration ('15 mins')",
            "actual": f"Telemetry label successfully synced to '{current_expiry}'",
            "screenshot": screenshot_path,
        }
    except Exception as e:
        screenshot_path = capture_screenshot(driver, "TC09", "FAIL") if driver else ""
        return {
            "test_id": "TC09",
            "name": "Cryptographic Expiration Timer Selection",
            "status": "FAIL",
            "duration": 0.0,
            "message": str(e),
            "expected": "Telemetry card reflects selected duration ('15 mins')",
            "actual": f"Expiration test failure: {e}",
            "screenshot": screenshot_path,
        }
    finally:
        if owns_driver and driver:
            driver.quit()
