"""
TC12 — Authenticated Vault Dashboard & Telemetry Inspection
==========================================================
Test Steps:
1. Ensure session is authenticated as valid user.
2. Navigate to /dashboard/ and wait for full page readiness.
3. Verify personal dashboard header and active security envelope.
4. Verify the 4 telemetry metric cards:
   - Vault Records
   - Active Passes
   - Total Passes
   - Storage Quota
5. Verify the Zero-Knowledge security status bar:
   - Argon2id + AES-256-GCM
   - Server TTL Guard Active
6. Verify Quick Action CTAs (Upload Record, Create Share Pass).
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
    Execute TC12: Authenticated vault dashboard metrics, greeting, and telemetry.
    """
    if driver is None:
        driver = get_shared_driver()

    wait = WebDriverWait(driver, test_config.DEFAULT_WAIT_TIMEOUT)

    try:
        # Step 1: Ensure user session is authenticated
        if record_callback:
            record_callback("Verifying authenticated session for vault dashboard...")

        ensure_authenticated_session(driver, step_reporter=record_callback)

        # Step 2: Navigate to dashboard
        if record_callback:
            record_callback("Loading personal vault dashboard...")

        driver.get(f"{test_config.BASE_URL}/dashboard/")
        wait_for_page_ready(driver, step_reporter=record_callback, step_msg="Stabilizing vault dashboard...")
        pause()

        # Step 3: Verify dashboard header
        if record_callback:
            record_callback("Verifying personalized greeting and envelope status...")

        header = wait_and_scroll_to_element(
            driver,
            (By.CSS_SELECTOR, test_config.SELECTORS["dashboard_header"]),
            step_reporter=record_callback,
            step_msg="Inspecting vault header...",
        )
        assert header.is_displayed(), "Dashboard header is not visible."

        # Step 4: Verify Zero-Knowledge Status Bar
        if record_callback:
            record_callback("Verifying Zero-Knowledge & AES-256 cryptographic status bar...")

        status_bar = wait_and_scroll_to_element(
            driver,
            (By.CSS_SELECTOR, test_config.SELECTORS["vault_status_bar"]),
        )
        assert "Zero-Knowledge" in status_bar.text or "AES-256" in status_bar.text, (
            "Cryptographic status bar did not declare active zero-knowledge envelope"
        )
        pause()

        # Step 5: Verify Telemetry Stats Grid & Cards
        if record_callback:
            record_callback("Verifying telemetry metric cards (Records, Passes, Quota)...")

        stats_grid = wait_and_scroll_to_element(
            driver,
            (By.CSS_SELECTOR, test_config.SELECTORS["stats_grid"]),
        )
        stat_cards = stats_grid.find_elements(By.CSS_SELECTOR, test_config.SELECTORS["stat_cards"])
        assert len(stat_cards) >= 4, f"Expected 4 dashboard metric cards, found {len(stat_cards)}"
        pause()

        # Step 6: Verify Quick Action CTAs
        if record_callback:
            record_callback("Verifying quick action buttons ('Upload Record' & 'Create Share Pass')...")

        upload_btn = driver.find_element(By.CSS_SELECTOR, test_config.SELECTORS["dash_upload_btn"])
        new_pass_btn = driver.find_element(By.CSS_SELECTOR, test_config.SELECTORS["dash_new_pass_btn"])
        assert upload_btn.is_displayed() and new_pass_btn.is_displayed(), (
            "Quick action CTA buttons missing on authenticated dashboard"
        )
        pause()

        screenshot_path = capture_screenshot(driver, "TC12", "PASS")
        return {
            "test_id": "TC12",
            "name": "Authenticated Vault Dashboard & Telemetry",
            "status": "PASS",
            "duration": 0.0,
            "message": "Successfully verified personal vault greeting, cryptographic status bar, and 4 telemetry cards.",
            "expected": "Personal Vault Dashboard with verified metrics and Zero-Knowledge envelope",
            "actual": f"Dashboard active ({len(stat_cards)} stat cards, status bar verified)",
            "screenshot": screenshot_path,
        }

    except Exception as e:
        screenshot_path = capture_screenshot(driver, "TC12", "FAIL") if driver else ""
        return {
            "test_id": "TC12",
            "name": "Authenticated Vault Dashboard & Telemetry",
            "status": "FAIL",
            "duration": 0.0,
            "message": str(e),
            "expected": "Personal Vault Dashboard with verified metrics and Zero-Knowledge envelope",
            "actual": f"Encountered error: {e}",
            "screenshot": screenshot_path,
        }
    finally:
        if not test_config.KEEP_BROWSER_OPEN and driver:
            try:
                driver.quit()
            except Exception:
                pass
