# Slide 03 — Terranetes Takeaway

**Type:** Synthesis — when Terranetes is the right choice  
**Design:** Light slide, heading "MEET TEAMS WHERE THEY ARE." three-point summary + migration path note

---

## Key Message

Terranetes is the pragmatic on-ramp for organisations with significant Terraform investments. It adds platform control, policy gates, and GitOps delivery without demanding a migration. Over time, modules can be migrated to ASO or Crossplane as the platform matures.

---

## Talking Points

"Terranetes is the most pragmatic tool in this set — and sometimes that's exactly what you need."

"*No rewrite required.* Your Terraform modules work as-is. The team that built and maintains them doesn't need to learn Crossplane or ASO. They keep writing Terraform. The platform team wraps it."

"*Policy gates are a first-class feature.* Require approval before any Terraform runs. Restrict which modules can be used. Enforce cost controls. These gates live in Kubernetes policies, not in CI scripts, not in a separate governance tool."

"*The migration path is gradual.* You can start with Terranetes for everything today. As specific resource types mature and the team gains confidence, migrate those to ASO or Crossplane — driven by real need, not by an arbitrary deadline."

"*When NOT to use Terranetes:* When you're starting fresh and have no Terraform investment. In that case, the overhead of running Terraform inside Kubernetes is unnecessary — go straight to ASO or Crossplane."

"The honest framing: Terranetes is an excellent bridge. It may not be the final destination for every resource type — but it's often the right first step for organisations that can't afford to pause and rewrite everything before the platform delivers value."

---

## Transition

→ Next: Sovereignty, AI, and what ties it all together
