#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
args=(
  iam-policy-autopilot@latest generate-policies
  "$repo_root/infra/bedrock_access_proof.py"
  --service-hints sts bedrock
  --pretty
)

if [[ -n "${AWS_REGION:-${AWS_DEFAULT_REGION:-}}" ]]; then
  args+=(--region "${AWS_REGION:-${AWS_DEFAULT_REGION}}")
fi
if [[ -n "${AWS_ACCOUNT_ID:-}" ]]; then
  args+=(--account "$AWS_ACCOUNT_ID")
fi

DISABLE_IAM_POLICY_AUTOPILOT_TELEMETRY=true uvx "${args[@]}"
