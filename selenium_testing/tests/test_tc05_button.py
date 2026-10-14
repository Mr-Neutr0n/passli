"""
TC05 — Button Testing
=====================
Test Steps:
1. Locate a real interactive button (#sim-generate-btn on the landing page cryptographic sandbox).
2. Click the button.
3. Verify the actual expected application response:
   - Button text updates to indicate generation state ("Pass & Key Generated!").
   - Generated key element (#sim-key-text) receives an 8-character token matching the security pattern (XXXX-XXXX).
4. Report PASS or FAIL based on genuine behavior verification.
"""

import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .. import test_config
from ..driver_factory import create_chrome_driver, capture_screenshot, pause


def run_test(driver=None, record_callback=None):
    """
    Execute TC05: Button interaction and validation of intended dynamic behavior.
    """
    owns_driver = driver is None
    if owns_driver:
        driver = create_chrome_driver()

    wait = WebDriverWait(driver, test_config.DEFAULT_WAIT_TIMEOUT)

    try:
        driver.get(test_config.BASE_URL)
        pause()

        # Step 1: Scroll into view and locate the real button
        generate_btn = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, test_config.SELECTORS["sim_generate_btn"]))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", generate_btn)
        pause()

        key_box = driver.find_element(By.CSS_SELECTOR, test_config.SELECTORS["sim_key_text"])
        initial_key = key_box.text.strip()

        # Step 2: Click the button
        wait.until(EC.element_to_be_clickable(generate_btn))
        generate_btn.click()
        pause()

        # Step 3: Verify the actual behavioral response
        # 3a: Verify button feedback text
        btn_text = generate_btn.text
        assert "Generated" in btn_text or "Pass" in btn_text, (
            f"Expected button state update, but found '{btn_text}'"
        )

        # 3b: Verify generated cryptographic access key pattern (4 alphanumeric, hyphen, 4 alphanumeric)
        new_key = key_box.text.strip()
        pattern = r"^[2-9A-HJ-NP-Z]{4}-[2-9A-HJ-NP-Z]{4}$"
        assert re.match(pattern, new_key), (
            f"Generated key '{new_key}' did not match expected cryptographic format XXXX-XXXX"
        )

        screenshot_path = capture_screenshot(driver, "TC05", "PASS")
        return {
            "test_id": "TC05",
            "name": "Button Interaction & Cryptographic Token Generation",
            "status": "PASS",
            "duration": 0.0,
            "message": f"Button click triggered key generation successfully: {new_key}",
            "expected": "Button updates state label and generates dynamic token matching XXXX-XXXX format",
            "actual": f"Button feedback confirmed; new token '{new_key}' verified against regex pattern",
            "screenshot": screenshot_path,
        }
    except Exception as e:
        screenshot_path = capture_screenshot(driver, "TC05", "FAIL") if driver else ""
        return {
            "test_id": "TC05",
            "name": "Button Interaction & Cryptographic Token Generation",
            "status": "FAIL",
            "duration": 0.0,
            "message": str(e),
            "expected": "Button updates state label and generates dynamic token matching XXXX-XXXX format",
            "actual": f"Button execution failure: {e}",
            "screenshot": screenshot_path,
        }
    finally:
        if owns_driver and driver:
            driver.quit()
