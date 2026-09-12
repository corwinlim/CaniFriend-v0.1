# CaniFriend Live AWS Proof

Verified on 2026-09-12.

## Build and runtime

- AWS CodeBuild ARM64 build: `SUCCEEDED`
- Amazon ECR image: built and deployed for the CaniFriend v0.1 AgentCore runtime
- Amazon Bedrock AgentCore Runtime: `READY`
- Protocol: HTTP
- Agent mode: Strands
- Bedrock model: `amazon.nova-lite-v1:0`

Account-specific build IDs, runtime IDs, registry locations, role identifiers, and other control-plane identifiers are intentionally omitted from the public repository. They are not required to reproduce or judge the application behavior.

## Live judge-path result

The live Strands invocation returned HTTP 200 and produced the intended safe proposal:

- Pet: Pika (synthetic demo data)
- Trusted carer: Neighbor A (synthetic demo data)
- Dinner: CaniBowl Chicken 100g
- Target: 19:00
- Owner Approval Required: Yes

## Observability

Amazon CloudWatch runtime logs recorded successful invocations, including the final judge-path session completing successfully in approximately 2.666 seconds.

The public proof reports behavior and outcome rather than publishing account-specific log-group names or session identifiers.

## What this proves

The agent path is not only a static UI fixture. The deployed path reaches Amazon Bedrock AgentCore, executes a Strands agent, uses Bedrock for reasoning, and preserves the human approval boundary before consequential care handoff.

## Verification boundary

This document is a redacted public summary of the verified hackathon run. It is not a credential, deployment manifest, or substitute for the repository's reproducible deterministic test path. See `README.md` for local reproduction instructions and `artifacts/aws/p1-a-bedrock-access-proof.json` for the public-safe machine-readable proof summary.
