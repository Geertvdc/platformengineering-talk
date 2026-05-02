# Slide 03 — Crossplane Takeaway

**Type:** Synthesis — when Crossplane is the right choice  
**Design:** Light slide, heading "OWN YOUR ABSTRACTION." three-point summary + when not to use callout

---

## Key Message

Crossplane is for when the platform team wants to fully own the API contract between developers and infrastructure. The investment is higher than ASO, but the payoff is a cloud-agnostic, opinionated platform API that encodes all your standards automatically.

---

## Talking Points

"What do you take away from that demo?"

"*Crossplane is a platform investment, not a quick win.* Writing good Compositions takes time. You're designing an API, not just writing YAML. But once it's done, it runs forever — and every team that joins gets the same experience."

"*Crossplane decouples developer experience from cloud implementation.* Today it's Azure PostgreSQL. Tomorrow you could swap the Composition to provision on a different service, and the developer manifest doesn't change. That's genuine abstraction."

"*Crossplane enforces platform standards automatically.* Backup policies, tagging, naming, networking — baked into the Composition. No pull request review required to catch a developer who forgot to enable backups. The platform makes it impossible to get it wrong."

"*When NOT to use Crossplane:* When your team is small, Azure-native, and doesn't need to hide cloud complexity. The overhead of designing XRDs and Compositions is real. ASO or KRO may be a better fit until the platform matures."

"Crossplane is the right choice when you're building a platform that will serve many teams over many years and you want the developer experience to be truly first-class."

---

## Transition

→ Next: Demo 3 — KRO
