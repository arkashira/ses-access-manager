# tech-spec.md — ses-access-manager (v1)

## 1. Stack

| Layer | Choice | Why |
|---|---|---|
| Language | **TypeScript 5.x (strict)** | Shared types across API + worker + frontend; AWS SDK v3 is first-class TS. |
| API runtime | **Node.js 20 LTS** on **Hono** (not Express) | Hono runs identically on Node, Lambda, and edge — keeps hosting portable; ~3x lighter than Express. |
| Background jobs | **BullMQ + Redis** | SES request polling, bounce/complaint ingestion, escalation timers are all cron/queue work. |
| Frontend | **Next.js 14 (App Router) + React 18 + Tailwind** | Dashboard for request status, deliverability health, appeal drafts. |
| AWS access | **AWS SDK v3** (`@aws-sdk/client-sesv2`, `client-sts`, `client-support`, `client-cloudwatch`) | Modular, tree-shakeable; STS for cross-account assume-role. |
| LLM (appeal drafting) | **Claude (claude-haiku-4-5)** for use-case draft generation + rejection-reason classification | Cheap, fast; this is the product's differentiating "auto-write a winning request" feature. |
| Validation | **Zod** | Single source of truth for API + env validation. |

**Hard call:** No microservices in v1. One API service + one worker process + Postgres + Redis. Resist Lambda-per-endpoint — SES polling needs persistent connections and predictable cron.

---

## 2. Hosting (free-tier-first)

| Component | Platform | Free tier | Upgrade trigger |
|---|---|---|---|
| API + worker | **Railway** or **Fly.io** | Fly: 3x shared-cpu-1x 256MB free; Railway $5 credit/mo | >50 active tenants → $5–20/mo |
| Postgres | **Neon** | 0.5 GB, autosuspend | >0.5GB or need branching |
| Redis | **Upstash Redis** | 10k commands/day free | >10k/day polling load |
| Frontend | **Vercel** (Hobby) | 100GB bandwidth | Commercial use → Pro $20 |
| Object storage (screenshots of AWS console rejections, attachments) | **Cloudflare R2** | 10GB + zero egress | >10GB |
| Email (our own transactional) | **Resend** | 3k/mo free | Eat your own dogfood later via SES once we trust it |

**Total v1 cost at <50 tenants: $0–5/mo.** First paid line item is Vercel Pro or Fly scale-up.

---

## 3. Data Model (Postgres)

```
tenants
  id (uuid, pk)
  name
  plan (enum: free|pro|agency)
  created_at

users
  id (uuid, pk)
  tenant_id (fk)
  email (unique)
  role (enum: owner|member)
  password_hash | oauth_sub

aws_connections                -- cross-account, NEVER store root keys
  id (uuid, pk)
  tenant_id (fk)
  account_id (12-digit)
  role_arn                     -- customer-created IAM role we assume
  external_id (uuid)           -- confused-deputy protection
  region (default us-east-1)
  status (enum: pending|active|access_denied)
  sandbox_state (enum: sandbox|production|unknown)

ses_requests                   -- each production-access / limit-increase ask
  id (uuid, pk)
  tenant_id (fk)
  aws_connection_id (fk)
  type (enum: production_access|sending_limit|rate_limit)
  status (enum: draft|submitted|rejected|approved|escalated)
  support_case_id              -- AWS Support case id when escalated
  requested_quota_24h
  requested_rate_sec
  use_case_text                -- the LLM-drafted justification
  rejection_reason_raw
  rejection_category (enum: weak_usecase|bounce_risk|incomplete|policy|other)
  submitted_at, resolved_at

deliverability_snapshots       -- pulled from SES/CloudWatch to defend access
  id, aws_connection_id (fk)
  captured_at
  bounce_rate, complaint_rate
  sent_24h, quota_24h
  reputation_status (enum: healthy|under_review|paused)

escalations
  id, ses_request_id (fk)
  channel (enum: support_case|reopen|appeal_draft)
  next_action_at              -- timer for follow-up nudge
  status (enum: open|waiting_aws|closed)

audit_log
  id, tenant_id, actor_user_id, action, target, meta(jsonb), created_at
```

Indexes: `ses_requests(tenant_id,status)`, `deliverability_snapshots(aws_connection_id,captured_at)`, `escalations(next_action_at) WHERE status='open'`.

---

## 4. API Surface

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/v1/connections` | Register an AWS account; returns IAM role + externalId setup instructions (CloudFormation one-click URL). |
| `POST` | `/v1/connections/:id/verify` | Assume role via STS, detect sandbox vs production, fetch current quotas. |
| `POST` | `/v1/requests` | Create a production-access/limit request; auto-drafts `use_case_text` via LLM from a short questionnaire. |
| `POST` | `/v1/requests/:id/submit` | Open the AWS Support case (SESv2 `PutAccountDetails` / Support `CreateCase`) and track id. |
| `GET` | `/v1/requests/:id` | Status, AWS case state, rejection category, recommended next step. |
| `POST` | `/v1/requests/:id/appeal` | Generate a rebuttal draft tuned to `rejection_category` and resubmit/escalate. |
| `GET` | `/v1/connections/:id/deliverability` | Latest bounce/complaint/reputation snapshot + "are you at risk of losing access" score. |
| `POST` | `/v1/escalations/:id/nudge` | Manually trigger a follow-up; otherwise fired by worker on `next_action_at`. |
| `GET` | `/v1/connections/:id/checklist` | Pre-submission readiness check (bounce <5%, complaint <0.1%, DKIM/SPF/DMARC, valid use case) — the thing that prevents rejection. |
| `POST` | `/v1/webhooks/ses-notifications` | Ingest SNS bounce/complaint feedback to keep deliverability fresh. |

Auth on all except the SNS webhook (which uses SNS signature verification).

---

## 5. Security Model

- **Auth:** Session cookies (httpOnly, SameSite=Lax) backed by JWT for API; OAuth (Google) + email/password via **Lucia** or **Auth.js**. Per-tenant row isolation enforced in a middleware that injects `tenant_id` into every query — no cross-tenant reads.
- **AWS access — the critical surface:** **Never** store customer access keys. Customer creates an IAM role granting us `sts:AssumeRole` with a per-tenant **ExternalId** (confused-deputy defense). We request **least-privilege**: `ses:GetAccount`, `ses:PutAccountDetails`, `sesv2:GetAccount`, `support:CreateCase/DescribeCases`, `cloudwatch:GetMetricData`. Ship a CloudFormation/Terraform template so customers see exactly what they grant.
- **Secrets:** App secrets in platform env (Fly/Railway secrets); no `.env` in repo. Per-tenant `external_id` and `role_arn` are not secrets but are tenant-scoped. DB connection over TLS. Encrypt `use_case_text`/`rejection_reason_raw` at rest is optional v1 (Neon encrypts at rest by default).
- **STS hygiene:** Assume-role sessions scoped to 15-min duration, requested on-demand per job, never cached beyond TTL.
- **Webhook:** Verify SNS message signature + topic ARN allowlist before processing.
- **Rate limiting:** Per-tenant token bucket on assume-role calls to avoid tripping AWS throttling and leaking our own posture.

---

## 6. Observability

- **Logs:** Structured JSON via **Pino**, one line per request with `tenant_id`, `request_id`, `aws_account_id`, latency. Ship to platform log drain (Fly/Railway) → free tier; **Axiom** free tier (500MB/day) for search.
- **Metrics:** Prometheus-format `/metrics` endpoint scraped by **Grafana Cloud free** (10k series). Track: `ses_requests_total{status}`, `appeal_success_rate`, `assume_role_failures_total`, `deliverability_at_risk_gauge`, queue depth, job latency p95.
- **Traces:** **OpenTelemetry** SDK auto-instrumenting Hono + AWS SDK + Postgres; export to Grafana Tempo free tier. Trace the full chain: API → assume-role → SESv2 call → DB write.
- **Product KPI dashboard:** request→approval conversion rate, median days-to-production-access, rejection-category distribution (this is the data moat — it tells us what justifications actually win).
- **Alerts:** Grafana alert on `assume_role_failures` spike (customer revoked role) and any tenant's `complaint_rate > 0.1%` (proactive churn-saver email).

---

## 7. Build / CI

- **Monorepo:** pnpm workspaces — `apps/api`, `apps/web`, `apps/worker`, `packages/shared` (Zod schemas + types).
- **CI (GitHub Actions):**
  1. `lint` — ESLint + Prettier + `tsc --noEmit` (strict).
  2. `test` — Vitest unit + integration (Testcontainers Postgres/Redis); mock AWS via `aws-sdk-client-mock`.
  3. `build` — Docker multi-stage (distroless Node) for api + worker.
  4. `migrate` — Drizzle migrations, checked in, applied on deploy.
- **CD:** Push to `main` → Actions builds + deploys to Fly/Railway via API token; Vercel auto-deploys web on push. Preview env per PR (Neon branch + Fly app suffix).
- **Quality gates:** PR blocked unless coverage ≥70% on `packages/shared` and `apps/api/services`. **Dependabot** + `pnpm audit` weekly.
- **Secrets in CI:** GitHub OIDC → no long-lived AWS keys in Actions; deploy tokens as encrypted repo secrets.