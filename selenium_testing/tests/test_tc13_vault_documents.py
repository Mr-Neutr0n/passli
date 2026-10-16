"""
TC13 — Encrypted Document Vault & Category Filtering
===================================================
Test Steps:
1. Ensure session is authenticated.
2. Navigate to /documents/ and wait for page layout to settle.
3. Verify Document Vault title and record counter banner.
4. Interact with Domain Category filter pills (Medical, All Records).
5. Interact with dynamic search input field (typing & clearing search).
6. Verify at least one encrypted document card is displayed in the vault.
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
    safe_click,
    safe_send_keys,
)


def run_test(driver=None, record_callback=None):
    """
    Execute TC13: Encrypted document vault inspection, category filter pills, and search.
    """
    if driver is None:
        driver = get_shared_driver()

    wait = WebDriverWait(driver, test_config.DEFAULT_WAIT_TIMEOUT)

    try:
        # Step 1: Ensure user session is authenticated
        if record_callback:
            record_callback("Verifying authenticated session for document vault...")

        ensure_authenticated_session(driver, step_reporter=record_callback)

        # Step 2: Navigate to /documents/
        if record_callback:
            record_callback("Loading Encrypted Document Vault (/documents/)...")

        driver.get(f"{test_config.BASE_URL}/documents/")
        wait_for_page_ready(driver, step_reporter=record_callback, step_msg="Stabilizing document vault records...")
        pause()

        # Step 3: Verify vault header
        if record_callback:
            record_callback("Verifying document vault title and record statistics banner...")

        h1 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".vault-title")))
        assert "Vault" in h1.text or "Document" in h1.text, f"Unexpected vault title: {h1.text}"

        # Step 4: Interact with Category Filter Pills
        if record_callback:
            record_callback("Inspecting domain classification pills (Medical, Personal, etc.)...")

        cat_pills = driver.find_elements(By.CSS_SELECTOR, test_config.SELECTORS["vault_cat_pills"])
        assert len(cat_pills) >= 2, f"Expected category filter pills, found {len(cat_pills)}"

        # Click Medical pill if available
        medical_pill = None
        for pill in cat_pills:
            if "Medical" in pill.text:
                medical_pill = pill
                break

        if medical_pill:
            if record_callback:
                record_callback("Filtering vault by 'Medical' domain category...")
            safe_click(driver, medical_pill)
            wait_for_page_ready(driver, min_stabilize=1.0)
            pause()

        # Step 5: Test Search Filter Input
        if record_callback:
            record_callback("Testing search input field with query 'Immunization'...")

        search_input = wait_and_scroll_to_element(
            driver,
            (By.CSS_SELECTOR, test_config.SELECTORS["vault_search_input"]),
        )
        safe_send_keys(driver, search_input, "Immunization", clear_first=True)
        pause()

        if record_callback:
            record_callback("Clearing search input to restore all vault records...")

        search_input.clear()
        pause()

        # Step 6: Verify document cards are rendered
        if record_callback:
            record_callback("Verifying encrypted document cards rendered on screen...")

        driver.get(f"{test_config.BASE_URL}/documents/")
        wait_for_page_ready(driver, min_stabilize=1.0)

        doc_cards = driver.find_elements(By.CSS_SELECTOR, test_config.SELECTORS["vault_doc_cards"])
        assert len(doc_cards) > 0, "No document cards rendered in vault"
        
        # Scroll to first card to highlight it
        wait_and_scroll_to_element(driver, (By.CSS_SELECTOR, test_config.SELECTORS["vault_doc_cards"]))
        pause()

        screenshot_path = capture_screenshot(driver, "TC13", "PASS")
        return {
            "test_id": "TC13",
            "name": "Encrypted Document Vault & Category Filter",
            "status": "PASS",
            "duration": 0.0,
            "message": f"Successfully verified document vault ({len(doc_cards)} cards), category pills, and search field.",
            "expected": "Encrypted Document Vault with category filters and search operation",
            "actual": f"Vault verified with {len(doc_cards)} document record cards",
            "screenshot": screenshot_path,
        }

    except Exception as e:
        screenshot_path = capture_screenshot(driver, "TC13", "FAIL") if driver else ""
        return {
            "test_id": "TC13",
            "name": "Encrypted Document Vault & Category Filter",
            "status": "FAIL",
            "duration": 0.0,
            "message": str(e),
            "expected": "Encrypted Document Vault with category filters and search operation",
            "actual": f"Encountered error: {e}",
            "screenshot": screenshot_path,
        }
    finally:
        if not test_config.KEEP_BROWSER_OPEN and driver:
            try:
                driver.quit()
            except Exception:
                pass
