# CaniFriend Observability Proof

Verified on 2026-09-12.

## Runtime telemetry

Amazon CloudWatch logs are enabled for the deployed Amazon Bedrock AgentCore Runtime used by CaniFriend.

Log group:

`/aws/bedrock-agentcore/runtimes/CaniFriendRuntime-k6Ik8Q9n01-DEFAULT`

Observed successful sessions:

- Health check session: success, approximately 0.000 s
- Live agent session `canifriend-agent-session-20260912-0002`: success, approximately 1.951 s
- Final judge-path session `canifriend-agent-session-20260912-0003`: success, approximately 2.666 s

## What the final trace proves

The final judge-path request reached the deployed AgentCore Runtime, executed the Strands orchestration path, selected Neighbor A for Pika's dinner mission, preserved the 19:00 target and CaniBowl Chicken 100g feeding context, and stopped at the human approval boundary with `Owner Approval Required: Yes`.

## Judge-safe interpretation

CaniFriend exposes decision and tool outcomes for auditability without displaying hidden model chain-of-thought. The useful proof is the structured sequence of request, tool calls, proposed plan, approval boundary, action state, verified outcome, latency, and errors.

## Safety boundary

**AI recommends. Policy authorizes. Human approves consequential care handoffs.**

The model cannot approve the owner handoff, accept on behalf of a carer, complete physical care, or write the authoritative CAIOS CareEvent.