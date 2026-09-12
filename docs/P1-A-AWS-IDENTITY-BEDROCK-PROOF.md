# P1-A — AWS least-privilege identity + Bedrock access proof

## Verified status — PASS (2026-09-12)

- AgentCore runtime: `READY`
- Runtime identity: dedicated execution role
- Trust boundary: source-account and AgentCore source-resource conditions present
- Bedrock permission: `bedrock:InvokeModel` on one selected Nova Lite model resource
- Streaming invocation: implicit deny
- Unselected model: implicit deny
- Live AgentCore invocation after policy narrowing: HTTP 200

The public-safe evidence is stored at `artifacts/aws/p1-a-bedrock-access-proof.json`.

Administrative/control-plane credentials used during infrastructure verification are not runtime credentials and are not deployed with CaniFriend. Account-specific identities and administrative security details are intentionally excluded from this public hackathon proof.

## Gate

P1-A is PASS only when all four checks succeed:

1. The runtime uses an IAM role or temporary federated role; no long-lived IAM user access key is deployed.
2. The baseline identity policy is derived from the runtime's actual AWS calls.
3. The policy is scoped to the selected Bedrock model or inference-profile resource before attachment.
4. A live Bedrock call writes a redacted proof artifact with HTTP 200.

## Preconditions

```bash
aws --version
aws sts get-caller-identity
aws bedrock get-foundation-model \
  --region "${AWS_REGION:-us-west-2}" \
  --model-identifier "${CANIFRIEND_MODEL_ID:-amazon.nova-lite-v1:0}"
```

Use an IAM role session. Do not place AWS access keys in this repository, browser code, screenshots, recordings, or proof artifacts.

## Least-privilege policy workflow

`infra/bedrock_access_proof.py` contains the deterministic verification calls used to derive and test the required permissions. `infra/generate_least_privilege_policy.sh` can be used as a helper where the referenced policy-generation tooling is available.

Review generated policy before attachment. Keep only the calls required by the proof and replace broad Bedrock resources with the exact selected model or inference-profile resource. Do not use `bedrock:*`, broad managed Bedrock administrator policies, or unnecessary `iam:PassRole` permissions for the runtime proof identity.

The deployed runtime statement was reduced to the effective IAM authorization used by non-streaming inference: `bedrock:InvokeModel` on the selected Nova Lite resource.

## Run the live proof

```bash
export AWS_REGION=us-west-2
export CANIFRIEND_MODEL_ID=amazon.nova-lite-v1:0
python infra/bedrock_access_proof.py
```

The proof output must remain redacted. It may contain model ID, region, HTTP status, stop reason, token usage, latency, and non-sensitive fingerprints. It must not contain credentials, AWS account ID, full principal/role ARN, registry URL, private endpoint, prompt text, or model output.

## Expected public result

```json
{
  "schema": "canifriend.aws-bedrock-access-proof.v1",
  "status": "PASS",
  "region": "us-west-2",
  "model_id": "amazon.nova-lite-v1:0",
  "agentcore_http_status": 200,
  "secrets_in_artifact": false
}
```

If the live script reports an authorization failure, verify model access and that the runtime identity policy covers the exact selected model or inference profile. Do not respond by attaching broad Bedrock access.
