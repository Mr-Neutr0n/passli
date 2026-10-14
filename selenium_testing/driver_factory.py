"""
Driver Factory Module for Passli Selenium Automated Testing Suite
================================================================
Manages WebDriver instantiation, browser options, and clean teardown.
Automatically detects matching local ChromeDriver or uses Selenium 4 manager.
"""

import os
import time
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

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
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(30)
    return driver


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
