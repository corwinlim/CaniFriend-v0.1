# CaniFriend Test Proof

Verified on 2026-09-12 from the current `main` test contracts and core deterministic/runtime/proof modules.

## Fresh result

```text
...........                                                              [100%]
11 passed in 0.07s
```

## Covered contracts

- trusted available carer selection resolves to Neighbor A
- owner approval is required before carer acceptance
- approved care can complete and record an authoritative CAIOS outcome
- `Pika` normalizes to canonical pet ID `pika`
- health/runtime deterministic fallback contract
- proposed plans remain unapproved until the explicit human action
- complete -> record outcome state transition
- Bedrock access proof redacts account/ARN/model output and keeps only fingerprints/metadata
- Bedrock proof keeps max token usage intentionally small
- Judge Recording Mode contains the required five-screen copy and actions

## Verification boundary

This was a fresh local reconstruction from files fetched from the repository's current `main` branch because the execution container could not perform a direct Git clone. It is strong contract-level evidence, but it is **not** represented as a GitHub Actions exact-checkout CI run.

For final submission, the strongest additional proof would be an exact-repository CI workflow or a fresh local checkout run when available.
