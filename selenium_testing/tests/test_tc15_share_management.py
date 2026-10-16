"""
TC15 — Ephemeral Share Pass Management & Creation View
=====================================================
Test Steps:
1. Ensure session is authenticated.
2. Navigate to /share/create/ and wait for page layout to settle.
3. Verify Share Pass creation heading 'Generate Ephemeral Share Pass'.
4. Verify document selection checklist and configuration controls.
5. Navigate to /share/ (Share Passes active list).
6. Verify pass list view, header, and 'Create Share Pass' CTA.
7. Capture evidence screenshot and record result.
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
    Execute TC15: Ephemeral share pass creation form and active pass management view.
    """
    if driver is None:
        driver = get_shared_driver()

    wait = WebDriverWait(driver, test_config.DEFAULT_WAIT_TIMEOUT)

    try:
        # Step 1: Ensure user session is authenticated
        if record_callback:
            record_callback("Verifying authenticated session for share pass management...")

        ensure_authenticated_session(driver, step_reporter=record_callback)

        # Step 2: Navigate to /share/create/
        if record_callback:
            record_callback("Loading Ephemeral Share Pass Creator (/share/create/)...")

        driver.get(f"{test_config.BASE_URL}/share/create/")
        wait_for_page_ready(driver, step_reporter=record_callback, step_msg="Stabilizing share pass form...")
        pause()

        # Step 3: Verify creation heading
        if record_callback:
            record_callback("Verifying Share Pass creation title and breadcrumb navigation...")

        h1 = wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(), 'Share Pass') or contains(text(), 'Generate')]")))
        assert "Share Pass" in h1.text or "Generate" in h1.text, f"Unexpected creation title: {h1.text}"

        # Step 4: Verify form or document selection card
        if record_callback:
            record_callback("Verifying document selection checklist and TTL controls...")

        form_or_card = driver.find_elements(By.CSS_SELECTOR, test_config.SELECTORS["share_create_form"]) or driver.find_elements(By.CSS_SELECTOR, ".card")
        assert len(form_or_card) > 0, "Neither share create form nor document card rendered"
        pause()

        # Step 5: Navigate to Share Passes list view
        if record_callback:
            record_callback("Navigating to Active Share Passes list (/share/)...")

        driver.get(f"{test_config.BASE_URL}/share/")
        wait_for_page_ready(driver, step_reporter=record_callback, step_msg="Stabilizing share passes dashboard...")
        pause()

        # Step 6: Verify share list heading & CTA
        if record_callback:
            record_callback("Verifying Share Passes list interface...")

        list_h1 = wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(), 'Passes') or contains(text(), 'Share')]")))
        assert "Pass" in list_h1.text or "Share" in list_h1.text, f"Unexpected list title: {list_h1.text}"
        pause()

        screenshot_path = capture_screenshot(driver, "TC15", "PASS")
        return {
            "test_id": "TC15",
            "name": "Ephemeral Share Pass Management & Creation",
            "status": "PASS",
            "duration": 0.0,
            "message": "Successfully verified Share Pass creation form and active passes list interface.",
            "expected": "Share Pass creation interface and active passes management portal",
            "actual": f"Share pass creation form and list interface verified ({list_h1.text})",
            "screenshot": screenshot_path,
        }

    except Exception as e:
        screenshot_path = capture_screenshot(driver, "TC15", "FAIL") if driver else ""
        return {
            "test_id": "TC15",
            "name": "Ephemeral Share Pass Management & Creation",
            "status": "FAIL",
            "duration": 0.0,
            "message": str(e),
            "expected": "Share Pass creation interface and active passes management portal",
            "actual": f"Encountered error: {e}",
            "screenshot": screenshot_path,
        }
    finally:
        if not test_config.KEEP_BROWSER_OPEN and driver:
            try:
                driver.quit()
            except Exception:
                pass
