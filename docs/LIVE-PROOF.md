# CaniFriend Live AWS Proof

Verified on 2026-09-12.

## Build and runtime

- AWS CodeBuild ARM64 build: `CaniFriendV01ArmBuild:08856766-77b2-44b9-8adb-c19638441db9`
- Build result: `SUCCEEDED`
- ECR image: `canifriend-v01-agentcore:p3`
- Amazon Bedrock AgentCore Runtime: `CaniFriendRuntime`
- Runtime ID: `CaniFriendRuntime-k6Ik8Q9n01`
- Runtime status: `READY`
- Protocol: HTTP
- Agent mode: Strands
- Bedrock model: `amazon.nova-lite-v1:0`

## Live judge-path result

The live Strands invocation returned HTTP 200 and produced the intended safe proposal:

- Pet: Pika
- Trusted carer: Neighbor A
- Dinner: CaniBowl Chicken 100g
- Target: 19:00
- Owner Approval Required: Yes

## Observability

CloudWatch runtime logs recorded successful invocations, including the final judge-path session completing successfully in approximately 2.666 seconds.

## What this proves

The agent path is not only a static UI fixture. The deployed path reaches Amazon Bedrock AgentCore, executes a Strands agent, uses Bedrock for reasoning, and preserves the human approval boundary before consequential care handoff.
