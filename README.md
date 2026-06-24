<h3 align="center">🛠️ ses-access-manager</h3>

<div align="center">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Build-Testing-passing.svg" alt="Build Status">
  <img src="https://img.shields.io/badge/Stage-Early-yellow.svg" alt="Stage">
</div>

---

# 🚀 ses-access-manager

**Automate AWS SES production access requests and support escalation for small‑to‑mid‑size businesses and ISPs.**

## Why ses-access-manager?

*   **Efficiency**: Eliminates manual AWS console navigation and repetitive form filling.
*   **Compliance**: Validates DKIM and SPF records before submission to ensure readiness.
*   **Workflow**: Provides a structured workflow for escalating support tickets to AWS.
*   **Automation**: Handles the entire request lifecycle via a simple CLI interface.
*   **Target**: Built specifically for technical teams at ISPs and SMBs.
*   **Testing**: Includes sandbox-tested implementation with unit test coverage.

## Feature Overview

| Feature | Description |
| :--- | :--- |
| **Production Access Automation** | Automates the submission of SES production access requests using the AWS SDK. |
| **Domain Validation** | Checks DKIM and SPF configuration to ensure domain compliance. |
| **Support Escalation** | Provides a workflow for managing and escalating support tickets. |
| **CLI Interface** | Built with Click for an intuitive command-line experience. |
| **Compliance Checks** | Helper functions to verify domain settings before request submission. |

## Tech Stack

*   **Python**: Core language for the utility.
*   **Boto3**: AWS SDK for interacting with AWS services.
*   **Click**: CLI framework for building the command-line interface.

## Project Structure

```
.
├── business/       # Business logic and context
├── docs/           # Documentation (PRD, REQUIREMENTS, etc.)
├── src/            # Source code
├── tests