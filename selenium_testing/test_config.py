"""
Configuration Module for Passli Selenium Automated Testing Suite
================================================================
Manages target URLs, browser settings, timeouts, and artifact paths.
Can be overridden via environment variables for CI/CD or local runs.
"""

import os
from pathlib import Path

# Base Paths
TESTING_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = TESTING_ROOT.parent

REPORTS_DIR = TESTING_ROOT / "reports"
SCREENSHOTS_DIR = TESTING_ROOT / "screenshots"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

# Application Target URL (defaults to local Django server; supports deployed instances)
DEFAULT_URL = "http://127.0.0.1:8000"
BASE_URL = os.environ.get("TARGET_URL", DEFAULT_URL).rstrip("/")

# Explicit Wait Timeouts (seconds)
DEFAULT_WAIT_TIMEOUT = float(os.environ.get("SELENIUM_WAIT_TIMEOUT", "10.0"))
SHORT_WAIT_TIMEOUT = float(os.environ.get("SELENIUM_SHORT_TIMEOUT", "3.0"))

# Browser Behavior
# Default is False so students and evaluators can watch the browser execute live in screen recordings
HEADLESS = os.environ.get("SELENIUM_HEADLESS", "false").lower() in ("true", "1", "yes")

# Optional micro-pause between steps (seconds) to make browser actions clearly visible in presentation videos
STEP_DELAY = float(os.environ.get("SELENIUM_STEP_DELAY", "0.3"))

# Known local Chromedriver fallback path for Windows Chrome 155
USER_PROFILE = os.environ.get("USERPROFILE", "")
CHROME_155_DRIVER_PATH = os.path.join(
    USER_PROFILE,
    ".cache",
    "selenium",
    "chromedriver",
    "win64",
    "155.0.8059.79",
    "chromedriver.exe"
)

# Test User Credentials for Authentication Tests
TEST_USERNAME = os.environ.get("PASSLI_TEST_USER", "qa_test_user")
TEST_PASSWORD = os.environ.get("PASSLI_TEST_PASS", "PassliQA2026!Secure")

# Expected Page Titles and Attributes for Assertions
EXPECTED_HOME_TITLE = "Passli — Controlled Document Sharing & Ephemeral Vault"
EXPECTED_LOGIN_TITLE = "Sign In — Passli Personal Vault"
EXPECTED_REGISTER_TITLE = "Create Personal Vault — Passli"

# Selectors Map (Real DOM selectors from Passli templates)
SELECTORS = {
    # Landing Page
    "brand_link": "#brand-link",
    "nav_home": '[data-testid="nav-home"]',
    "nav_login": '[data-testid="hero-login-btn"], [data-testid="nav-login"]',
    "nav_register": '[data-testid="hero-get-started-btn"], [data-testid="nav-register"]',
    "hero_title": '[data-testid="hero-title"]',
    "hero_subtitle": '[data-testid="hero-subtitle"]',
    "hero_get_started_btn": '[data-testid="hero-get-started-btn"]',
    "hero_login_btn": '[data-testid="hero-login-btn"]',
    "interactive_sandbox": '[data-testid="interactive-simulator"]',
    "sim_checkboxes": ".sim-doc-checkbox",
    "sim_selected_count": "#sim-selected-count",
    "sim_expiry_btns": ".expiry-btn",
    "sim_expiry_text": "#sim-expiry-text",
    "sim_generate_btn": "#sim-generate-btn",
    "sim_key_text": "#sim-key-text",
    
    # Login Page
    "login_card": '[data-testid="login-card"]',
    "login_username": "#login-username",
    "login_password": "#login-password",
    "login_submit": '[data-testid="login-submit-btn"]',
    "auth_error_box": '[data-testid="auth-error-box"]',
    
    # Authenticated Navigation & Dashboard
    "nav_user_pill": ".nav-user-pill",
    "nav_dashboard": '[data-testid="nav-dashboard"]',
    "nav_documents": '[data-testid="nav-documents"]',
    "nav_passes": '[data-testid="nav-passes"]',
    "nav_logout_btn": '[data-testid="nav-logout"]',
}
