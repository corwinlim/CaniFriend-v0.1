# CaniFriend

**When you can't be there, your neighborhood can.**

CaniFriend is an AI-coordinated trusted-neighborhood care network for pets, built for the **Good Neighbor Agents** track of Agents for Humans.

## The 90-second story

A pet owner says:

> “I can't get home tonight. Make sure Pika gets dinner.”

CaniFriend retrieves Pika's minimum-necessary care context, finds an already-trusted and authorized neighbor, proposes a care plan, pauses for owner approval, coordinates the care mission, captures proof and an observation, and records the verified outcome back into the pet's longitudinal record.

## Why this is agentic

This is not a chatbot answer. The Strands agent performs real orchestration:

1. understand the care need,
2. retrieve pet context,
3. find eligible trusted carers,
4. propose the best care plan,
5. stop at a human approval boundary.

Consequential actions are intentionally outside the LLM toolset. The owner approves. The carer accepts and completes. The system validates transitions and records the final outcome.

## Architecture

![CaniFriend v0.1 architecture](docs/CaniFriend-Architecture.svg)

```text
CaniFriend Web
    |
    | POST /invocations
    v
AgentCore Runtime (HTTP)
    |
    v
Strands Care Agent
    |
    +--> get_pet_context ------> CAIOS context
    +--> find_trusted_carers --> CaniFriend trust graph
    +--> create_care_plan -----> PROPOSED
                                  |
                                  v
                           OWNER APPROVAL
                                  |
                                  v
                         carer accept / care
                                  |
                                  v
                         proof + CAIOS outcome
```

See `docs/ARCHITECTURE.md` for the trust and memory boundaries.

## Safety rule

> AI recommends. Policy authorizes. Humans approve consequential care handoffs.

The model cannot approve a care plan, accept on behalf of a carer, complete a care task, or write the final authoritative care outcome.

## Production proof

The current build has been verified through AWS CodeBuild → ECR → Amazon Bedrock AgentCore Runtime → Strands Agents SDK → Amazon Bedrock. The live judge-path invocation selected Neighbor A, preserved Pika's dinner context, and returned `Owner Approval Required: Yes`.

See `docs/LIVE-PROOF.md`, `docs/OBSERVABILITY-PROOF.md`, and `docs/DEMO-SCREENPLAY.md`.

## Repository map

```text
agent/      Strands agent, deterministic actions, audit, API adapters
web/        five-screen judge UI and live/fallback API client
shared/     stable data contracts
tests/      safety, runtime, state-transition, and web-contract tests
docs/       architecture, demo, observability, deployment, video, submission
infra/      AgentCore verification/deployment helpers
```

## License

MIT
