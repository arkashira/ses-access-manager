<h3 align="center">🛠️ ses-access-manager</h3>

<div align="center">
  <a href="https://github.com/axentx/ses-access-manager/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
  </a>
  <a href="https://github.com/axentx/ses-access-manager">
    <img src="https://img.shields.io/badge/Language-Python-blue.svg" alt="Language: Python">
  </a>
  <a href="https://github.com/axentx/ses-access-manager/actions">
    <img src="https://img.shields.io/badge/Build-Passing-green.svg" alt="Build: Passing">
  </a>
  <a href="https://github.com/axentx/ses-access-manager/stargazers">
    <img src="https://img.shields.io/github/stars/axentx/ses-access-manager.svg?style=social" alt="Stars">
  </a>
</div>

---
# 🚀 ses-access-manager
**Power technical teams with automated AWS SES production access request management and support escalation tools.** Automated AWS SES production access request management and support escalation tools for small/mid-size businesses and ISPs.

## Why ses-access-manager?
- **Streamlined Onboarding**: Automate the process of requesting AWS SES production access, reducing manual effort and increasing efficiency.
- **Compliance Guidance**: Provide tools and guidance to help users comply with AWS email policies, reducing the risk of non-compliance.
- **Support Escalation**: Offer support escalation workflows to help users resolve SES-related issues with AWS, reducing downtime and increasing productivity.
- **Domain Validation**: Validate sender domains, DKIM/SPF setup, and email sending best practices, ensuring secure and reliable email sending.
- **Non-Expert Friendly**: Structure tools to guide non-experts through compliance with AWS email policies, making it accessible to a wider range of users.
- **Customizable**: Allow for customization to meet the specific needs of small/mid-size businesses and ISPs.
- **Cost-Effective**: Reduce the cost and time associated with manual SES production access requests and support escalation.

## Feature Overview
| Feature | Description |
| --- | --- |
| Automated SES Production Access Requests | Automate the process of requesting AWS SES production access |
| Support Escalation Workflows | Provide workflows to help users resolve SES-related issues with AWS |
| Domain Validation | Validate sender domains, DKIM/SPF setup, and email sending best practices |
| Compliance Guidance | Offer guidance to help users comply with AWS email policies |
| Customizable | Allow for customization to meet the specific needs of users |

## Tech Stack
* Python
* boto3
* flask
* aws-ses
* terraform

## Project Structure
* business: Business logic and automation scripts
* docs: Documentation and guides

## Getting Started
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## Deploy
```bash
# Deploy to AWS using Terraform
terraform init
terraform apply
```

## Status
Last commit: bd99f5a - docs: add startup artifacts (PRD.md, REQUIREMENTS.md, BMC.md, STORIES.md)

## Contributing
[CONTRIBUTING.md](CONTRIBUTING.md)

## License
Licensed under the MIT License.