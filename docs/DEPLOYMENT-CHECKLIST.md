# CaniFriend v0.1 — Deployment Checklist

Target: `canifriend.canibowl.my`

## Vercel project

Create a NEW Vercel project for this repo. Do not reuse CAIOS or WebMCP projects.

Repository:

`corwinlim/CaniFriend-v0.1`

Recommended project name:

`canifriend-v0-1`

Framework preset:

`Other` / static site

Root directory:

Repository root

Build command:

Leave empty

Output directory:

Leave empty

Install command:

Leave empty

`vercel.json` already rewrites `/` to `/web/demo.html`.

## Domain

After the production deployment is READY, add:

`canifriend.canibowl.my`

Then add the DNS value Vercel provides in the `canibowl.my` DNS zone. Do not replace unrelated records.

## Verification after deploy

Open the production URL and verify all five screens:

1. Care Need
2. Smart Match
3. Human Approval
4. Care Mission
5. Proof & Memory

Verify these exact visible strings:

- `Pika needs dinner tonight.`
- `I can't get home tonight. Make sure Pika gets dinner.`
- `Neighbor A · Recommended`
- `Owner Approval Required`
- `CARE COMPLETE ✓`
- `CAIOS CareEvent`

Also verify:

- `Reset Demo` returns to Screen 1
- Agent trace remains readable at desktop recording width
- no secrets or AWS account identifiers are visible
- mobile view remains usable
- production URL opens without Vercel authentication

## Live AgentCore mode

The static demo is recording-safe by default.

To use a browser-callable live API, the URL can accept an API parameter:

`/?api=<BFF invocation endpoint>`

Do not expose AWS credentials or sign AgentCore directly in browser JavaScript. The public browser endpoint should be a BFF/proxy that performs server-side authorization.

If live API is unavailable during recording, the UI labels the path `Demo fallback`. Do not describe fallback output as a live model invocation. Show the separately captured AWS production proof instead.

## Submission deployment gate

Deployment is READY only when:

- production Vercel URL loads
- custom domain loads
- five-screen path works
- no authentication wall
- no console-breaking errors
- repo is public
- live/fallback state is truthfully labeled
