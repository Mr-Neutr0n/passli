# Passli Automated Test Case Specification Matrix (TEST_CASES.md)

This document specifies the formal test cases implemented in the Selenium WebDriver test suite for **Passli**.  
Actual results and statuses reflect the latest automated test execution recorded on **October 15, 2026**.

---

## 1. Normal Application Tests (TC01 – TC11)

| Test Case ID | Test Case Description | Preconditions | Test Steps | Expected Result | Actual Result | Test Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`TC01`** | **Open Website & Maximize Window** | Application running at target URL; Chrome WebDriver available | 1. Launch Chrome.<br>2. Open base URL.<br>3. Maximize window.<br>4. Verify hero title is visible.<br>5. Capture evidence screenshot. | Base URL opens; browser maximizes; hero title element is displayed. | Landing page loaded; hero title visible: *"Share only the records you choose..."* | **PASS** | Meets assignment Requirement TC01. |
| **`TC02`** | **Verify Page Title** | Application running; landing page loaded | 1. Read `driver.title`.<br>2. Compare with expected project title.<br>3. Assert strict match. | Actual title equals `"Passli — Controlled Document Sharing & Ephemeral Vault"` | Title strictly matches: `"Passli — Controlled Document Sharing & Ephemeral Vault"` | **PASS** | Meets assignment Requirement TC02. |
| **`TC03`** | **Navigation, Browser History & Refresh** | Landing page loaded | 1. Locate navigation link (`a[href*='/login/']`).<br>2. Click link.<br>3. Verify destination URL (`/login/`) and login card.<br>4. Navigate back (`driver.back()`).<br>5. Verify landing page.<br>6. Navigate forward (`driver.forward()`).<br>7. Verify login page.<br>8. Refresh page (`driver.refresh()`).<br>9. Verify login card remains visible. | Seamless forward/backward navigation and page persistence across browser refresh. | Successfully navigated to `/login/`, backward to home, forward to login, and retained state after refresh. | **PASS** | Meets assignment Requirement TC03. |
| **`TC04`** | **Text Input Entry, Value Check & Clear** | Login page loaded (`/login/`) | 1. Locate `#login-username` field.<br>2. Send test string `qa_student_automation_test`.<br>3. Verify value via DOM property.<br>4. Clear input using `.clear()`.<br>5. Verify field value is empty (`""`). | Input field accepts text, verifies entered string, and successfully resets to empty. | Field accepted `qa_student_automation_test`, reflected in DOM, and cleared to `""`. | **PASS** | Meets assignment Requirement TC04. |
| **`TC05`** | **Button Testing & Dynamic Token Generation** | Landing page loaded with interactive sandbox visible | 1. Scroll to `#sim-generate-btn`.<br>2. Click button.<br>3. Verify button state label updates to `"Pass & Key Generated!"`.<br>4. Verify generated key matches cryptographic pattern `XXXX-XXXX`. | Button triggers client-side key generation; code updates to valid 8-character token. | Button feedback confirmed; new token `'G3LT-HSVQ'` generated and verified against regex. | **PASS** | Meets assignment Requirement TC05. Validates intended behavioral response. |
| **`TC06`** | **Required-Field Form Validation** | Login page loaded (`/login/`) | 1. Clear username and password fields.<br>2. Click Sign In submit button.<br>3. Verify user remains on `/login/` and form rejects empty payload. | Submission blocked; user retained on `/login/`; form errors/validation displayed. | Retained on `http://127.0.0.1:8000/login/`; client-side/server rejection verified. | **PASS** | Meets assignment Requirement TC06. |
| **`TC07`** | **Invalid Authentication Handling** | Login page loaded (`/login/`) | 1. Enter non-existent credentials (`invalid_student_qa`, `DefectivePass2026!`).<br>2. Submit form.<br>3. Verify error alert box (`[data-testid="auth-error-box"]`) appears with error message. | Error alert displayed containing `"Invalid username or password. Please try again."` | Alert box rendered with text: `"Invalid username or password. Please try again."` | **PASS** | Meets assignment Requirement TC07. |
| **`TC08`** | **Interactive Sandbox Document Selector** | Landing page sandbox in viewport | 1. Locate simulator document checkboxes (`.sim-doc-checkbox`).<br>2. Toggle second checkbox.<br>3. Verify dynamic counter (`#sim-selected-count`) updates count and MB size. | Counter recalculates instantly (e.g. from 2 items to 1 item / 2.4 MB). | Selection updated dynamically from `'2 selected (3.5 MB)'` to `'1 selected (2.4 MB)'`. | **PASS** | Validates client-side DOM telemetry recalculation. |
| **`TC09`** | **Cryptographic Expiration Timer Selection** | Landing page sandbox in viewport | 1. Locate `.expiry-btn` pills.<br>2. Click `'15 mins'` button.<br>3. Verify `#sim-expiry-text` label synchronizes to `'15 mins'`. | Countdown card label updates to `'15 mins'`. | Telemetry label successfully synced to `'15 mins'`. | **PASS** | Validates interactive UI state binding. |
| **`TC10`** | **Valid User Authentication & Dashboard Access** | User `qa_test_user` exists in database | 1. Enter valid credentials.<br>2. Click Sign In.<br>3. Wait for redirect to `/dashboard/`.<br>4. Verify `[data-testid="dashboard-header"]` and user greeting. | HTTP 302 redirect to `/dashboard/`; authenticated interface components rendered. | Landed on `/dashboard/`; greeting *"Welcome back, qa_test_user!"* verified. | **PASS** | Meets assignment Requirement TC10. |
| **`TC11`** | **Secure Logout & Session Teardown** | User is authenticated on `/dashboard/` | 1. Locate CSRF logout form.<br>2. Submit form.<br>3. Verify redirect away from private routes to public page.<br>4. Verify public Sign In links restored. | Session terminated; user redirected to public route; authenticated controls cleared. | Landed on public landing page with public Sign In link restored; private route cleared. | **PASS** | Meets assignment Requirement TC11. |

---

## 2. Controlled Negative Demonstrations (DEMO_FAIL_01 – DEMO_FAIL_03)

> **Important Presentation Note**: These 3 test cases are **deliberately engineered to fail** for the university presentation video. They demonstrate Selenium's capability to detect mismatches, enforce timeouts, and report failures without crashing the automation system.

| Test Case ID | Test Case Description | Preconditions | Test Steps | Expected Result | Actual Result | Test Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`DEMO_FAIL_01`** | **Intentional Title Mismatch Demonstration** | Base URL loaded in browser | 1. Read actual page title.<br>2. Intentionally assert equality against artificial string `"University Grading Portal 2026 — Secure Student Gateway"`. | Assertion failure caught by Selenium (`AssertionError`). | Selenium intercepted mismatch: expected `'University Grading Portal 2026...'`, got `'Passli — Controlled Document Sharing & Ephemeral Vault'`. | **FAIL (DEMO)** | Demonstrates exact title comparison assertion failure. |
| **`DEMO_FAIL_02`** | **Deliberately Missing Element Demonstration** | Landing page loaded | 1. Configure explicit wait with short timeout (3.0s).<br>2. Search for non-existent ghost selector `#deliberately-missing-ghost-element-xyz-999`. | `TimeoutException` raised when element is not located within 3 seconds. | Selenium `TimeoutException` triggered after 3.0s: element was not present in DOM. | **FAIL (DEMO)** | Demonstrates timeout handling for missing elements. |
| **`DEMO_FAIL_03`** | **Deliberate Content Mismatch Demonstration** | Landing page loaded | 1. Locate hero title element.<br>2. Assert that hero copy contains `"Welcome to the Legacy Plaintext Banking Portal"`. | Assertion failure caught by Selenium (`AssertionError`). | Selenium intercepted content mismatch: expected legacy banking text not found in actual Passli hero text. | **FAIL (DEMO)** | Demonstrates string inclusion assertion failure. |

---

## Summary of Latest Execution
- **Total Test Cases**: 14
- **Normal Test Cases Passed**: 11 / 11 (100% Pass Rate)
- **Controlled Negative Demonstrations**: 3 / 3 (All triggered expected intentional errors)
- **Uncontrolled / Unexpected Failures**: 0
