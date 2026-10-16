"""
Driver Factory Module for Passli Selenium Automated Testing Suite
================================================================
Manages WebDriver instantiation, browser options, and clean teardown.
Includes robust page readiness and layout stabilization for slow internet.
"""

import os
import time
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException

from . import test_config


def create_chrome_driver(headless: bool = None) -> webdriver.Chrome:
    """
    Instantiate and return a configured Chrome WebDriver instance.
    
    Args:
        headless: If provided, overrides test_config.HEADLESS.
    """
    if headless is None:
        headless = test_config.HEADLESS

    chrome_options = Options()
    
    if headless:
        chrome_options.add_argument("--headless=new")
    
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1440,900")
    chrome_options.add_argument("--disable-search-engine-choice-screen")
    chrome_options.add_argument("--remote-allow-origins=*")
    chrome_options.page_load_strategy = "eager"  # Avoids hanging on slow external font/image CDNs
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36"
    )

    driver = None
    last_error = None

    # Priority 1: Use downloaded matching driver if present
    driver_candidate = test_config.CHROME_155_DRIVER_PATH
    if os.path.exists(driver_candidate):
        try:
            service = Service(executable_path=driver_candidate)
            driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            last_error = e

    # Priority 2: Use Selenium 4 auto-manager
    if driver is None:
        try:
            driver = webdriver.Chrome(options=chrome_options)
        except Exception as e:
            last_error = e

    if driver is None:
        raise RuntimeError(
            f"Failed to launch Chrome WebDriver. Ensure Google Chrome is installed. "
            f"Error details: {last_error}"
        )

    # Set script timeout and page load timeout
    driver.set_page_load_timeout(45)
    driver.set_script_timeout(45)
    return driver


from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def wait_for_page_ready(
    driver: webdriver.Chrome,
    min_stabilize: float = None,
    step_reporter=None,
    step_msg: str = "Waiting for page layout, fonts, and assets to settle...",
):
    """
    Safely wait for the page to finish loading and allow slow network assets to settle:
    1. Checks document.readyState === 'complete' (waits for all HTML, styles, and scripts)
    2. Checks document.fonts to ensure web fonts and typography have rendered
    3. Verifies document.images have completed loading
    4. Performs an explicit stabilization pause so layouts and styles are fully painted
    """
    if step_reporter:
        step_reporter(step_msg)

    # Step 1: Wait for document.readyState == 'complete'
    try:
        WebDriverWait(driver, test_config.DEFAULT_WAIT_TIMEOUT).until(
            lambda d: d.execute_script("return document.readyState === 'complete'")
        )
    except TimeoutException:
        # Graceful fallback: check if at least interactive
        try:
            WebDriverWait(driver, 3.0).until(
                lambda d: d.execute_script("return document.readyState in ('complete', 'interactive')")
            )
        except Exception:
            pass

    # Step 2: Wait for web fonts (e.g. Google Fonts / Material Symbols)
    try:
        WebDriverWait(driver, 4.0).until(
            lambda d: d.execute_script("return !document.fonts || document.fonts.status === 'loaded'")
        )
    except Exception:
        pass

    # Step 3: Wait for images to complete loading
    try:
        WebDriverWait(driver, 4.0).until(
            lambda d: d.execute_script(
                "return Array.from(document.images || []).every(function(img) { return img.complete; })"
            )
        )
    except Exception:
        pass

    # Step 4: Settlement pause for slow internet connections
    settle_delay = min_stabilize if min_stabilize is not None else test_config.PAGE_SETTLE_DELAY
    if settle_delay and settle_delay > 0:
        if step_reporter:
            step_reporter(f"Page loaded. Settling layout & visual elements ({settle_delay:.1f}s)...")
        time.sleep(settle_delay)


def highlight_element(driver: webdriver.Chrome, element, color: str = "#38bdf8", duration: float = 0.6):
    """
    Draw a clean, professional cyan focus border around the element being interacted with.
    Makes it instantly clear in university presentation recordings which element is being tested.
    """
    try:
        driver.execute_script(
            f"""
            var el = arguments[0];
            var origOutline = el.style.outline;
            var origShadow = el.style.boxShadow;
            el.style.outline = '2px solid {color}';
            el.style.outlineOffset = '2px';
            el.style.boxShadow = '0 0 12px rgba(56, 189, 248, 0.6)';
            setTimeout(function() {{
                try {{
                    el.style.outline = origOutline;
                    el.style.boxShadow = origShadow;
                }} catch(e) {{}}
            }}, {int(duration * 1000)});
            """,
            element,
        )
    except Exception:
        pass


def wait_and_scroll_to_element(
    driver: webdriver.Chrome,
    locator: tuple,
    timeout: float = None,
    step_reporter=None,
    step_msg: str = None,
):
    """
    Waits for an element to be strictly visible on screen, scrolls it smoothly
    to viewport center, highlights it, and lets layout settle.
    """
    if step_reporter and step_msg:
        step_reporter(step_msg)

    t = timeout or test_config.DEFAULT_WAIT_TIMEOUT
    element = WebDriverWait(driver, t).until(
        EC.visibility_of_element_located(locator)
    )

    try:
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest', behavior: 'smooth'});",
            element,
        )
    except Exception:
        pass

    highlight_element(driver, element)
    
    # Brief settlement pause after scrolling so evaluator sees it clearly
    if test_config.STEP_DELAY >= 1.0:
        time.sleep(0.4)
    return element


def safe_click(
    driver: webdriver.Chrome,
    element_or_locator,
    timeout: float = None,
    step_reporter=None,
    step_msg: str = None,
):
    """
    Safely scrolls to and clicks an element with automatic JavaScript fallback
    if overlay, floating navbars, or animations interfere.
    """
    if step_reporter and step_msg:
        step_reporter(step_msg)

    if isinstance(element_or_locator, tuple):
        element = wait_and_scroll_to_element(driver, element_or_locator, timeout=timeout)
    else:
        element = element_or_locator
        try:
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'nearest', behavior: 'smooth'});",
                element,
            )
        except Exception:
            pass

    highlight_element(driver, element)
    
    t = timeout or test_config.DEFAULT_WAIT_TIMEOUT
    WebDriverWait(driver, t).until(EC.element_to_be_clickable(element))

    try:
        element.click()
    except Exception:
        driver.execute_script("arguments[0].click();", element)


def safe_send_keys(
    driver: webdriver.Chrome,
    element_or_locator,
    text: str,
    clear_first: bool = True,
    timeout: float = None,
    step_reporter=None,
    step_msg: str = None,
):
    """
    Safely scrolls to an input element, highlights it, clears any contents,
    and types the specified text.
    """
    if step_reporter and step_msg:
        step_reporter(step_msg)

    if isinstance(element_or_locator, tuple):
        element = wait_and_scroll_to_element(driver, element_or_locator, timeout=timeout)
    else:
        element = element_or_locator

    highlight_element(driver, element)

    if clear_first:
        element.clear()

    element.send_keys(text)


def capture_screenshot(driver: webdriver.Chrome, test_id: str, status: str = "STATE") -> str:
    """
    Capture and save a timestamped screenshot for audit reports and evidence.
    
    Returns:
        Absolute filepath to the saved PNG image.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_test_id = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in test_id)
    filename = f"{safe_test_id}_{status.upper()}_{timestamp}.png"
    filepath = test_config.SCREENSHOTS_DIR / filename
    
    try:
        driver.save_screenshot(str(filepath))
        return str(filepath)
    except Exception as e:
        print(f"[WARN] Failed to capture screenshot for {test_id}: {e}")
        return ""


def pause(custom_delay=None):
    """
    Pacing pause between actions so students can explain what is happening
    and evaluators can observe every browser interaction clearly.
    """
    delay = custom_delay if custom_delay is not None else test_config.STEP_DELAY
    if delay and delay > 0:
        time.sleep(delay)


_SHARED_DRIVER = None


def get_shared_driver(headless: bool = None) -> webdriver.Chrome:
    """
    Returns the persistent active Chrome WebDriver session.
    Keeps the browser window open across test executions without closing.
    """
    global _SHARED_DRIVER
    if _SHARED_DRIVER is not None:
        try:
            _ = _SHARED_DRIVER.window_handles
            return _SHARED_DRIVER
        except Exception:
            _SHARED_DRIVER = None

    _SHARED_DRIVER = create_chrome_driver(headless=headless)
    return _SHARED_DRIVER


def close_shared_driver():
    """Explicitly terminate the persistent shared browser session."""
    global _SHARED_DRIVER
    if _SHARED_DRIVER is not None:
        try:
            _SHARED_DRIVER.quit()
        except Exception:
            pass
        finally:
            _SHARED_DRIVER = None


def is_driver_alive(driver) -> bool:
    """Check if the webdriver instance is currently running and responsive."""
    if not driver:
        return False
    try:
        _ = driver.window_handles
        return True
    except Exception:
        return False


def ensure_authenticated_session(driver: webdriver.Chrome, step_reporter=None) -> bool:
    """
    Check if the current browser window is already logged in as qa_test_user.
    If not, perform an immediate clean authentication so authenticated tests
    can run individually without requiring manual login first.
    """
    driver.get(f"{test_config.BASE_URL}/dashboard/")
    wait_for_page_ready(driver, min_stabilize=1.0)

    if "/dashboard" in driver.current_url and len(driver.find_elements(By.CSS_SELECTOR, test_config.SELECTORS["dashboard_header"])) > 0:
        return True

    # Otherwise authenticate cleanly
    if step_reporter:
        step_reporter(f"Authenticating session for '{test_config.TEST_USERNAME}'...")

    driver.get(f"{test_config.BASE_URL}/login/")
    wait_for_page_ready(driver, min_stabilize=1.0)

    wait = WebDriverWait(driver, test_config.DEFAULT_WAIT_TIMEOUT)
    username_input = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, test_config.SELECTORS["login_username"]))
    )
    password_input = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, test_config.SELECTORS["login_password"]))
    )
    submit_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, test_config.SELECTORS["login_submit"]))
    )

    username_input.clear()
    username_input.send_keys(test_config.TEST_USERNAME)
    password_input.clear()
    password_input.send_keys(test_config.TEST_PASSWORD)
    pause(0.5)

    submit_btn.click()
    wait.until(EC.url_contains("/dashboard"))
    wait_for_page_ready(driver, min_stabilize=1.0)
    return True
