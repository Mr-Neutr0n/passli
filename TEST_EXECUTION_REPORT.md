# Passli Automated Selenium Test Execution Report

**Execution Date/Time**: `2026-10-15 00:36:02`  
**Application Tested**: Passli Cryptographic Vault & Sharing Platform  
**Target Environment**: `http://127.0.0.1:8000`  
**Browser / Engine**: Google Chrome (Win64) with Selenium 4 WebDriver  
**Suite Executed**: `ALL`  
**Total Duration**: `29.44s`  

---

## Executive Summary Metrics

| Metric | Count / Value |
| :--- | :--- |
| **Total Tests Executed** | **14** |
| **Passed Tests** | **<span style="color:green">11</span>** |
| **Failed Tests** | **<span style="color:red">3</span>** (Includes controlled demonstrations) |
| **Skipped Tests** | **0** |
| **Success Rate (Normal Suite)** | **100%** (Excluding intentional demonstration failures) |

---

## Detailed Test Results Matrix

| Test ID | Test Name | Category | Status | Duration | Result / Failure Reason | Screenshot |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `TC01` | Open Website & Maximize Window | Normal | **PASS** | 2.6s | Application loaded successfully and hero element is visible. | [Screenshot](selenium_testing/screenshots/TC01_PASS_20261015_003605.png) |
| `TC02` | Verify Page Title | Normal | **PASS** | 0.6s | Page title matches expected value: 'Passli — Controlled Document Sharing & Ephemeral Vault' | [Screenshot](selenium_testing/screenshots/TC02_PASS_20261015_003606.png) |
| `TC03` | Navigation, History (Back/Forward), and Refresh | Normal | **PASS** | 2.49s | Successfully verified navigation link, back/forward history, and page refresh. | [Screenshot](selenium_testing/screenshots/TC03_PASS_20261015_003608.png) |
| `TC04` | Text Input (Entry, Value Verification, and Clear) | Normal | **PASS** | 1.28s | Text entered, verified via DOM property, and successfully cleared. | [Screenshot](selenium_testing/screenshots/TC04_PASS_20261015_003610.png) |
| `TC05` | Button Interaction & Cryptographic Token Generation | Normal | **PASS** | 1.27s | Button click triggered key generation successfully: G3LT-HSVQ | [Screenshot](selenium_testing/screenshots/TC05_PASS_20261015_003611.png) |
| `TC06` | Required-Field Form Validation | Normal | **PASS** | 1.32s | Submission verified; blank credentials rejected and retained on /login/. | [Screenshot](selenium_testing/screenshots/TC06_PASS_20261015_003612.png) |
| `TC07` | Invalid Authentication Handling | Normal | **PASS** | 4.38s | Negative auth triggered expected error alert: 'error
Invalid username or password. Please try again.' | [Screenshot](selenium_testing/screenshots/TC07_PASS_20261015_003617.png) |
| `TC08` | Sandbox Document Selector & Dynamic Recalculation | Normal | **PASS** | 1.19s | Selection updated from '2 selected (3.5 MB)' to '1 selected (2.4 MB)' | [Screenshot](selenium_testing/screenshots/TC08_PASS_20261015_003618.png) |
| `TC09` | Cryptographic Expiration Timer Selection | Normal | **PASS** | 1.18s | Expiration timer switched successfully to '15 mins' | [Screenshot](selenium_testing/screenshots/TC09_PASS_20261015_003619.png) |
| `TC10` | User Authentication & Dashboard Access | Normal | **PASS** | 3.94s | Successfully authenticated user 'qa_test_user' to http://127.0.0.1:8000/dashboard/ | [Screenshot](selenium_testing/screenshots/TC10_PASS_20261015_003623.png) |
| `TC11` | Secure Logout & Session Teardown | Normal | **PASS** | 0.77s | User successfully logged out; session terminated and public routes restored. | [Screenshot](selenium_testing/screenshots/TC11_PASS_20261015_003624.png) |
| `DEMO_FAIL_01` | [DEMO FAIL] Deliberate Title Mismatch | Demonstration | **FAIL (DEMO)** | 0.52s | [INTENTIONAL DEMO FAILURE] Title mismatch detected by Selenium! Expected: 'University Grading Portal 2026 — Secure Student Gateway', Actual: 'Passli — Controlled Document Sharing & Ephemeral Vault' | [Screenshot](selenium_testing/screenshots/DEMO_FAIL_01_FAIL_20261015_003624.png) |
| `DEMO_FAIL_02` | [DEMO FAIL] Deliberately Missing Element | Demonstration | **FAIL (DEMO)** | 3.7s | [INTENTIONAL DEMO FAILURE] WebDriverWait timed out after 3.0s waiting for nonexistent element '#deliberately-missing-ghost-element-xyz-999'. | [Screenshot](selenium_testing/screenshots/DEMO_FAIL_02_FAIL_20261015_003628.png) |
| `DEMO_FAIL_03` | [DEMO FAIL] Deliberate Content Mismatch | Demonstration | **FAIL (DEMO)** | 0.57s | [INTENTIONAL DEMO FAILURE] Content assertion failed! Expected string 'Welcome to the Legacy Plaintext Banking Portal' not in actual text 'Share only the records you choose.
Never your account creden...' | [Screenshot](selenium_testing/screenshots/DEMO_FAIL_03_FAIL_20261015_003629.png) |

---

## Key Findings & Evaluation Notes

1. **Core Verification**: All 5 fundamental university assignment requirements (`TC01` - `TC05`) passed reliably against the live Passli web application with verified real element selectors.
2. **Dynamic Behavior Validation**: Button testing (`TC05`) confirmed both state transformation and algorithmic key derivation (`XXXX-XXXX` token generation) rather than mere element presence.
3. **Controlled Negative Demonstrations**: Dedicated demonstration cases (`DEMO_FAIL_01` to `DEMO_FAIL_03`) verify that Selenium correctly raises `AssertionError` and `TimeoutException` when anomalies occur, providing high-visibility failure evidence for the video presentation.
4. **Zero Flakiness**: Explicit waits (`WebDriverWait` with `expected_conditions`) replace fixed sleeps, ensuring high execution speed and stable synchronization.

*Report automatically generated by `selenium_testing.test_runner` at `2026-10-15T00:36:31.492396`.*
