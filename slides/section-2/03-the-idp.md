# Slide 03 — The Internal Developer Platform

**Type:** Definition slide — what an IDP is  
**Design:** Could use a visual: layers or columns showing what the IDP sits between

---

## Key Message

The Internal Developer Platform (IDP) is the curated set of tools, workflows, and abstractions that developers self-serve from. It sits between the raw infrastructure and the developer.

---

## Talking Points

"The thing the platform team builds has a name: the Internal Developer Platform, or IDP."

"An IDP is not a portal. It's not a dashboard. It's not a ticketing system with a friendly UI. An IDP is the entire set of abstractions that sits between your developers and the raw infrastructure underneath."

"It might include: a way to request a namespace with the right RBAC policies already applied. A way to get a managed database that comes pre-configured with your organisation's backup and tagging standards. A deployment pipeline that bakes in your security scanning, your container policies, your approval gates."

"Developers don't need to know any of that is there. They just say 'I need a database' and they get one that already meets all your standards."

"And crucially — the IDP is the *product*. The Kubernetes cluster, the cloud resources, the GitOps tooling underneath — those are the implementation. Developers consume the IDP. They don't consume the implementation."

"This separation is important because it means you can change the implementation without changing the developer experience. You can swap out a tool, change a cloud provider, or add a new policy — and from the developer's perspective, nothing changed."

"And here's a thought that's increasingly relevant right now: AI coding agents. When a developer uses GitHub Copilot to generate a service, or an AI agent to scaffold infrastructure — what guardrails are in place? If your platform is just a wiki and a ticket queue, the answer is none. But if you have an IDP with well-defined abstractions, the AI agent operates inside those guardrails. It can only request what the platform allows. More on this later."

---

## Transition

→ Next: The golden path — how opinionated should the platform be?
