# Passli Selenium WebDriver Automated Testing Suite

A professional, runnable Selenium 4 automated testing framework and live desktop dashboard built for the **Passli Cryptographic Vault & Controlled Sharing Platform**.

---

## 1. Project Inspection & Architecture

- **Target Application**: Passli Cryptographic Document Vault & Ephemeral Sharing Platform
- **Backend Framework**: Django 5.2 (Python 3.12, SQLite database with PostgreSQL compatibility)
- **Frontend Framework**: Semantic HTML5, CSS3 Custom Properties, Geist Typography, Vanilla JavaScript
- **Testing Technology**: Python 3.12, Selenium WebDriver 4, Tkinter Desktop GUI, ChromeDriver for Chrome 155
- **Local Application URL**: `http://127.0.0.1:8000` (or Railway deployment `https://web-production-c1bd05e.up.railway.app`)

### Folder Structure
```
selenium_testing/
├── main.py                     # Primary entry point (launches Dashboard or CLI runner)
├── dashboard.py                # Thread-safe Tkinter Live PASS/FAIL Desktop Dashboard
├── test_config.py              # Central configuration (URLs, timeouts, credentials, selectors)
├── driver_factory.py           # Robust Chrome WebDriver factory with Chrome 155 driver & persistent window session
├── test_runner.py              # Multi-threaded test runner & reporting engine (16 Full Tests + 3 Demo Tests)
├── requirements.txt            # Python dependencies for the test suite
├── README.md                   # Complete documentation and presentation guide
├── tests/
│   ├── __init__.py
│   ├── test_tc01_open_website.py        # TC01: Open Website & Maximize Window
│   ├── test_tc02_page_title.py          # TC02: Verify Page Title
│   ├── test_tc03_navigation.py          # TC03: Navigation & History (Back/Forward/Refresh)
│   ├── test_tc04_text_input.py          # TC04: Text Input, DOM Verification & Clear
│   ├── test_tc05_button.py              # TC05: Button Behavior & Token Generation
│   ├── test_tc06_form_validation.py     # TC06: Required-Field Form Validation
│   ├── test_tc07_invalid_login.py       # TC07: Invalid Credentials Authentication
│   ├── test_tc08_sandbox_selector.py    # TC08: Dynamic Document Checkbox & Telemetry
│   ├── test_tc09_expiry_selector.py     # TC09: Expiration Timer Selection & Sync
│   ├── test_tc10_valid_auth.py          # TC10: Valid User Login & Dashboard Access
│   ├── test_tc12_dashboard_inspection.py# TC12: Dashboard Inspection & Telemetry Metrics
│   ├── test_tc13_vault_documents.py     # TC13: Encrypted Vault Documents & Filter
│   ├── test_tc14_document_upload.py     # TC14: Document Upload Portal & Security Form
│   ├── test_tc15_share_management.py    # TC15: Ephemeral Share Pass Management
│   ├── test_tc16_audit_trail.py         # TC16: Cryptographic Security Audit Trail
│   ├── test_tc11_logout_session.py      # TC11: CSRF Logout & Session Teardown
│   └── test_negative_demonstrations.py  # DEMO_FAIL_01 to 03: Controlled Intentional Failures
├── reports/
│   ├── report.html             # Standalone dark-mode HTML execution report
│   ├── report.json             # Machine-readable JSON execution metrics
│   └── execution.log           # Timestamped plain-text execution logs
└── screenshots/                # Automated PNG screenshots captured per test case
```

---

## 2. Quick Start Guide

### Step 1: Install Dependencies
From the repository root with your virtual environment activated:
```powershell
pip install -r selenium_testing/requirements.txt
```

### Step 2: Start the Web Application
In a dedicated terminal, launch the Django development server:
```powershell
python manage.py runserver 127.0.0.1:8000
```
Verify by visiting `http://127.0.0.1:8000/` in your browser.

### Step 3: Launch the Live Testing Dashboard
In a second terminal window, run:
```powershell
python selenium_testing/main.py
```
The compact dark-mode **Tkinter Live Dashboard** will open on your desktop. It remains on top of other windows so you can easily record both the dashboard and the browser during your screen recording.

---

## 3. Continuous Browser Window Mode (Presentation Mode)

By default, **the Chrome browser window NEVER closes automatically** (`KEEP_BROWSER_OPEN = True`).
- **Single Continuous Window**: All 16 tests run sequentially inside the same visible Chrome browser window without closing or restarting.
- **Explain Live**: When a test finishes, the browser remains open on screen so you can point, scroll, and explain features to your instructor.
- **Run Subsequent Tests**: When you run another individual test (e.g. TC13 or TC14), it executes seamlessly in the active window without opening a new one.
- **Window Controls**:
  - `🪟 Keep Browser Open`: Checkbox in the top header to toggle automatic closing on or off.
  - `❌ Close Browser`: Explicit button in the top header to close Chrome whenever your presentation is finished.

---

## 4. Dashboard Features & Controls

The dashboard is designed for high visual appeal and clear university video presentation:
- **Project Name & Engine Status**: Live telemetry showing target URL and Selenium driver state.
- **Metric Cards**: Total Tests, Passed (Green), Failed (Red), Skipped (Yellow/Gray), Total Duration.
- **Progress Bar**: Smooth animated completion bar reflecting test suite progress.
- **Live Test Matrix**: Displays Test ID, Name, Category, Live Status (`WAITING`, `RUNNING`, `PASS`, `FAIL`), and Duration.
- **Always-on-Top Pin (`📌 On Top: ON`)**: Pins the dashboard above the browser for clean side-by-side video recording.
- **Execution Pacing & Narration Speed (Slowdown Controls)**:
  - `⏱ Action Pacing`: Adjusts the pause time at every step so you have ample time to speak and explain what is happening on screen to your professor.
    - `Slow Process Mode (2.5s)` *(Recommended default for presentation)*
    - `Presentation Mode (1.5s)`
    - `Very Slow Narration (3.5s)`
    - `Ultra Slow (5.0s)`
  - `🌐 Slow Internet Pre-Load`: Ensures fonts, layout, and heavy assets fully render before interactions.
  - `🐢 Patient Full Pre-Load`: Quick toggle to enforce slow-network settling.
- **Run Individual Tests**:
  - **Dropdown Selector**: Choose any test (public, authentication, or post-login) from the dropdown and click `▶ Run Selected from List`.
  - **Table Row Click**: Click on any test row in the live matrix and click `▶ Run [ID] Now`.
  - **Double Click**: Double-click any row in the table to execute that test immediately.
  - *Isolated Execution*: Even if you run an authenticated test like TC12 (Dashboard), TC13 (Documents), TC14 (Upload), TC15 (Share), or TC16 (Audit) individually, it automatically ensures an authenticated session so it never fails!
- **Suite Action Buttons**:
  - `▶ Full Website Suite (16)`: Runs all 16 tests covering the entire website lifecycle from landing to login, post-login vault, and logout.
  - `▶ After-Login Suite (6)`: Runs authenticated features: Login (TC10), Dashboard (TC12), Documents Vault (TC13), Upload Portal (TC14), Share Pass (TC15), and Audit Trail (TC16).
  - `▶ Core Suite (11)`: Runs the initial 11 baseline assignment test cases.
  - `⚠ Demo Failures (3)`: Runs the 3 controlled negative demonstration tests for showing error handling.
  - `⏹ Stop`: Gracefully terminates execution after the current running test.
  - `🗑 Clear`: Resets the treeview and metric counters.
  - `🌐 Open HTML Report`: Launches the generated HTML report in your browser.
  - `📸 Screenshots`: Opens the folder containing all timestamped screenshot evidence.

---

## 5. Command-Line (CLI) Execution Options

You can also run full suites or individual tests via the command line:

```powershell
# Run the entire website suite (all 16 tests) with Chrome window remaining open:
python selenium_testing/main.py --cli --suite full --delay 2.0

# Run after-login features only (Login, Dashboard, Documents, Upload, Share, Audit):
python selenium_testing/main.py --cli --suite auth --delay 2.0

# Run a specific individual test slowly for recording (e.g. TC13 Vault Documents):
python selenium_testing/main.py --test TC13 --delay 2.0

# Run TC14 (Document Upload Portal) individually:
python selenium_testing/main.py --test TC14 --delay 2.0

# Run TC05 (Dynamic Token Generator) individually:
python selenium_testing/main.py --test TC05 --delay 1.5

# Run DEMO_FAIL_02 (TimeoutException demo) individually:
python selenium_testing/main.py --test DEMO_FAIL_02

# Run headlessly and auto-close browser when finished:
python selenium_testing/main.py --cli --suite full --headless --close-browser
```

---

## 6. University Presentation Script (5–10 Minutes Walkthrough)

When recording your university assignment video, follow this recommended structure:

### Part 1: Introduction (1 Minute)
1. Introduce yourself, the course, and project name: **Passli — Controlled Cryptographic Document Vault**.
2. Mention the architecture: Python, Selenium 4 WebDriver, and a custom multi-threaded Tkinter dashboard communicating over thread-safe event queues.
3. Show the web application running at `http://127.0.0.1:8000`.

### Part 2: Normal Application Testing Demo (4–5 Minutes)
1. Open the dashboard side-by-side with your browser window (`python selenium_testing/main.py`).
2. Point out that the Chrome window stays open continuously so you can walk through the live website without interruptions.
3. Click **`▶ Full Website Suite (16)`** (or **`▶ After-Login Suite (6)`**).
4. Narrate while the browser automatically executes:
   - **TC01 & TC02**: Browser opens, maximizes, verifies hero copy, and asserts page title.
   - **TC03**: Clicks "Sign In", verifies navigation to `/login/`, tests browser Back history, tests Forward history, and tests Page Refresh persistence.
   - **TC04**: Inputs test data into username field, verifies value via DOM attributes, clears field, and verifies empty state.
   - **TC05**: Scrolls to interactive sandbox, clicks cryptographic generator button, and validates that a dynamic 8-character token (format `XXXX-XXXX`) was generated.
   - **TC06 & TC07**: Demonstrates required field validation and negative authentication handling with invalid credentials.
   - **TC08 & TC09**: Toggles document selection checkboxes (verifying dynamic MB recalculation) and tests expiration timer pills.
   - **TC10**: Authenticates with valid credentials, verifies redirect to `/dashboard/`.
   - **TC12**: Inspects personalized user greeting, Zero-Knowledge security status bar, and 4 telemetry metric cards.
   - **TC13**: Navigates to `/documents/`, verifies encrypted document cards, tests category domain filter pills (`Medical`, etc.), and performs real-time search.
   - **TC14**: Navigates to `/documents/upload/`, inspects AES-256 dropzone, fills in document title, and validates category selection.
   - **TC15**: Navigates to `/share/create/`, tests Ephemeral Share Pass creation form, TTL duration controls, and verifies active passes list.
   - **TC16**: Navigates to `/audit/`, inspects real-time security audit trail, verified key unlocks, and event logs.
   - **TC11**: Performs secure CSRF logout and verifies session teardown.
5. Point out the dashboard updating live: all tests turn **GREEN (PASS)** with execution times.

### Part 3: Controlled Negative Demonstrations Demo (2 Minutes)
1. Explain to the evaluator: *"Now I will demonstrate how our Selenium framework intercepts anomalies and generates structured failure evidence using 3 controlled negative demonstration tests."*
2. Click **`⚠ Demo Failures (3)`**.
3. Explain the 3 demonstration tests:
   - **DEMO_FAIL_01**: Compares the real page title against a deliberately mismatched university title, showing how Selenium raises an `AssertionError`.
   - **DEMO_FAIL_02**: Searches for a non-existent ghost element with a 3-second explicit wait, demonstrating how Selenium cleanly catches a `TimeoutException`.
   - **DEMO_FAIL_03**: Validates element content against deliberate legacy banking text, proving that text content assertion catches semantic drift.
4. Point out the dashboard showing **RED (FAIL)** for the 3 demo tests, with exact error messages and reasons displayed.

### Part 4: Evidence & Reports (1 Minute)
1. Click **`🌐 Open HTML Report`** from the dashboard.
2. Show the evaluator the generated responsive HTML report (`report.html`) with total counts, timing metrics, and screenshot links.
3. Show the generated files in the project:
   - `TEST_CASES.md`: Complete test specification and actual result matrix.
   - `selenium_testing/reports/report.json`: Machine-readable results.
   - `selenium_testing/screenshots/`: Timestamped PNG screenshots.

---

## 7. Pre-Configured Test Credentials

The test suite comes with a pre-seeded, dedicated testing user:
- **Username**: `qa_test_user`
- **Password**: `PassliQA2026!Secure`
- **Role**: Standard Vault User

*Credentials can also be customized via environment variables: `PASSLI_TEST_USER` and `PASSLI_TEST_PASS`.*
