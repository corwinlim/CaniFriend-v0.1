# CaniFriend — Devpost Final Submission Pack

Hackathon: Agents for Humans Hackathon
Track: Good Neighbor Agents

## Project

**Name:** CaniFriend

**Tagline:** When you can't be there, your neighborhood can.

## Public repository

https://github.com/corwinlim/CaniFriend-v0.1

> Submission requirement: repository visibility must be PUBLIC before final submission.

## Architecture diagram

Upload one of:

- `docs/CaniFriend-Architecture.pdf`
- `docs/CaniFriend-Architecture.png`

## Submitter fields

- Submitter Type: Individual
- Country of Residence: Malaysia
- Track: Good Neighbor Agents
- Organization: leave blank unless submitting on behalf of Absolute Global Resources PLT

## Testing instructions

Use the five-screen Judge Recording Mode from the deployed web demo.

1. Start at the CaniFriend home screen with Pika.
2. Confirm the owner request reads: `I can't get home tonight. Make sure Pika gets dinner.`
3. Select **Find someone I trust**.
4. Confirm **Neighbor A** is ranked as the strongest trusted match and Pika's dinner is **CaniBowl Chicken 100g** for **7:00 PM**.
5. Continue to the approval screen and verify **Owner Approval Required** is shown before any consequential handoff.
6. Approve the plan. Confirm the care mission transitions from proposed to approved/accepted.
7. Complete the care task and verify **CARE COMPLETE** with feed, water, condition and proof checks.
8. Confirm the final outcome is written as a **CAIOS CareEvent**.

Safety invariant to verify: **AI recommends. Policy authorizes. Human approves consequential care handoffs.**

The LLM cannot approve a care plan, accept on behalf of a carer, complete physical care, or write the final authoritative outcome.

## Demo video checklist

Maximum 5 minutes. Recommended cut: 90 seconds.

- 0–10s: Problem — owner cannot get home; Pika still needs dinner.
- 10–20s: Exact owner request.
- 20–32s: Pet context retrieval.
- 32–45s: Neighbor A trusted match.
- 45–57s: Owner Approval Required.
- 57–70s: Care mission.
- 70–82s: Care complete + proof.
- 82–90s: CAIOS outcome + closing line.

Video must clearly cover:

1. the problem,
2. who it is for,
3. why it matters,
4. a working product demonstration.

## Built with

- Strands Agents SDK
- Amazon Bedrock AgentCore Runtime
- Amazon Bedrock
- Amazon Nova Lite
- AWS CodeBuild
- Amazon ECR
- Amazon CloudWatch
- Python
- JavaScript
- HTML/CSS
- Vercel (optional live demo)

## Production proof

See:

- `docs/LIVE-PROOF.md`
- `docs/OBSERVABILITY-PROOF.md`
- `docs/TEST-PROOF.md`
- `docs/ARCHITECTURE.md`

Verified judge-path result:

- Pet: Pika
- Trusted carer: Neighbor A
- Dinner: CaniBowl Chicken 100g
- Target: 19:00
- Owner Approval Required: Yes
- Agent mode: Strands
- AgentCore Runtime status: READY

## Remaining values required before final submit

- AWS Builder ID: **REQUIRED — user-provided real ID only**
- Demo video URL: **REQUIRED — public YouTube or Vimeo URL**
- Architecture diagram upload: **REQUIRED**
- GitHub repository visibility: **REQUIRED PUBLIC**
- Live demo URL: optional, but recommended for Technical Implementation score

## Final positioning

CaniFriend is not a pet-sitter marketplace. It is an AI-coordinated trusted-neighborhood care network that converts a real-world care need into a safe, auditable handoff:

**Need → Reason → Match → Human Approval → Coordinate → Care → Verify → Remember**

One pet. One missed dinner. One trusted neighbor. One agent completes the entire handoff.