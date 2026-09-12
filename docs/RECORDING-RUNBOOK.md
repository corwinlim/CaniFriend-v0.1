# CaniFriend v0.1 — Judge Demo Recording Runbook

Use this runbook to record the final Agents for Humans submission video with the fewest possible cuts.

## Recording target

- Full submission video: 3:20–3:45
- Golden product path: about 90 seconds
- Product footage: about 75%
- Architecture + AWS proof: about 20%
- End card: about 5%

## Pre-flight

Before recording:

1. Browser zoom 100% and notifications off.
2. Open the CaniFriend demo at the Home / Care Need screen.
3. Reset demo state so no caregiver is confirmed.
4. Keep Pika, Neighbor A, 19:00, and CaniBowl Chicken 100g unchanged.
5. Prepare the architecture diagram in a second tab.
6. Prepare AWS proof in separate tabs: AgentCore Runtime READY and CloudWatch successful invocation.
7. Do not show credentials, account IDs, tokens, environment variables, IAM details, or private URLs.

## Take A — opening + live product flow

Record this as one continuous take if possible.

### Opening

Start on Pika's Home screen:

- `Pika needs dinner tonight.`
- `No caregiver confirmed`
- `Find someone I trust`

Narration:

> Pet care often depends on one or two people. When they suddenly can't get home, the backup plan is usually a message and hope. CaniFriend turns that uncertainty into a trusted, AI-coordinated care handoff.

### Owner request

Enter or reveal:

> I can't get home tonight. Make sure Pika gets dinner.

Click `Find someone I trust`.

Narration:

> I simply tell CaniFriend what happened. The agent understands the care need and retrieves only the context required for tonight's task.

### Context

Pause long enough to show:

- Pika
- CaniBowl Chicken
- 100g
- 7:00 PM
- Refresh water
- Check general condition

Narration:

> It knows Pika's dinner is CaniBowl Chicken, one hundred grams, around seven PM, without exposing Pika's full private history.

### Trusted match

Pause on Neighbor A and make these fields readable:

- Available tonight
- Authorized for feeding
- High familiarity
- 8 previous care tasks
- 100% completion

Narration:

> The Strands agent evaluates Pika's existing trusted care network. It recommends Neighbor A because they are available, already know Pika, are authorized for feeding, and have completed eight previous care tasks.

### Human approval gate

Pause for at least three seconds on:

`Owner Approval Required`

Narration:

> This is where AI stops. The agent can recommend a plan, but it cannot authorize someone to care for my pet.

Click `Approve Care Plan`.

Narration:

> AI recommends. Policy authorizes. Human approves.

Wait for:

- `OWNER APPROVED`
- `Neighbor A accepted`

### Care mission

Switch to the helper mission. Show:

- Pika's Dinner
- CaniBowl Chicken 100g
- Feed Pika
- Refresh water
- Check general condition

Check the tasks and click `Complete Care + Proof`.

Narration:

> Neighbor A receives only the minimum necessary instructions, completes the physical care, and returns proof and an observation.

### Verified outcome

Pause on:

- CARE COMPLETE
- Fed 7:04 PM
- Water refreshed
- Condition normal
- Proof received
- CAIOS CareEvent recorded

Narration:

> The completed outcome is then recorded into CAIOS as part of Pika's longitudinal care history.

## Take B — architecture

Show the architecture diagram for roughly 15–20 seconds.

Narration:

> Behind the interface, CaniFriend runs a Strands agent on Amazon Bedrock AgentCore. The agent can interpret the request, retrieve context, evaluate trusted carers, and create a proposal. Owner approval, carer acceptance, physical completion, and the authoritative CAIOS outcome remain outside the LLM's authority.

Point visually through:

`Owner → CaniFriend → AgentCore → Strands → Safe Tools → Human Approval → Care Mission → CAIOS`

## Take C — AWS production proof

Use quick cuts only.

Show:

1. `CaniFriendRuntime — READY`
2. Live judge result: `Neighbor A / 19:00 / CaniBowl Chicken 100g / Owner Approval Required: Yes`
3. CloudWatch: `Invocation completed successfully`

Narration:

> This is not a mocked agent response. The ARM64 image was built on AWS CodeBuild and deployed to Amazon Bedrock AgentCore. The live Strands invocation selected Neighbor A, preserved the correct dinner context, and kept the human approval requirement intact.

Do not linger in AWS Console or expose sensitive account information.

## Take D — close

Return to Pika or a clean CaniFriend end card.

On screen:

`When you can't be there, your neighborhood can.`

Narration:

> AI can reason about what a pet needs, but real-world care still needs trusted humans. CaniFriend turns neighbors into an AI-coordinated care network for pets. When you can't be there, your neighborhood can.

## Must-show judge evidence

The final edit is not ready unless all of these are visible:

- Natural-language owner request
- Pet-specific context
- Trusted-carer recommendation and reason
- `Owner Approval Required`
- Explicit owner approval
- Carer mission
- Completed care + proof
- CAIOS outcome
- Strands / AgentCore architecture
- Runtime READY
- Successful live invocation / CloudWatch evidence

## Do not show

- Hidden chain-of-thought
- AWS credentials or secrets
- Private health records beyond the task
- Claims of autonomous home access
- Claims that the LLM itself completed physical care
- Long terminal or AWS setup footage

## Recovery if the live model is slow

Do not restart the entire recording. Hold the loading state for a few seconds, then cut to the successful result. The product's deterministic state machine may be used for the post-approval mission flow, but do not label a deterministic fallback as a live model invocation.

## Final end card

**CaniFriend**

**When you can't be there, your neighborhood can.**

Powered by Strands Agents SDK + Amazon Bedrock AgentCore + CAIOS
