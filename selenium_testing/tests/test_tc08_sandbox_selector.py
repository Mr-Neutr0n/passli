"""
TC08 — Interactive Sandbox Document Selector
============================================
Test Steps:
1. Navigate to the landing page and wait for full page readiness.
2. Scroll to the cryptographic sandbox.
3. Locate the document selector checkboxes (.sim-doc-checkbox).
4. Toggle a document checkbox to modify the selection.
5. Verify that the dynamic document counter (#sim-selected-count) instantly recalculates
   both the selected item count and the cumulative file size (e.g. "1 selected (2.4 MB)").
6. Report PASS or FAIL.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .. import test_config
from ..driver_factory import get_shared_driver, capture_screenshot, pause, wait_for_page_ready


def run_test(driver=None, record_callback=None):
    """
    Execute TC08: Interactive sandbox document checkbox state and telemetry recalculation.
    """
    owns_driver = driver is None
    if owns_driver:
        driver = get_shared_driver()

    wait = WebDriverWait(driver, test_config.DEFAULT_WAIT_TIMEOUT)

    try:
        if record_callback:
            record_callback("Opening landing page...")

        driver.get(test_config.BASE_URL)
        wait_for_page_ready(driver, step_reporter=record_callback, step_msg="Stabilizing landing page & sandbox simulator...")
        pause()

        if record_callback:
            record_callback("Scrolling to interactive document sandbox...")

        # Step 1: Scroll to sandbox and ensure visibility
        sandbox = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, test_config.SELECTORS["interactive_sandbox"]))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest', behavior: 'smooth'});", sandbox)
        pause()

        # Step 2: Locate checkboxes
        checkboxes = driver.find_elements(By.CSS_SELECTOR, test_config.SELECTORS["sim_checkboxes"])
        assert len(checkboxes) >= 2, f"Expected at least 2 simulator checkboxes, found {len(checkboxes)}"

        count_badge = driver.find_element(By.CSS_SELECTOR, test_config.SELECTORS["sim_selected_count"])
        initial_text = count_badge.text.strip()

        if record_callback:
            record_callback(f"Toggling document selection checkbox (current: '{initial_text}')...")

        # Step 3: Toggle the second checkbox (uncheck)
        second_cb = checkboxes[1]
        driver.execute_script("arguments[0].click();", second_cb)
        pause()

        if record_callback:
            record_callback("Verifying real-time file size & count recalculation...")

        # Step 4: Verify dynamic calculation
        updated_text = count_badge.text.strip()
        assert updated_text != initial_text, (
            f"Badge failed to update dynamically. Remained: '{initial_text}'"
        )
        assert "1 selected" in updated_text and "2.4 MB" in updated_text, (
            f"Expected '1 selected (2.4 MB)', got '{updated_text}'"
        )

        screenshot_path = capture_screenshot(driver, "TC08", "PASS")
        return {
            "test_id": "TC08",
            "name": "Sandbox Document Selector & Dynamic Recalculation",
            "status": "PASS",
            "duration": 0.0,
            "message": f"Selection updated from '{initial_text}' to '{updated_text}'",
            "expected": "Dynamic recalculation of count and cumulative file size upon checkbox toggle",
            "actual": f"Recalculated successfully to '{updated_text}'",
            "screenshot": screenshot_path,
        }
    except Exception as e:
        screenshot_path = capture_screenshot(driver, "TC08", "FAIL") if driver else ""
        return {
            "test_id": "TC08",
            "name": "Sandbox Document Selector & Dynamic Recalculation",
            "status": "FAIL",
            "duration": 0.0,
            "message": str(e),
            "expected": "Dynamic recalculation of count and cumulative file size",
            "actual": f"Selector test failure: {e}",
            "screenshot": screenshot_path,
        }
    finally:
        if not test_config.KEEP_BROWSER_OPEN and owns_driver and driver:
            try:
                driver.quit()
            except Exception:
                pass
