"""
TC14 — Document Upload Portal & Security Form Inspection
=======================================================
Test Steps:
1. Ensure session is authenticated.
2. Navigate to /documents/upload/ and wait for page layout to settle.
3. Verify Upload Card title and 'AES-256 Envelope' security badge.
4. Locate and inspect the interactive file dropzone (#file-dropzone).
5. Locate the Document Title input (#id_title) and Classification Domain dropdown (#id_category).
6. Input mock title 'QA_Presentation_Encrypted_Audit_Record_2026' into title field.
7. Verify input value property and clear for presentation clean state.
8. Capture evidence screenshot and record result.
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
    safe_send_keys,
)


def run_test(driver=None, record_callback=None):
    """
    Execute TC14: Document upload portal form controls and security envelope.
    """
    if driver is None:
        driver = get_shared_driver()

    wait = WebDriverWait(driver, test_config.DEFAULT_WAIT_TIMEOUT)

    try:
        # Step 1: Ensure user session is authenticated
        if record_callback:
            record_callback("Verifying authenticated session for upload portal...")

        ensure_authenticated_session(driver, step_reporter=record_callback)

        # Step 2: Navigate to /documents/upload/
        if record_callback:
            record_callback("Loading Document Upload Portal (/documents/upload/)...")

        driver.get(f"{test_config.BASE_URL}/documents/upload/")
        wait_for_page_ready(driver, step_reporter=record_callback, step_msg="Stabilizing upload portal...")
        pause()

        # Step 3: Verify Upload Card & Security Badge
        if record_callback:
            record_callback("Verifying upload card and AES-256 Envelope security badge...")

        card = wait_and_scroll_to_element(
            driver,
            (By.CSS_SELECTOR, test_config.SELECTORS["upload_card"]),
        )
        assert "Upload" in card.text and "AES-256" in card.text, (
            "Upload card or AES-256 Envelope badge missing on upload page"
        )

        # Step 4: Verify File Dropzone
        if record_callback:
            record_callback("Inspecting cryptographic file dropzone (#file-dropzone)...")

        dropzone = wait_and_scroll_to_element(
            driver,
            (By.CSS_SELECTOR, test_config.SELECTORS["upload_dropzone"]),
        )
        assert dropzone.is_displayed(), "File dropzone element is not displayed"
        pause()

        # Step 5: Locate Document Title and Category fields
        if record_callback:
            record_callback("Locating document title input (#id_title) and category domain (#id_category)...")

        title_input = wait_and_scroll_to_element(
            driver,
            (By.CSS_SELECTOR, test_config.SELECTORS["upload_title"]),
        )
        category_select = driver.find_element(By.CSS_SELECTOR, test_config.SELECTORS["upload_category"])
        assert title_input.is_displayed() and category_select.is_displayed(), (
            "Metadata form fields (title, category) missing on upload page"
        )

        # Step 6: Enter mock title
        mock_title = "QA_Presentation_Encrypted_Audit_Record_2026"
        if record_callback:
            record_callback(f"Entering test document title: '{mock_title}'...")

        safe_send_keys(driver, title_input, mock_title, clear_first=True)
        pause()

        # Step 7: Verify value and clear
        if record_callback:
            record_callback("Verifying DOM value property and resetting field...")

        assert title_input.get_attribute("value") == mock_title, "Title input DOM value mismatch"
        title_input.clear()
        pause()

        screenshot_path = capture_screenshot(driver, "TC14", "PASS")
        return {
            "test_id": "TC14",
            "name": "Document Upload Portal & Security Form",
            "status": "PASS",
            "duration": 0.0,
            "message": "Successfully verified upload portal, AES-256 envelope badge, dropzone, and metadata inputs.",
            "expected": "Upload Portal with file dropzone, security badge, and metadata fields",
            "actual": f"Upload portal verified with AES-256 envelope and title/category controls",
            "screenshot": screenshot_path,
        }

    except Exception as e:
        screenshot_path = capture_screenshot(driver, "TC14", "FAIL") if driver else ""
        return {
            "test_id": "TC14",
            "name": "Document Upload Portal & Security Form",
            "status": "FAIL",
            "duration": 0.0,
            "message": str(e),
            "expected": "Upload Portal with file dropzone, security badge, and metadata fields",
            "actual": f"Encountered error: {e}",
            "screenshot": screenshot_path,
        }
    finally:
        if not test_config.KEEP_BROWSER_OPEN and driver:
            try:
                driver.quit()
            except Exception:
                pass
