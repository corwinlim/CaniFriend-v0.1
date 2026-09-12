# CaniFriend v0.1 — Demo Screenplay

**Track:** Agents for Humans / Good Neighbor Agents  
**Target:** 3:15–3:45 full submission video  
**Golden product demo:** ~90 seconds  
**Primary line:** **When you can't be there, your neighborhood can.**

## 0:00–0:18 — The human problem

**Screen:** Cream opening frame → Pika home screen. Show `Pika needs dinner tonight` and `No caregiver confirmed`.

**Voiceover:**

“Pet care often depends on one or two people. But when work runs late, travel changes, or an emergency happens, the backup plan is usually just a message to someone… and hope.”

On-screen: `A real-world coordination problem`

## 0:18–0:33 — Introduce CaniFriend

**Screen:** CaniFriend / Pika profile. Reveal:

`Need → Reason → Match → Approve → Care → Verify → Remember`

**Voiceover:**

“We built CaniFriend as an AI neighborhood care network for pets. Instead of simply answering a question, the agent understands the care need, finds someone already trusted by the pet owner, coordinates the handoff, and closes the care loop.”

## 0:33–0:48 — The ask

**Screen:** Enter:

`I can't get home tonight. Make sure Pika gets dinner.`

Click `Find someone I trust`.

Show `Understanding Pika's care need…` then `Finding someone Pika already knows…`

**Voiceover:**

“I simply tell CaniFriend: ‘I can't get home tonight. Make sure Pika gets dinner.’ CaniFriend retrieves only the context needed for this task.”

## 0:48–1:03 — Minimum-necessary pet context

**Screen:**

- Pika
- CaniBowl Chicken — 100g
- Target — 7:00 PM
- Refresh water
- Check general condition

**Voiceover:**

“The agent knows Pika's dinner is CaniBowl Chicken, one hundred grams, around seven PM. It doesn't expose Pika's entire history. It uses only the minimum necessary care context.”

## 1:03–1:25 — Trusted match

**Screen:** Recommended Match → **Neighbor A**

- Available tonight ✓
- Authorized for feeding ✓
- Pika familiarity: High
- Previous care tasks: 8
- Completion: 100%

Reason: `Available, authorized, familiar with Pika, 8 successful previous care tasks.`

**Voiceover:**

“CaniFriend doesn't search an anonymous marketplace. The Strands agent evaluates Pika's existing trusted care network. It recommends Neighbor A because they're available tonight, Pika already knows them, they're authorized for feeding, and they've successfully completed eight previous care tasks. This is where AI stops.”

## 1:25–1:43 — Human approval gate

**Screen:**

`You stay in control.`

`Neighbor A · Feed Pika · 7:00 PM`

`Owner approval required`

Click **Approve Care Plan**.

Then show `OWNER APPROVED ✓` and `Neighbor A accepted ✓`.

**Voiceover:**

“The agent can recommend a care plan. But it cannot authorize someone to care for my pet. That consequential decision requires explicit owner approval.”

Hold this line for at least three seconds:

**AI recommends. Policy authorizes. Human approves.**

## 1:43–2:02 — Care mission

**Screen:** Neighbor A view → Pika's Dinner.

- CaniBowl Chicken — 100g
- Feed Pika
- Refresh water
- Check general condition

Check all three, then click `Complete Care + Proof`.

**Voiceover:**

“Neighbor A receives a simple care mission—not Pika's full private record. They know exactly what to do: feed one hundred grams, refresh the water, and check Pika's condition.”

## 2:02–2:19 — Close the loop

**Screen:**

`CARE COMPLETE ✓`

- Fed — 7:04 PM
- Water — Refreshed ✓
- Condition — Normal ✓
- Proof — Received ✓
- CAIOS CareEvent recorded

**Voiceover:**

“When the task is complete, CaniFriend verifies the outcome and records the care event back into CAIOS. The outcome becomes part of Pika's longitudinal memory.”

On-screen: `Need → Human → Action → Outcome → Memory`

## 2:19–2:42 — Show the real agent architecture

**Screen:** Architecture diagram. Highlight:

`Owner → CaniFriend Web → AgentCore Runtime → Strands Care Agent → Safe Tools → Human Approval → Care Outcome → CAIOS`

**Voiceover:**

“Behind the interface, CaniFriend runs a real Strands agent on Amazon Bedrock AgentCore. The agent can understand the request, retrieve Pika's context, evaluate trusted carers, and propose a plan. But approval, carer acceptance, physical completion, and the authoritative CAIOS write are deliberately kept outside the LLM's authority.”

## 2:42–3:02 — AWS production proof

**Screen, quick cuts only:**

1. `CaniFriendRuntime — READY`
2. `Live Invocation — HTTP 200`
3. `Neighbor A · 19:00 · CaniBowl Chicken 100g`
4. `Owner Approval Required: Yes`
5. CloudWatch: `Invocation completed successfully`

**Voiceover:**

“This isn't a mocked agent response. The CaniFriend ARM64 image was built on AWS CodeBuild and deployed to Amazon Bedrock AgentCore. Our live Strands invocation successfully selected Neighbor A, produced the correct dinner plan, and preserved the human approval requirement.”

## 3:02–3:24 — Why this matters

**Screen:** Three escalation cards: Trusted Neighbor → Professional Help → Emergency/Vet. Then ecosystem: `CAIOS remembers · CARLI watches · CaniFriend brings help`.

**Voiceover:**

“AI can reason about what a pet needs. But AI cannot physically feed the pet, walk the dog, or drive an animal to a clinic. Real-world care needs AI, trusted humans, devices, and memory working together. CaniFriend is our human execution layer.”

## 3:24–3:38 — Ending

**Screen:** Pika + CaniFriend logo.

# When you can't be there,
# your neighborhood can.

Powered by Strands Agents SDK · Amazon Bedrock AgentCore · CAIOS

**Voiceover:**

“CaniFriend turns neighbors into a trusted AI-coordinated care network for pets. When you can't be there, your neighborhood can.”

---

# 90-second golden cut

**0–10s:** Problem: pet care depends on one or two people; when they cannot get home, the backup plan is often a message and hope.

**10–20s:** Enter `I can't get home tonight. Make sure Pika gets dinner.`

**20–32s:** Show Pika, CaniBowl Chicken 100g, 7 PM, and `Finding someone Pika already knows…`

**32–45s:** Show Neighbor A: available, high familiarity, 8 previous tasks, 100% completion.

**45–57s:** Hold `Owner Approval Required`; click Approve Care Plan. Narrate: “The agent recommends. The owner authorizes.”

**57–70s:** Neighbor mission: Feed Pika, Refresh water, Check condition → Complete Care + Proof.

**70–82s:** `CARE COMPLETE ✓`, Fed 7:04 PM, Water refreshed, Condition normal, CAIOS CareEvent recorded.

**82–90s:** CaniFriend end card: `When you can't be there, your neighborhood can.`

## Recording rules

- Keep the first 33 seconds human and understandable; avoid infrastructure language.
- From 0:33 to 2:19 stay on the working product.
- Never expose chain-of-thought. Show concise decision reasons only.
- Hold `Owner Approval Required` for at least three seconds.
- AWS proof should be quick: Runtime READY → live result → CloudWatch success.
- Do not claim autonomous home access or broad health-record sharing.
