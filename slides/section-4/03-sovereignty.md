# Slide 03 — Sovereignty

**Type:** Nuance slide — compliance and control as a design input  
**Design:** Dark slide, impact word "SOVEREIGNTY." with three bullet callouts

---

## Key Message

Sovereignty is not just a European legal concern — it's a design constraint that affects which tools you can use, where your state lives, and who controls the control plane. Keeping the platform API inside your own Kubernetes cluster is a deliberate choice with real consequences.

---

## Talking Points

"I want to spend a moment on sovereignty, because it comes up in almost every enterprise conversation in Europe — and it's often treated as a legal problem, not an architecture problem."

"Sovereignty in this context means: who controls the API? Where is the state? Who can see the audit trail? And what happens if a vendor goes away or changes their pricing?"

"When your platform is built on Kubernetes — and your infrastructure tools run as Kubernetes operators — the control plane is inside your cluster. You own it. You can air-gap it, inspect it, back it up, move it. Your Git repository is the source of truth and it lives wherever you put it."

"Compare that to a managed platform-as-a-service where all your resource definitions are stored in the vendor's backend. If they have an outage, your deployments stop. If they change their API, your automation breaks. If you want to migrate, you're starting from scratch."

"I'm not saying SaaS is wrong. I'm saying: know what you're trading. Sovereignty is a dial, not a switch — but you have to turn it deliberately."

"The four tools we'll look at all share one property: they run inside your Kubernetes API. The control plane stays with you."

---

## Transition

→ Next: The flexible control plane — four tools, four angles
