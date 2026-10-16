"""
TC03 — Navigation Testing
=========================
Test Steps:
1. Open landing page and wait for full readiness.
2. Find navigation link (Sign In) and click it.
3. Verify destination URL (/login/) and unique element on destination page.
4. Navigate backward using browser history.
5. Verify original landing page is restored.
6. Navigate forward using browser history.
7. Verify destination page again.
8. Refresh page and verify stability.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .. import test_config
from ..driver_factory import get_shared_driver, capture_screenshot, pause, wait_for_page_ready


def run_test(driver=None, record_callback=None):
    """
    Execute TC03: Navigation, Back/Forward Browser History, and Page Refresh.
    """
    owns_driver = driver is None
    if owns_driver:
        driver = get_shared_driver()

    wait = WebDriverWait(driver, test_config.DEFAULT_WAIT_TIMEOUT)

    try:
        if record_callback:
            record_callback("Loading landing page...")

        # Step 1: Open landing page and settle
        driver.get(test_config.BASE_URL)
        wait_for_page_ready(driver, step_reporter=record_callback, step_msg="Stabilizing initial landing page...")
        pause()

        if record_callback:
            record_callback("Locating navigation link to login portal...")

        # Step 2: Find a real navigation link leading to login
        nav_links = wait.until(
            lambda d: d.find_elements(By.CSS_SELECTOR, "a[href*='/login/']")
        )
        assert len(nav_links) > 0, "No login navigation link found on landing page"
        
        target_link = nav_links[0]
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_link)
        pause()
        
        if record_callback:
            record_callback("Clicking Sign In navigation link...")

        try:
            target_link.click()
        except Exception:
            driver.execute_script("arguments[0].click();", target_link)
        
        # Step 3: Verify destination URL and unique element (Login Card)
        wait_for_page_ready(driver, step_reporter=record_callback, step_msg="Waiting for destination page (/login/) to load...")
        wait.until(EC.url_contains("/login"))
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, test_config.SELECTORS["login_card"])))
        assert "/login" in driver.current_url, f"Expected '/login' in URL, got {driver.current_url}"
        pause()

        if record_callback:
            record_callback("Testing browser history: navigating backward...")

        # Step 4: Navigate backward
        driver.back()
        wait_for_page_ready(driver, step_reporter=record_callback, step_msg="Waiting for home page to restore after back navigation...")
        wait.until(lambda d: "/login" not in d.current_url)
        assert "/login" not in driver.current_url, "Browser back failed to return to landing page"
        pause()

        if record_callback:
            record_callback("Testing browser history: navigating forward...")

        # Step 6: Navigate forward
        driver.forward()
        wait_for_page_ready(driver, step_reporter=record_callback, step_msg="Waiting for destination to restore after forward navigation...")
        wait.until(EC.url_contains("/login"))
        assert "/login" in driver.current_url, "Browser forward failed to reach login page"
        pause()

        if record_callback:
            record_callback("Testing browser refresh and persistence...")

        # Step 8: Refresh page
        driver.refresh()
        wait_for_page_ready(driver, step_reporter=record_callback, step_msg="Stabilizing page after browser refresh...")

        # Step 9: Verify destination still loads correctly after refresh
        login_card = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, test_config.SELECTORS["login_card"]))
        )
        assert login_card.is_displayed(), "Login card missing after page refresh"
        pause()

        screenshot_path = capture_screenshot(driver, "TC03", "PASS")
        return {
            "test_id": "TC03",
            "name": "Navigation, History (Back/Forward), and Refresh",
            "status": "PASS",
            "duration": 0.0,
            "message": "Successfully verified navigation link, back/forward history, and page refresh.",
            "expected": "Seamless page transition, history navigation, and persistence on refresh",
            "actual": f"Destination verified: {driver.current_url}",
            "screenshot": screenshot_path,
        }
    except Exception as e:
        screenshot_path = capture_screenshot(driver, "TC03", "FAIL") if driver else ""
        return {
            "test_id": "TC03",
            "name": "Navigation, History (Back/Forward), and Refresh",
            "status": "FAIL",
            "duration": 0.0,
            "message": str(e),
            "expected": "Seamless page transition, history navigation, and persistence on refresh",
            "actual": f"Navigation failure: {e}",
            "screenshot": screenshot_path,
        }
    finally:
        if not test_config.KEEP_BROWSER_OPEN and owns_driver and driver:
            try:
                driver.quit()
            except Exception:
                pass
