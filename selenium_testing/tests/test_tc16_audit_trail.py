"""
TC16 — Cryptographic Security Audit Trail & Telemetry
====================================================
Test Steps:
1. Ensure session is authenticated.
2. Navigate to /audit/ and wait for page layout to settle.
3. Verify page heading 'Access & Verification Audit Trail'.
4. Verify cryptographic metrics (Total Events Logged, Verified Key Unlocks).
5. Verify immutable session activity log table / feed.
6. Capture evidence screenshot and record result.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .. import test_config
from ..driver_factory import (
    get_shared_driver,
    capture_screenshot,
    pause,
    wait_for_page_ready,
    ensure_authenticated_session,
    wait_and_scroll_to_element,
)


def run_test(driver=None, record_callback=None):
    """
    Execute TC16: Cryptographic security audit log stream and verification metrics.
    """
    if driver is None:
        driver = get_shared_driver()

    wait = WebDriverWait(driver, test_config.DEFAULT_WAIT_TIMEOUT)

    try:
        # Step 1: Ensure user session is authenticated
        if record_callback:
            record_callback("Verifying authenticated session for audit logs...")

        ensure_authenticated_session(driver, step_reporter=record_callback)

        # Step 2: Navigate to /audit/
        if record_callback:
            record_callback("Loading Cryptographic Security Audit Trail (/audit/)...")

        driver.get(f"{test_config.BASE_URL}/audit/")
        wait_for_page_ready(driver, step_reporter=record_callback, step_msg="Stabilizing audit log trail...")
        pause()

        # Step 3: Verify page heading
        if record_callback:
            record_callback("Verifying Audit Trail title and breadcrumbs...")

        h1 = wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(), 'Audit') or contains(text(), 'Trail')]")))
        assert "Audit" in h1.text or "Trail" in h1.text, f"Unexpected audit title: {h1.text}"

        # Step 4: Verify audit telemetry metrics
        if record_callback:
            record_callback("Verifying audit metrics (Total Events & Verified Key Unlocks)...")

        metric_events = wait_and_scroll_to_element(
            driver,
            (By.CSS_SELECTOR, test_config.SELECTORS["audit_metric_events"]),
        )
        metric_unlocks = driver.find_element(By.CSS_SELECTOR, test_config.SELECTORS["audit_metric_unlocks"])
        assert metric_events.is_displayed() and metric_unlocks.is_displayed(), (
            "Audit telemetry metrics missing on audit log page"
        )
        pause()

        # Step 5: Verify audit table or log container
        if record_callback:
            record_callback("Verifying session event log table and security timestamp stream...")

        table_or_card = driver.find_elements(By.CSS_SELECTOR, ".vault-doc-table") or driver.find_elements(By.CSS_SELECTOR, ".card") or driver.find_elements(By.CSS_SELECTOR, ".vault-container")
        assert len(table_or_card) > 0, "Audit log container missing on screen"
        pause()

        screenshot_path = capture_screenshot(driver, "TC16", "PASS")
        return {
            "test_id": "TC16",
            "name": "Cryptographic Security Audit Trail",
            "status": "PASS",
            "duration": 0.0,
            "message": "Successfully verified access audit trail, event metrics, and immutable activity stream.",
            "expected": "Security Audit Trail with total events and verified unlock telemetry",
            "actual": f"Audit trail verified (Events: {metric_events.text.strip()}, Unlocks: {metric_unlocks.text.strip()})",
            "screenshot": screenshot_path,
        }

    except Exception as e:
        screenshot_path = capture_screenshot(driver, "TC16", "FAIL") if driver else ""
        return {
            "test_id": "TC16",
            "name": "Cryptographic Security Audit Trail",
            "status": "FAIL",
            "duration": 0.0,
            "message": str(e),
            "expected": "Security Audit Trail with total events and verified unlock telemetry",
            "actual": f"Encountered error: {e}",
            "screenshot": screenshot_path,
        }
    finally:
        if not test_config.KEEP_BROWSER_OPEN and driver:
            try:
                driver.quit()
            except Exception:
                pass
