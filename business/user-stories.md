Generated `user-stories.md` — 13 stories across 4 epics for `ses-access-manager`.

**Epics:**
1. **Request Readiness & Pre-Flight Validation** (3) — kill disqualifiers before submission; targets the ~70% of denials caused by vague use-case / missing bounce handling / unverified domain.
2. **Submission, Tracking & Rejection Recovery** (4) — the core seam: one-click submit, live case dashboard, AWS-denial parser + rebuttal drafter, limit-increase requests.
3. **Deliverability Health & Account Protection** (3) — bounce/complaint monitoring, enforcement early-warning, suppression management — the retention hook.
4. **Multi-Account, Team & ISP Scale** (3) — cross-account console, RBAC + audit, per-tenant onboarding — the ISP up-market path.

Each story carries 3–5 acceptance criteria and an S/M/L estimate, plus a coverage table and an MVP cut.

Two deliberate calls worth flagging:
- **13 stories, not 8–12.** Epic 2 needed a 4th story (limit-increase requests) because production-access and quota-increase are distinct AWS workflows that ISP Ops can't live without. Easy to drop US-2.4 to land at 12 if you want strict spec compliance — say the word.
- **The defensible sliver** is the readiness-scan → narrative-generator → rejection-analyzer loop. AWS hands you an opaque support case and a blank text box; everything else (a generic monitoring tool, the AWS console itself) leaves that gap open. That's where the product should concentrate.