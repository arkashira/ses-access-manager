<h3 align="center">🛠️ ses-access-manager</h3>

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Language: Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://www.python.org/)
[![Build: pytest](https://img.shields.io/badge/Build-pytest-green.svg)](https://docs.pytest.org/)
[![Stars: 0](https://img.shields.io/github/stars/axentx/ses-access-manager.svg)](https://github.com/axentx/ses-access-manager/stargazers)

</div>

---

# 🚀 ses-access-manager

**Empower technical teams at ISPs and SMBs with automated AWS SES production access requests and support escalations.**

## Why ses-access-manager?

- **Automated Validation**: Validates DKIM and SPF records before SES access requests to reduce failures.
- **Built for ISPs & SMBs**: Specifically designed for technical teams managing AWS SES in regulated or small-scale environments.
- **CLI-First Workflow**: Streamlines the entire request lifecycle via a simple, powerful command-line interface.
- **Support Escalation Ready**: Includes built-in workflows for escalating AWS support tickets when needed.
- **Sandbox Tested**: Fully tested in sandbox environments to ensure reliability before production use.
- **Minimal Dependencies**: Built with Python, Boto3, and Click—lightweight and maintainable.
- **Open Source & MIT Licensed**: Free to use, modify, and contribute to.

## Feature Overview

| Feature                     | Description                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| SES Access Request         | Automate the process of requesting AWS SES production access.               |
| DKIM/SPF Record Validation | Validates DNS records before submitting access requests.                    |
| Support Ticket Escalation  | Provides workflow for escalating AWS support tickets if needed.             |
| Command-Line Interface     | Full control via intuitive CLI powered by Click.                            |
| Sandbox Testing            | Verified functionality in isolated AWS environments.                        |

## Tech Stack

- **Python** – Core logic and CLI interface
- **Boto3** – AWS SDK integration for SES management
- **Click** – Command-line interface framework

## Project Structure

```
ses-access-manager/
├── business/        # Business logic and domain models
├── docs/            # Documentation artifacts (PRD, BMC, etc.)
├── src/             # Source code
│   └── ses_access_manager/
│       ├── __init__.py
│       ├── cli.py
│       ├── ses_client.py
│       └── validators.py
├── tests/           # Unit and integration tests
├── pyproject.toml   # Project metadata and dependencies
└── README.md        # This file
```

## Getting Started

### Prerequisites

Ensure you have Python 3.8+ installed.

### Installation

```bash
pip install .
```

### Usage

Request SES production access:

```bash
ses-access-manager request --region us-east-1 --email sender@example.com
```

Validate DNS records:

```bash
ses-access-manager validate-dns --domain example.com
```

Escalate a support ticket:

```bash
ses-access-manager escalate-ticket --ticket-id 1234567890
```

Run tests:

```bash
pytest tests/
```

## Deploy

Deploy using pip:

```bash
pip install .
```

Or install in development mode:

```bash
pip install -e .
```

## Status

**Early-stage tool** for automating AWS SES access requests.  
Latest commit: `4048703` — _readme-keeper: generate proper project README_

## Contributing

Contributions are welcome! Please read our [CONTRIBUTING.md](./CONTRIBUTING.md) to get started.

## License

This project is licensed under the **MIT License** – see the [LICENSE](./LICENSE) file for details.