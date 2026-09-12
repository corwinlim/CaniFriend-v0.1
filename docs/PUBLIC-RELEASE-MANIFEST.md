# CaniFriend v0.1 — Public Release Manifest

Status: **PRE-PUBLISH / RC CERTIFIED**. This document defines the intended public hackathon boundary. It does not authorize changing repository visibility.

## Include

The following repository surfaces are intended to be public for the Agents for Humans submission:

- `LICENSE`
- `README.md`
- `pyproject.toml`
- `vercel.json`
- `.github/workflows/release-candidate.yml` — exact-checkout release certification
- `agent/` — Strands agent, deterministic care logic, audit helper, synthetic/demo tools, runtime entrypoint
- `shared/` — hackathon-safe data contracts
- `tests/` — safety, state-transition, runtime, demo, and proof tests
- `web/` — hackathon judge UI and client logic
- `infra/bedrock_access_proof.py` — redacted verification helper
- `infra/generate_least_privilege_policy.sh` — policy-generation helper
- `artifacts/aws/p1-a-bedrock-access-proof.json` — redacted machine-readable proof
- `docs/` — architecture, demo, deployment, testing, observability, submission, recording, and redacted proof documentation

## Explicitly exclude from this repository

Do not add any of the following to the public release:

- CAIOS production longitudinal Memory Engine
- production retrieval, ranking, scoring, recommendation, clinical, nutrition, or evidence-graph implementations
- proprietary prompts, private evidence corpora, decision policies, evaluation datasets, or production model-routing logic
- production databases, exports, backups, logs, user records, veterinary records, CRM records, or real care records
- AWS access keys, temporary credentials, session tokens, cookies, authorization headers, presigned URLs, account IDs, full principal/role ARNs, private registry URLs, private endpoints, or unrelated infrastructure identifiers
- Supabase, Render, Vercel, database, CRM, messaging, or other production secrets
- unrelated CAIOS/CaniBowl/CaniBiz/CaniTrust source code, funding materials, contracts, investor documents, internal roadmaps, or private operational documents

## Public data policy

Only synthetic/demo pet, owner, neighbor, permission, care-plan, observation, and outcome data may be committed for the judge path. Pika and Neighbor A in this repository are demo fixtures, not production records.

## Public AWS evidence policy

Public proof should establish the technical claim while minimizing infrastructure disclosure. Allowed evidence includes region, selected model ID, runtime status, HTTP status, non-sensitive timing, permission behavior, and redacted build/runtime outcomes. Do not publish account-specific control-plane identifiers merely to make the proof look more detailed.

## Release-candidate certification — PASS

Exact-checkout GitHub Actions certification completed successfully on 2026-09-13 MYT for release-candidate commit `cfadc9c9204360ea227faf5a01f7da296566437f`.

Observed successful steps:

- exact repository checkout
- Python 3.11 setup
- dependency installation from `agent/requirements.txt`
- full `pytest -q` suite
- deterministic Pika dinner judge-path certification
- public-release invariant checks

The deterministic certification asserts that Neighbor A is selected, dinner remains CaniBowl Chicken 100g at 19:00, and the care plan remains `proposed`, `owner_approved=false`, and `requires_owner_approval=true` before the human gate.

## Human/static final review — PASS WITH PUBLICATION GATE

A final repository-surface review found the intended hackathon-only code, synthetic fixtures, tests, web judge UI, redacted AWS evidence, documentation, and MIT license. No unresolved credential-pattern finding was returned by the final repository search. The README explicitly separates hackathon implementation from CAIOS Background IP. AWS proof docs omit unnecessary account-specific build/runtime/log identifiers.

This review does **not** include future screenshots/video; those must be separately checked before upload. It also does not authorize repository publication.

## Publication gates

Technical gates now satisfied:

1. Repository-wide secret-pattern scan: PASS for reviewed current `main`.
2. Human/static repository review: PASS for reviewed current `main`.
3. README cold-start consistency: PASS.
4. Exact-checkout install + `pytest -q`: PASS.
5. Deterministic Pika judge path / human approval boundary: PASS.
6. Architecture and proof-doc redaction: PASS.
7. MIT license + Background-IP disclosure: PASS.

Still required before/at publication:

8. Demo screenshots/video must be separately checked for secrets/private AWS identifiers before upload.
9. Corwin must give explicit publication authorization. Generic instructions such as “继续” or “下一步” are **not** publication authorization.

## Post-publication verification

After publication, verify from an unauthenticated browser or fresh clone that:

- repository is accessible,
- README renders correctly,
- architecture image renders,
- clone/install/test instructions work,
- no private files were added during publication,
- the exact public repository URL is the one entered into Devpost.
