# The Daily Journal

Copy this template into `docs/journal/day-NN.md` every morning. Fill it as you
go, not at 5:55pm from memory.

**Time budget: 20 minutes a day.** If it's taking an hour you're writing a
transcript instead of a journal — see §"What this is not" below.

**This is graded**, and it carries real weight in the final assessment. A
working system built by copy-pasting a tutorial and a working system built with
understanding look identical in a demo. They look nothing alike in a journal.

---

## The template

```markdown
# Day NN — <topic>

**Date:** YYYY-MM-DD
**Spend so far:** $XX.XX  (yesterday: $XX.XX — delta: $X.XX)
**Resources currently running:** <one line, e.g. "2 × B1s VM, 1 LB, 1 public IP">

---

## What I built

<Two or three sentences. What exists now that didn't exist this morning?>

## The thing that took longest

<What ate the most time today, and why? Be honest — "I misread the
docs for 40 minutes" is a perfectly good and useful entry.>

## What broke, and what I learned

For each failure, including the deliberate ones:

### 🔴 <short name for the failure>

- **What I expected to happen:**
- **What actually happened:** (paste the real error, not a paraphrase)
- **What I thought was causing it:** ← fill this in BEFORE you find the answer
- **What was actually causing it:**
- **How I found out:**
- **What I'd check first if I saw this again:**

## Concepts I can now explain to someone else

<Bulleted. Only list things you could genuinely explain out loud, without
notes, to another intern. If you can't, it goes in the next section instead.>

## ❓ What I still don't understand

<THE MOST IMPORTANT SECTION. Be specific. See guidance below.>

## Commands / snippets worth keeping

<Things you'll want again. Not everything you ran — the ones that
were non-obvious.>

## Tomorrow

<One line.>
```

---

## Filling in "what I thought was causing it"

This field is the reason the journal exists, and it is the one people skip.

You must write it **before** you find the actual answer. Not after. The moment
you know the real cause, your memory of what you believed five minutes ago
quietly rewrites itself — this is well-documented and it happens to everyone,
including people who know it happens.

The gap between your hypothesis and reality is the *entire* learning signal. If
you only record the fix, you've built a lookup table of symptoms, not a model of
the system. Lookup tables don't transfer to the next problem; models do.

**Weak entry:**
> The app wasn't reachable. I fixed the NSG rule.

**Strong entry:**
> - **Expected:** `curl http://<public-ip>` returns the homepage.
> - **Actually:** hung for 30s, then `Connection timed out`.
> - **I thought:** the app had crashed, or uvicorn was bound to 127.0.0.1
>   instead of 0.0.0.0. I'd read about that failure mode.
> - **Actually:** uvicorn was fine — `curl localhost:8000` worked *from inside*
>   the VM. The NSG had no inbound rule for port 80 at all, so the packet was
>   dropped before it ever reached the VM.
> - **How I found out:** the "connection timed out" vs "connection refused"
>   distinction. *Refused* means something answered and said no — the packet
>   arrived. *Timed out* means nothing answered at all, so the packet never
>   arrived. That points at the network, not the app.
> - **Next time:** timeout → suspect the network path (NSG, routing, wrong IP).
>   Refused → suspect the app (not running, wrong port, wrong bind address).

The second entry is worth more than the whole rest of the day. Notice that it
contains a *reusable diagnostic rule* that the first one doesn't.

---

## Filling in "what I still don't understand"

Your supervisor reads this section first. Treat it as a feature request queue,
not a confession.

**Good entries** (specific, actionable, teachable):

- "I got the private DNS zone working by following the docs, but I don't
  understand *why* the A record has to be in a zone linked to the VNet rather
  than just existing."
- "I know a Managed Identity means no password, but I don't understand what the
  app actually sends to Azure to prove who it is."
- "The Bicep deployed, but I don't know why `dependsOn` was needed in one place
  and not the other."

**Weak entries** (not actionable, and usually a sign of overload):

- "Networking."
- "Everything about Bicep."
- *(blank)*

**An empty section three days running is a problem, not an achievement.** It
means one of two things: you're not pushing into unfamiliar territory, or you've
stopped writing honestly. Neither is good, and your supervisor will read a blank
here as a signal to slow down and check in — which is exactly what should
happen.

Nobody is scored down for what's in this section. You *are* scored on whether
it's real.

---

## What this is not

- **Not a command log.** Your shell history already has that. Only record
  commands that were non-obvious or that you'll need again.
- **Not a tutorial rewrite.** Don't restate the lesson file. Record your
  *encounter* with it.
- **Not a performance.** Days where you got very little working and understood
  why are more valuable than days where everything worked and you don't know
  why. Write those days honestly.
- **Not written at the end of the day.** Keep it open in a split pane. Failures
  get recorded the moment they happen or they get recorded wrong.

---

## Weekly retrospective

At the end of each phase (days 6, 11, 16, 20), add
`docs/journal/phase-N-retro.md`:

```markdown
# Phase N retrospective

## The one-sentence summary of this phase

## Three things I can do now that I couldn't 5 days ago

## The single most surprising thing

## What I'd tell myself on day 1 of this phase

## Cost: $XX.XX  — was that worth it? What did I waste money on?

## The comparison table so far

| | Phase 1 (VMs) | Phase 2 (PaaS) | Phase 3 (Containers) |
|---|---|---|---|
| Time to first deploy | | | |
| Time to redeploy a code change | | | |
| What I control | | | |
| What I gave up | | | |
| Cost per month at idle | | | |
| What happens at 3am when it breaks | | | |

## Open questions I'm carrying into the next phase
```

**That comparison table is the spine of your final presentation.** Fill one
column at the end of each phase, while it's fresh. Trying to reconstruct the
Phase 1 column on day 20 from memory is both painful and inaccurate — you will
have forgotten how long the first VM deploy actually took, and you'll guess low.
