"""
Controlled Negative Demonstrations (Deliberate Selenium Failures)
=================================================================
IMPORTANT NOTE FOR EVALUATION / UNIVERSITY VIDEO DEMONSTRATION:
These test cases are DELIBERATELY DESIGNED TO FAIL under controlled conditions.
They demonstrate how Selenium WebDriver assertions, timeouts, and exception handlers
intercept mismatches and missing elements without crashing the test runner or dashboard.

Do NOT confuse these controlled demonstration tests with real application bugs.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from .. import test_config
from ..driver_factory import create_chrome_driver, capture_screenshot, pause


def run_demo_fail_01(driver=None, record_callback=None):
    """
    DEMO_FAIL_01 — Intentional Title Mismatch Demonstration
    Purpose: Demonstrates assertion failure when page title does not match an incorrect expectation.
    """
    owns_driver = driver is None
    if owns_driver:
        driver = create_chrome_driver()

    try:
        driver.get(test_config.BASE_URL)
        pause()

        actual_title = driver.title.strip()
        deliberate_wrong_title = "University Grading Portal 2026 — Secure Student Gateway"

        # Deliberate assertion failure
        assert actual_title == deliberate_wrong_title, (
            f"[INTENTIONAL DEMO FAILURE] Title mismatch detected by Selenium! "
            f"Expected: '{deliberate_wrong_title}', Actual: '{actual_title}'"
        )

        return {
            "test_id": "DEMO_FAIL_01",
            "name": "[DEMO FAIL] Deliberate Title Mismatch",
            "status": "PASS",  # Would only happen if title magically matched
            "duration": 0.0,
            "message": "Unexpected pass: title matched artificial string",
            "expected": deliberate_wrong_title,
            "actual": actual_title,
            "screenshot": "",
            "is_demo_failure": True,
        }
    except AssertionError as e:
        screenshot_path = capture_screenshot(driver, "DEMO_FAIL_01", "FAIL") if driver else ""
        return {
            "test_id": "DEMO_FAIL_01",
            "name": "[DEMO FAIL] Deliberate Title Mismatch",
            "status": "FAIL",
            "duration": 0.0,
            "message": str(e),
            "expected": "Deliberately incorrect title: 'University Grading Portal 2026 — Secure Student Gateway'",
            "actual": f"Selenium intercepted title mismatch: '{driver.title}'",
            "screenshot": screenshot_path,
            "is_demo_failure": True,
        }
    finally:
        if owns_driver and driver:
            driver.quit()


def run_demo_fail_02(driver=None, record_callback=None):
    """
    DEMO_FAIL_02 — Deliberately Nonexistent Element Demonstration
    Purpose: Demonstrates explicit wait TimeoutException when seeking an element that does not exist.
    """
    owns_driver = driver is None
    if owns_driver:
        driver = create_chrome_driver()

    try:
        driver.get(test_config.BASE_URL)
        pause()

        ghost_selector = "#deliberately-missing-ghost-element-xyz-999"
        
        # Use short timeout (3.0s) so video demo runs swiftly
        short_wait = WebDriverWait(driver, test_config.SHORT_WAIT_TIMEOUT)
        
        short_wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ghost_selector))
        )

        return {
            "test_id": "DEMO_FAIL_02",
            "name": "[DEMO FAIL] Deliberately Missing Element",
            "status": "PASS",
            "duration": 0.0,
            "message": "Unexpected pass: ghost element was found",
            "expected": f"Presence of ghost element '{ghost_selector}'",
            "actual": "Ghost element located",
            "screenshot": "",
            "is_demo_failure": True,
        }
    except TimeoutException as e:
        screenshot_path = capture_screenshot(driver, "DEMO_FAIL_02", "FAIL") if driver else ""
        return {
            "test_id": "DEMO_FAIL_02",
            "name": "[DEMO FAIL] Deliberately Missing Element",
            "status": "FAIL",
            "duration": 0.0,
            "message": f"[INTENTIONAL DEMO FAILURE] WebDriverWait timed out after {test_config.SHORT_WAIT_TIMEOUT}s waiting for nonexistent element '{ghost_selector}'.",
            "expected": f"Element '{ghost_selector}' visible within {test_config.SHORT_WAIT_TIMEOUT}s",
            "actual": f"Selenium TimeoutException triggered cleanly as expected.",
            "screenshot": screenshot_path,
            "is_demo_failure": True,
        }
    finally:
        if owns_driver and driver:
            driver.quit()


def run_demo_fail_03(driver=None, record_callback=None):
    """
    DEMO_FAIL_03 — Deliberate Text Content Mismatch Demonstration
    Purpose: Demonstrates assertion failure when element inner text differs from expected marketing copy.
    """
    owns_driver = driver is None
    if owns_driver:
        driver = create_chrome_driver()

    try:
        driver.get(test_config.BASE_URL)
        pause()

        wait = WebDriverWait(driver, test_config.DEFAULT_WAIT_TIMEOUT)
        hero_title = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, test_config.SELECTORS["hero_title"]))
        )

        actual_text = hero_title.text.strip()
        deliberate_incorrect_text = "Welcome to the Legacy Plaintext Banking Portal"

        # Deliberate assertion failure
        assert deliberate_incorrect_text in actual_text, (
            f"[INTENTIONAL DEMO FAILURE] Content assertion failed! "
            f"Expected string '{deliberate_incorrect_text}' not in actual text '{actual_text[:60]}...'"
        )

        return {
            "test_id": "DEMO_FAIL_03",
            "name": "[DEMO FAIL] Deliberate Content Mismatch",
            "status": "PASS",
            "duration": 0.0,
            "message": "Unexpected pass: text matched artificial string",
            "expected": deliberate_incorrect_text,
            "actual": actual_text,
            "screenshot": "",
            "is_demo_failure": True,
        }
    except AssertionError as e:
        screenshot_path = capture_screenshot(driver, "DEMO_FAIL_03", "FAIL") if driver else ""
        return {
            "test_id": "DEMO_FAIL_03",
            "name": "[DEMO FAIL] Deliberate Content Mismatch",
            "status": "FAIL",
            "duration": 0.0,
            "message": str(e),
            "expected": f"Hero title contains 'Welcome to the Legacy Plaintext Banking Portal'",
            "actual": f"Selenium assertion caught actual content: '{driver.find_element(By.CSS_SELECTOR, test_config.SELECTORS['hero_title']).text[:50]}...'",
            "screenshot": screenshot_path,
            "is_demo_failure": True,
        }
    finally:
        if owns_driver and driver:
            driver.quit()
