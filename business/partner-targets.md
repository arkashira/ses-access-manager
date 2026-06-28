Generated `partner-targets.md` for `ses-access-manager`. Key decisions:

- **8 partners, rev-share-first ordering.** 3 carry direct affiliate/rev-share (ZeroBounce, EasyDMARC, GlockApps) — all deliverability-adjacent, all sellable *inside* the access-request flow.
- **The dual-purpose insight:** the rev-share partners are also evidence-generators. A clean list (ZeroBounce), a DMARC compliance report (EasyDMARC), and an inbox-placement score (GlockApps) each *raise AWS approval probability* — our core promise — while paying us a commission. The feature that helps the user pays us twice.
- **Cloudflare DNS as the P0 wedge** (effort S): one-click SPF/DKIM/DMARC publish removes the most common auto-reject cause before submission.
- **Explicit anti-pattern flagged:** don't integrate competing ESPs (SendGrid/Postmark/Mailgun) on the happy path — they're the exit ramp off SES and dilute the "get you approved" promise.
- **PRD risk flags** included: Cloudflare token scope, Postmaster's ~100/day volume floor (which hits our new-sender users), FTC affiliate disclosure, and partner-program lead times.

Note: the file at `/tmp/partner-targets.md` previously held a pack for a different product (`api-throttle`) — a leftover from a prior run — which I overwrote.