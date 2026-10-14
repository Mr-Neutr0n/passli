"""
TC03 — Navigation Testing
=========================
Test Steps:
1. Find a real navigation link or menu item (Sign In link).
2. Click it.
3. Verify the destination URL (/login/) and unique element on destination page.
4. Navigate backward using browser history.
5. Verify the original landing page is restored.
6. Navigate forward using browser history.
7. Verify the destination page again.
8. Refresh the page.
9. Verify that the destination still loads correctly.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .. import test_config
from ..driver_factory import create_chrome_driver, capture_screenshot, pause


def run_test(driver=None, record_callback=None):
    """
    Execute TC03: Navigation, Back/Forward Browser History, and Page Refresh.
    """
    owns_driver = driver is None
    if owns_driver:
        driver = create_chrome_driver()

    wait = WebDriverWait(driver, test_config.DEFAULT_WAIT_TIMEOUT)

    try:
        # Step 1: Open landing page
        driver.get(test_config.BASE_URL)
        pause()

        # Step 2: Find a real navigation link leading to login
        # Uses standard href locator matching both desktop and mobile layouts
        nav_links = wait.until(
            lambda d: d.find_elements(By.CSS_SELECTOR, "a[href*='/login/']")
        )
        assert len(nav_links) > 0, "No login navigation link found on landing page"
        
        target_link = nav_links[0]
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_link)
        pause()
        
        # Click link via javascript if blocked by layout or directly
        try:
            target_link.click()
        except Exception:
            driver.execute_script("arguments[0].click();", target_link)
        
        pause()

        # Step 3: Verify destination URL and unique element (Login Card)
        wait.until(EC.url_contains("/login"))
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, test_config.SELECTORS["login_card"])))
        assert "/login" in driver.current_url, f"Expected '/login' in URL, got {driver.current_url}"

        # Step 4: Navigate backward
        driver.back()
        pause()

        # Step 5: Verify original page restored
        wait.until(lambda d: "/login" not in d.current_url)
        assert "/login" not in driver.current_url, "Browser back failed to return to landing page"

        # Step 6: Navigate forward
        driver.forward()
        pause()

        # Step 7: Verify destination again
        wait.until(EC.url_contains("/login"))
        assert "/login" in driver.current_url, "Browser forward failed to reach login page"

        # Step 8: Refresh page
        driver.refresh()
        pause()

        # Step 9: Verify destination still loads correctly after refresh
        login_card = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, test_config.SELECTORS["login_card"]))
        )
        assert login_card.is_displayed(), "Login card missing after page refresh"

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
        if owns_driver and driver:
            driver.quit()
