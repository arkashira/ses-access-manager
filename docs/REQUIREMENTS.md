# REQUIREMENTS.md

## Project Overview

**Project Name:** `ses-access-manager`  
**Product:** Automated AWS Simple Email Service (SES) production access request management and support escalation tool.  
**Target Users:** Small to mid‑size businesses and Internet Service Providers (ISPs) that require SES production access.  
**Goal:** Simplify the SES production access request workflow, reduce manual effort, and provide a clear escalation path for support issues.

---

## 1. Functional Requirements

| ID | Requirement | Description | Acceptance Criteria |
|----|-------------|-------------|---------------------|
| **FR‑1** | **User Registration & Authentication** | Users must be able to create an account and authenticate using email/password or SSO (OpenID Connect). | • Registration page accepts email, password, and optional SSO token.<br>• Passwords hashed with Argon2.<br>• Authenticated users receive a JWT with a 24‑hour expiry. |
| **FR‑2** | **SES Access Request Creation** | Authenticated users can submit a new SES production access request. | • Form captures: domain(s), sending volume, use case, compliance info.<br>• Validation ensures at least one domain and volume > 0.<br>• Request status set to `Pending`. |
| **FR‑3** | **Request Lifecycle Management** | System tracks request status through AWS SES approval workflow. | • Statuses: `Pending`, `Under Review`, `Approved`, `Rejected`, `Escalated`. <br>• Automatic polling of AWS SES API every 6 h to update status. |
| **FR‑4** | **Email Notification System** | Notify users of status changes via email. | • Email templates for each status.<br>• Delivery via SES (sandbox or production). |
| **FR‑5** | **Escalation Workflow** | Provide a mechanism to manually or automatically raise support tickets. | • Users can click “Escalate” on a `Rejected` or `Under Review` request.<br>• System creates a ticket in an external ticketing system (e.g., Jira) via REST API.<br>• Ticket ID is stored and displayed. |
| **FR‑6** | **Audit Trail** | Maintain immutable logs of all actions. | • Every state change, API call, and user action logged to a write‑once storage (e.g., S3 + DynamoDB). |
| **FR‑7** | **Admin Dashboard** | Admins can view all requests, filter by status, and override decisions. | • Dashboard shows table with sortable columns.<br>• Admin can change status to `Approved` or `Rejected` with a comment. |
| **FR‑8** | **Rate Limiting & Quotas** | Prevent abuse of the request API. | • Max 5 active requests per user.<br>• Rate limit of 10 requests per minute per IP. |
| **FR‑9** | **API Exposure** | Provide a RESTful API for external integrations. | • Endpoints: `/requests`, `/requests/{id}`, `/auth`. <br>• All endpoints require JWT auth. |
| **FR‑10** | **Data Export** | Users can export request history as CSV. | • Export button triggers CSV download with columns: ID, Domain, Volume, Status, CreatedAt, UpdatedAt. |

---

## 2. Non‑Functional Requirements

| ID | Requirement | Description |
|----|-------------|-------------|
| **NFR‑1** | **Performance** | • API response time < 200 ms for 95 % of requests.<br>• Background polling job must complete within 30 s. |
| **NFR‑2** | **Scalability** | • System should support 10,000 concurrent users and 5,000 active requests. |
| **NFR‑3** | **Security** | • All data in transit encrypted with TLS 1.3.<br>• Sensitive fields (e.g., passwords) stored encrypted at rest (KMS).<br>• OWASP Top‑10 mitigations applied. |
| **NFR‑4** | **Reliability** | • 99.9 % uptime SLA.<br>• Automatic failover for database and API layer. |
| **NFR‑5** | **Observability** | • Centralized logging (CloudWatch/ELK).<br>• Metrics exposed via Prometheus. |
| **NFR‑6** | **Compliance** | • GDPR‑compliant data handling.<br>• Users can request data deletion within 30 days. |
| **NFR‑7** | **Maintainability** | • Codebase follows Clean Architecture.<br>• All modules unit‑tested (≥ 80 % coverage). |
| **NFR‑8** | **Internationalization** | • UI supports English and Spanish. |

---

## 3. Constraints

| ID | Constraint | Impact |
|----|------------|--------|
| **C‑1** | AWS SES API limits | Must respect AWS SES API rate limits (e.g., 5 k requests per day). |
| **C‑2** | External Ticketing API | Must integrate with Jira Cloud; API token rotation required. |
| **C‑3** | Deployment | Must run on AWS Fargate with ECS, using RDS PostgreSQL. |
| **C‑4** | Data Residency | All data must reside in the EU‑West‑1 region. |
| **C‑5** | Open Source Licenses | All dependencies must be MIT/Apache‑2.0; no GPL. |

---

## 4. Assumptions

| ID | Assumption | Rationale |
|----|------------|-----------|
| **A‑1** | Users already have AWS accounts. | The tool only manages SES access, not account creation. |
| **A‑2** | AWS IAM roles for SES access are pre‑configured. | Simplifies implementation; focus on request workflow. |
| **A‑3** | Ticketing system supports REST API. | Enables automated escalation. |
| **A‑4** | Users will provide accurate domain and volume data. | Reduces need for extensive validation logic. |

---

## 5. Deliverables

1. **API Specification** – OpenAPI 3.0 document.  
2. **Database Schema** – ER diagram and migration scripts.  
3. **UI Mockups** – Figma files for registration, request form, dashboards.  
4. **CI/CD Pipeline** – GitHub Actions for linting, tests, and deployment.  
5. **Documentation** – User guide, admin guide, and developer onboarding docs.  

---

## 6. Acceptance Checklist

- [ ] All functional requirements implemented and unit‑tested.  
- [ ] Security audit completed (OWASP).  
- [ ] Performance benchmark meets NFR‑1.  
- [ ] Deployment pipeline fully automated.  
- [ ] Documentation published to internal Confluence.  

---
