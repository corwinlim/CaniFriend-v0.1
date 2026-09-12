# P1-A — AWS least-privilege identity + Bedrock access proof

## Verified status — PASS (2026-09-12)

- AgentCore runtime: `READY`
- Runtime identity: dedicated execution role
- Trust boundary: `aws:SourceAccount` and AgentCore `aws:SourceArn` conditions present
- Bedrock permission: `bedrock:InvokeModel` on one Nova Lite foundation-model ARN
- Streaming invocation: implicit deny
- Unselected Nova 2 Lite model: implicit deny
- Live AgentCore invocation after policy narrowing: HTTP 200

The public-safe evidence is stored at `artifacts/aws/p1-a-bedrock-access-proof.json`.

The control-plane connector used for the audit authenticated as the AWS account root. It is not the runtime identity and is not deployed with CaniFriend. Root-account hardening is a separate administrative security action.

## Gate

P1-A is PASS only when all four checks succeed:

1. The runtime uses an IAM role or temporary federated role; no long-lived IAM user access key is deployed.
2. IAM Policy Autopilot derives the baseline identity policy from `infra/bedrock_access_proof.py`.
3. The policy is scoped to the selected Bedrock model or inference-profile ARN before attachment.
4. A live `Converse` call writes a redacted `bedrock-access-proof.json` with HTTP 200.

## Preconditions

```bash
aws --version
aws sts get-caller-identity
aws bedrock get-foundation-model \
  --region "${AWS_REGION:-us-west-2}" \
  --model-identifier "${CANIFRIEND_MODEL_ID:-amazon.nova-lite-v1:0}"
```

Use an IAM role session. Do not place AWS access keys in this repository, Vercel browser code, screenshots, or proof artifacts.

## Generate the baseline identity policy

The deterministic command is:

```bash
uvx iam-policy-autopilot@latest generate-policies \
  "$(pwd)/infra/bedrock_access_proof.py" \
  --region "${AWS_REGION:-us-west-2}" \
  --account "$AWS_ACCOUNT_ID" \
  --service-hints sts bedrock \
  --pretty
```

Or run `bash infra/generate_least_privilege_policy.sh`. Generation does not upload or attach a policy.

Review the generated policy before attachment. Keep only the calls required by this proof (`sts:GetCallerIdentity` and the Bedrock inference action derived by Autopilot). Replace broad Bedrock resources with the exact foundation-model or inference-profile ARN verified for the selected model. Do not use `bedrock:*`, `AmazonBedrockFullAccess`, or `iam:PassRole` for this proof identity.

Autopilot 0.3.0 conservatively proposed extra Bedrock candidate actions for Boto3 `Converse`. Those candidates were not attached. The deployed runtime statement was reduced to the effective IAM authorization used by non-streaming Converse: `bedrock:InvokeModel` on the selected Nova Lite ARN.

## Run the live proof

```bash
export AWS_REGION=us-west-2
export CANIFRIEND_MODEL_ID=amazon.nova-lite-v1:0
python infra/bedrock_access_proof.py
```

Default output: `artifacts/aws/bedrock-access-proof.json`.

The committed proof may contain only redacted fingerprints, model ID, region, request ID, HTTP status, stop reason, token usage, and latency. It must not contain credentials, account ID, full principal ARN, prompt text, or model output.

## Expected result

```json
{
  "schema": "canifriend.aws-bedrock-access-proof.v1",
  "status": "PASS",
  "region": "us-west-2",
  "model_id": "amazon.nova-lite-v1:0",
  "http_status": 200,
  "stop_reason": "end_turn"
}
```

If the script reports `AccessDeniedException`, verify model access and that the attached identity policy covers the exact selected model or inference profile. Do not respond by attaching full Bedrock access.
