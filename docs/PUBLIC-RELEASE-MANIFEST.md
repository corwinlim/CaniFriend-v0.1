# CaniFriend v0.1 — Public Release Manifest

Status: **PRE-PUBLISH**. This document defines the intended public hackathon boundary. It does not authorize changing repository visibility.

## Include

The following repository surfaces are intended to be public for the Agents for Humans submission:

- `LICENSE`
- `README.md`
- `pyproject.toml`
- `vercel.json`
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

Public proof should establish the technical claim while minimizing infrastructure disclosure. Allowed evidence includes:

- region
- selected model ID
- runtime status
- HTTP success/failure status
- non-sensitive latency/timing
- permission behavior (allowed/denied)
- redacted build/runtime outcome

Do not publish account-specific control-plane identifiers merely to make the proof look more detailed.

## Publication gates

Before changing repository visibility to public, all of the following must be true:

1. Repository-wide secret-pattern scan has no unresolved findings.
2. Human review confirms no real customer, owner, veterinary, or operational data is present.
3. README cold-start instructions are internally consistent with the repository.
4. A clean clone installs dependencies and executes `pytest -q` successfully in a supported Python environment.
5. The deterministic Pika dinner judge path runs from the clean clone and stops at the human approval boundary.
6. Architecture and proof docs contain no unnecessary account-specific/private deployment identifiers.
7. Demo screenshots/video are separately checked for secrets and private AWS identifiers.
8. Repository still contains the MIT `LICENSE` and the prior-work / Background-IP disclosure.
9. Corwin gives explicit publication authorization. Generic instructions such as “继续” or “下一步” are **not** publication authorization.

## Post-publication verification

After publication, verify from an unauthenticated browser or fresh clone that:

- repository is accessible,
- README renders correctly,
- architecture image renders,
- clone/install/test instructions work,
- no private files were added during publication,
- the exact public repository URL is the one entered into Devpost.
