<h3 align="center">🛠️ <a href="https://github.com/axentx/ses-access-manager">ses-access-manager</a></h3>

<div align="center">
  <a href="https://github.com/axentx/ses-access-manager/blob/master/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
  </a>
  <a href="https://github.com/axentx/ses-access-manager/blob/master/pyproject.toml">
    <img src="https://img.shields.io/badge/Python-3.9-blue.svg" alt="Python 3.9">
  </a>
  <a href="https://github.com/axentx/ses-access-manager/actions">
    <img src="https://img.shields.io/badge/Build-Passed-green.svg" alt="Build Passed">
  </a>
  <a href="https://github.com/axentx/ses-access-manager/stargazers">
    <img src="https://img.shields.io/github/stars/axentx/ses-access-manager.svg?style=social" alt="Stars">
  </a>
</div>

---

# 🚀 ses-access-manager

**Power businesses with automated AWS SES production access requests.** A Python tool that automates AWS SES production access requests and support escalation for small-to-mid-size businesses and ISPs.

---

## Why ses-access-manager?

* **Automates SES production access requests**: Reduce manual AWS console interactions and save time.
* **Validates domain settings**: Ensure DKIM and SPF are correctly configured for your domain.
* **Provides a workflow for escalating support tickets**: Streamline support requests and improve response times.
* **Compliance checks**: Ensure your business meets AWS SES compliance requirements.
* **Simple CLI interface**: Easily manage SES production access requests and support escalation.
* **Unit tests**: Reliable and efficient testing of core logic.

---

## Feature Overview

| Feature | Description |
| --- | --- |
| SES Production Access Requests | Automate SES production access requests for small-to-mid-size businesses and ISPs. |
| Domain Validation | Validate DKIM and SPF settings for your domain. |
| Support Escalation Workflow | Streamline support requests and improve response times. |
| Compliance Checks | Ensure your business meets AWS SES compliance requirements. |
| CLI Interface | Easily manage SES production access requests and support escalation. |
| Unit Tests | Reliable and efficient testing of core logic. |

---

## Tech Stack

* Python
* boto3
* click

---

## Project Structure

* `business/`: Business logic and utilities.
* `docs/`: Documentation and artifacts.
* `src/`: Source code for the ses-access-manager tool.
* `tests/`: Unit tests for the ses-access-manager tool.

---

## Getting Started

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the tool

```bash
python -m ses_access_manager
```

### Test the tool

```bash
python -m unittest discover -s tests
```

---

## Deploy

### Deploy to AWS Lambda

```bash
pip install -r requirements.txt
zip -r ses-access-manager.zip .
aws lambda update-function-code --function-name ses-access-manager --zip-file fileb://ses-access-manager.zip
```

---

## Status

Last updated: 2026-06-23T09:16:17.767127Z
Commit: dbfcba3 feat(ses-access-manager): real, sandbox-tested implementation

---

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to this project.

---

## License

This project is licensed under the MIT License.