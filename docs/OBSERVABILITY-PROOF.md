# CaniFriend Observability Proof

Verified on 2026-09-12.

## Runtime telemetry

Amazon CloudWatch logs are enabled for the deployed Amazon Bedrock AgentCore Runtime used by CaniFriend.

The public repository intentionally omits account-specific log-group names, runtime IDs, session IDs, role identifiers, and control-plane resource identifiers. Those values are not needed to evaluate the agent behavior and should not become part of the public hackathon surface.

Observed successful runs included:

- Health check: success, approximately 0.000 s
- Live Strands agent invocation: success, approximately 1.951 s
- Final judge-path invocation: success, approximately 2.666 s

## What the final trace proves

The final judge-path request reached the deployed AgentCore Runtime, executed the Strands orchestration path, selected synthetic Neighbor A for synthetic Pika's dinner mission, preserved the 19:00 target and CaniBowl Chicken 100g feeding context, and stopped at the human approval boundary with `Owner Approval Required: Yes`.

## Judge-safe interpretation

CaniFriend exposes decision and tool outcomes for auditability without displaying hidden model chain-of-thought. The useful proof is the structured sequence of request, tool calls, proposed plan, approval boundary, action state, verified outcome, latency, and errors.

## Safety boundary

**AI recommends. Policy authorizes. Humans approve consequential care handoffs.**

The model cannot approve the owner handoff, accept on behalf of a carer, complete physical care, or write an authoritative CAIOS CareEvent by itself.

## Public evidence policy

Screenshots or recordings used for judging should likewise redact AWS account numbers, principal/role ARNs, registry URLs, temporary credentials, presigned URLs, request authorization headers, private endpoints, and unrelated production telemetry.
