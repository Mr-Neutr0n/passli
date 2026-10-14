"""
TC01 — Open Website
===================
Test Steps:
1. Launch the browser.
2. Open the application.
3. Maximize the browser window.
4. Verify that the page loads successfully and the expected page element is visible.
5. Record the result.
6. Close the browser cleanly.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .. import test_config
from ..driver_factory import create_chrome_driver, capture_screenshot, pause


def run_test(driver=None, record_callback=None):
    """
    Execute TC01: Open Website and verify initial view.
    """
    owns_driver = driver is None
    if owns_driver:
        driver = create_chrome_driver()

    try:
        # Step 2: Open application
        driver.get(test_config.BASE_URL)
        pause()

        # Step 3: Maximize browser
        driver.maximize_window()
        pause()

        # Step 4: Verify expected page element is visible
        wait = WebDriverWait(driver, test_config.DEFAULT_WAIT_TIMEOUT)
        hero_title = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, test_config.SELECTORS["hero_title"]))
        )
        assert hero_title.is_displayed(), "Hero title is not displayed on the landing page."
        
        # Step 5: Capture evidence screenshot
        screenshot_path = capture_screenshot(driver, "TC01", "PASS")
        
        return {
            "test_id": "TC01",
            "name": "Open Website & Maximize Window",
            "status": "PASS",
            "duration": 0.0,
            "message": "Application loaded successfully and hero element is visible.",
            "expected": "Landing page loaded with visible hero title element",
            "actual": f"Hero title visible: '{hero_title.text[:50]}...'",
            "screenshot": screenshot_path,
        }
    except Exception as e:
        screenshot_path = capture_screenshot(driver, "TC01", "FAIL") if driver else ""
        return {
            "test_id": "TC01",
            "name": "Open Website & Maximize Window",
            "status": "FAIL",
            "duration": 0.0,
            "message": str(e),
            "expected": "Landing page loaded with visible hero title element",
            "actual": f"Error: {e}",
            "screenshot": screenshot_path,
        }
    finally:
        if owns_driver and driver:
            driver.quit()
