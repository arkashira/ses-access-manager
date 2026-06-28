# dataflow.md — ses-access-manager

## System Dataflow Architecture

```
                          ┌─────────────────── AUTH BOUNDARY: PUBLIC INTERNET ───────────────────┐
                          │                                                                       │
 EXTERNAL SOURCES         │   INGESTION              PROCESSING            STORAGE      SERVING    │   EGRESS
─────────────────         │  ───────────            ────────────         ─────────    ─────────   │  ────────
                          │                                                                       │
┌──────────────┐  IAM    ┌┴┐  poll/15m  ┌──────────────┐  events  ┌──────────────┐              │
│ AWS SES API  ├────────►│ │───────────►│ Collector svc├─────────►│  Postgres    │◄──┐          │
│ (acct status)│ AssumeRole │ │           │ (Lambda/ECS) │          │  (RLS per    │   │          │
└──────────────┘         │ │           └──────┬───────┘          │   tenant)    │   │ SQL      │
┌──────────────┐  SNS    │A│           ┌──────▼───────┐          └──────┬───────┘   │          │   ┌─────────┐
│ SES Reputation│───────►│P│  webhook  │ Normalizer / │  scored  ┌──────▼───────┐   ├──────────┼──►│ Web UI  │
│ / Bounce SNS │ HMAC-sig│I│──────────►│ Risk Scorer  ├─────────►│ Risk/State   │   │ GraphQL  │   │ (React) │
└──────────────┘         │G│           │ (rules+LLM)  │          │ tables       │   │ /REST API│   └─────────┘
┌──────────────┐  OAuth  │W│           └──────┬───────┘          └──────────────┘   │          │   ┌─────────┐
│ AWS Support  │◄───────►│ │           ┌──────▼───────┐          ┌──────────────┐   ├──────────┼──►│ Email / │
│ API (cases)  │ case CRUD│ │           │ Case Drafter │  drafts  │ S3 (evidence,│◄──┘ presign │   │ Slack   │
└──────────────┘         │ │           │ + Escalation │─────────►│  templates)  │   │          │   │ alerts  │
┌──────────────┐  CSV/API│ │           │ Engine       │          └──────────────┘   │          │   └─────────┘
│ User uploads │───────►└┬┘           └──────────────┘          ┌──────────────┐   │          │
│ (domains,DNS)│         │              ┌──────────────┐         │ pgvector     │◄──┘ semantic │
└──────────────┘         │              │ DNS/DMARC    │────────►│ (playbook KB)│     search   │
                         │              │ Verifier     │         └──────────────┘              │
                         └─── AUTH BOUNDARY: VPC PRIVATE SUBNET (no public ingress) ────────────┘
```

---

### 1. External data sources
- **AWS SES API** — per-tenant account sending status, quota, sandbox/production flag, sending-enabled state. Auth: cross-account **AssumeRole** (customer-provisioned IAM role, ExternalId-scoped, read-only `ses:Get*`/`ses:Describe*`).
- **SES Reputation + Bounce/Complaint SNS** — real-time deliverability events (bounce rate, complaint rate, suppression list growth). Auth: SNS subscription confirmation + **HMAC signature** verification on each payload.
- **AWS Support API** — production-access case creation, correspondence threads, case status. Requires customer **Business/Enterprise support tier**; auth via AssumeRole with `support:*` scoped permissions (fallback: guided manual case for Basic-tier accounts).
- **User uploads** — sending domains, DNS records, use-case descriptions, prior rejection emails (CSV / form / API). Auth: tenant-scoped session token.

### 2. Ingestion layer
- **Collector service** (Lambda on 15-min schedule + ECS for long polls) — pulls SES/Support state, deduplicates against last-seen snapshot.
- **Webhook receiver** (API Gateway → Lambda) — terminates SNS notifications and inbound case-update callbacks; validates signatures before forwarding.
- **Upload handler** — streams user files to S3 staging, emits an ingest event.
- **Auth boundary:** API Gateway is the only public ingress; mutual TLS / signature validation here; everything downstream sits in **private VPC subnets**.

### 3. Processing / transform layer
- **Normalizer** — maps heterogeneous SES/Support/SNS payloads to a canonical `account_health` event schema.
- **Risk Scorer** (rules engine + LLM assist) — computes a 0–100 **production-readiness score** from bounce rate (<5%), complaint rate (<0.1%), DKIM/SPF/DMARC presence, warmup volume curve, and use-case quality.
- **Case Drafter + Escalation Engine** — generates AWS-spec-compliant production-access request text, auto-fills sending volume/use-case, and triggers escalation (re-open case, tier-up suggestion) on rejection patterns.
- **DNS/DMARC Verifier** — resolves and validates domain auth records out-of-band.
- *Components run with least-privilege task roles; LLM calls scrubbed of PII before egress to model endpoint.*

### 4. Storage tier
- **Postgres (primary)** — tenants, accounts, case state machine, audit log. **Row-Level Security** enforces per-tenant isolation.
- **Risk/State tables** — time-series of scores and SES metrics for trend graphs.
- **S3** — evidence bundles, generated drafts, uploaded artifacts; SSE-KMS, per-tenant prefix + bucket policy.
- **pgvector** — semantic KB of AWS rejection reasons → remediation playbooks (reuse of company BRAIN pattern).
- **Auth boundary:** storage reachable only from processing/serving security groups; no public endpoints; KMS-encrypted at rest.

### 5. Query / serving layer
- **GraphQL/REST API** (ECS behind internal ALB) — serves dashboard reads, mutation of case actions, presigned S3 URLs.
- **Semantic search endpoint** — queries pgvector for "why was I rejected → how to fix."
- **Auth:** JWT (Cognito/Auth0) per request; tenant claim drives RLS session var; rate-limited per tenant.

### 6. Egress to user
- **Web UI (React SPA)** — readiness dashboard, one-click case submission, remediation checklist.
- **Email / Slack alerts** — score drops, case status changes, rejection-with-fix notifications. Auth: signed unsubscribe tokens, Slack OAuth per workspace.
- **Public boundary re-crossed** only via authenticated TLS responses and presigned, short-TTL (≤300s) S3 links.