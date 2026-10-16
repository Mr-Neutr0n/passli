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

# Explicit Wait Timeouts (seconds) - Generous timeout for slow networks/computers
DEFAULT_WAIT_TIMEOUT = float(os.environ.get("SELENIUM_WAIT_TIMEOUT", "20.0"))
SHORT_WAIT_TIMEOUT = float(os.environ.get("SELENIUM_SHORT_TIMEOUT", "3.0"))

# Browser Behavior
# Default is False so students and evaluators can watch the browser execute live in screen recordings
HEADLESS = os.environ.get("SELENIUM_HEADLESS", "false").lower() in ("true", "1", "yes")

# Presentation Delay between actions (seconds)
# Default set to 1.5s so student can narrate and show evaluator every action clearly
DEFAULT_STEP_DELAY = float(os.environ.get("SELENIUM_STEP_DELAY", "1.5"))
STEP_DELAY = DEFAULT_STEP_DELAY

# Network & Page Settlement Delay (seconds)
# Essential on slow internet: pauses after initial page navigation so all fonts, styles,
# and images complete rendering before test interactions begin.
DEFAULT_PAGE_SETTLE_DELAY = float(os.environ.get("SELENIUM_PAGE_SETTLE_DELAY", "2.5"))
PAGE_SETTLE_DELAY = DEFAULT_PAGE_SETTLE_DELAY

# Slow Process Mode Presets (for slow internet & detailed presentation narration)
SLOW_MODE_STEP_DELAY = 2.5
SLOW_MODE_SETTLE_DELAY = 3.5

# Keep Browser Window Open after completion (ideal for live class presentations)
KEEP_BROWSER_OPEN = os.environ.get("SELENIUM_KEEP_OPEN", "true").lower() in ("true", "1", "yes")


def set_step_delay(delay_seconds: float):
    """Dynamically configure delay between steps for presentation narration."""
    global STEP_DELAY
    STEP_DELAY = max(0.0, float(delay_seconds))


def set_page_settle_delay(delay_seconds: float):
    """Dynamically configure page-load settlement grace period for slow internet."""
    global PAGE_SETTLE_DELAY
    PAGE_SETTLE_DELAY = max(0.0, float(delay_seconds))


def set_keep_browser_open(keep_open: bool):
    """Configure whether browser window remains open after test execution."""
    global KEEP_BROWSER_OPEN
    KEEP_BROWSER_OPEN = bool(keep_open)


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
EXPECTED_DASHBOARD_TITLE = "Personal Vault Dashboard — Passli"
EXPECTED_DOCUMENTS_TITLE = "Personal Document Vault — Passli"
EXPECTED_UPLOAD_TITLE = "Upload Document Record — Passli Vault"
EXPECTED_SHARE_CREATE_TITLE = "Create Share Pass — Passli Personal Vault"
EXPECTED_AUDIT_TITLE = "Cryptographic Access Audit Trail — Passli Vault"

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
    
    # Authenticated Navigation Bar
    "nav_user_pill": ".nav-user-pill",
    "nav_dashboard": '[data-testid="nav-dashboard"]',
    "nav_documents": '[data-testid="nav-documents"]',
    "nav_passes": '[data-testid="nav-passes"]',
    "nav_audit": '[data-testid="nav-audit"]',
    "nav_logout_btn": '[data-testid="nav-logout"]',
    
    # Authenticated Vault Dashboard (/dashboard/)
    "dashboard_header": '[data-testid="dashboard-header"]',
    "dash_upload_btn": '[data-testid="dash-upload-btn"]',
    "dash_new_pass_btn": '[data-testid="dash-new-pass-btn"]',
    "vault_status_bar": '[data-testid="vault-status-bar"]',
    "stats_grid": '[data-testid="stats-grid"]',
    "stat_cards": ".stat-card",
    
    # Encrypted Document Vault (/documents/)
    "vault_upload_btn": '[data-testid="vault-upload-btn"]',
    "vault_search_input": '[data-testid="vault-search-input"]',
    "vault_cat_pills": ".cat-pill",
    "vault_doc_cards": ".vault-doc-card",
    
    # Document Upload Record (/documents/upload/)
    "upload_card": '[data-testid="upload-card"]',
    "upload_dropzone": "#file-dropzone",
    "upload_title": "#id_title",
    "upload_category": "#id_category",
    
    # Ephemeral Share Passes (/share/ & /share/create/)
    "share_create_form": '[data-testid="share-create-form"]',
    "back_to_passes_btn": '[data-testid="back-to-passes"]',
    
    # Cryptographic Audit Logs (/audit/)
    "audit_metric_events": '[data-testid="metric-total-events"]',
    "audit_metric_unlocks": '[data-testid="metric-verified-unlocks"]',
}
