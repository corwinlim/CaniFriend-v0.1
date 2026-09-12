# CaniFriend v0.1 Architecture

```text
Pet Owner
   |
   v
CaniFriend Web / BFF
   |
   v
Amazon Bedrock AgentCore Runtime (HTTP)
   |
   v
Strands CaniFriend Care Agent
   |
   +--> get_pet_context
   +--> find_trusted_carers
   +--> create_care_plan
   |
   v
PROPOSED CARE PLAN
   |
   v
HUMAN OWNER APPROVAL GATE
   |
   v
Carer accepts → performs care → submits proof
   |
   v
Verified outcome
   |
   v
CAIOS authoritative CareEvent
```

## Trust boundary

**AI recommends. Policy authorizes. Human approves consequential handoff.**

The Strands agent can retrieve minimum-necessary pet context, evaluate trusted carers, and create a proposed care plan. It cannot approve the owner handoff, accept on behalf of the carer, complete physical care, or write the authoritative CAIOS outcome.

## Memory boundary

Agent context and community reliability can be retained as agent memory. The authoritative pet-care event remains in CAIOS as the system of record.
