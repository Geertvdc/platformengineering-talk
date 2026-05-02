# Slide 04 — GitOps

**Type:** Principle — Git as the single source of truth
**Design:** Light slide, big "GIT IS THE TRUTH." heading, four-principle list, watermark "GITOPS"

---

## Key Message

GitOps is four things, not one tool: declarative state, versioned in Git, pulled by an agent in the cluster, and continuously reconciled. Git becomes the audit log, the change-control system, and the rollback button — all at once.

---

## Talking Points

"GitOps isn't a product. It's a working model with four properties — and if any one of them is missing, you don't have GitOps, you have something that looks like it."

"*One: declarative.* The state of the system is described as data, not as a script you run."

"*Two: versioned in Git.* Every change to that state goes through a Git commit. Pull request, review, merge. That gives you the history, the author, the reason — for free, with tooling everyone already knows."

"*Three: pulled.* An agent inside the cluster watches Git and pulls changes. You don't push from CI into production. The cluster reaches out and asks, 'what should I look like right now?' That changes the security model — your CI never needs cluster credentials."

"*Four: continuously reconciled.* The agent doesn't just apply once and forget. It keeps checking. If someone manually changes something in the cluster, it gets reverted back to what Git says. Drift heals itself."

"Put those four together and Git becomes the platform's source of truth. Want to know what's running in production? Read the repo. Want to roll back a bad change? Revert the commit. Want to audit who changed what when? It's already there in `git log`."

"And the platform team's job becomes managing a Git repository — not running deploy commands at midnight."

---

## Transition

→ Next: How Argo CD makes this real
