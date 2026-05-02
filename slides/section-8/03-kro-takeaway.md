# Slide 03 — KRO Takeaway

**Type:** Synthesis — when KRO is the right choice  
**Design:** Light slide, heading "COMPOSE WITHOUT COMPLEXITY." three-point summary + pairing callout

---

## Key Message

KRO is the right choice when you want app-level self-service without building full Crossplane compositions. It's simpler to learn, pairs naturally with ASO, and is ideal for teams that want to bundle multiple Kubernetes resources behind a single developer-facing CR.

---

## Talking Points

"KRO's superpower is simplicity at the right level."

"*KRO is fast to adopt.* The ResourceGroup format is straightforward. If you already understand Kubernetes resource definitions, you can write a KRO template in an afternoon. Crossplane Compositions have a steeper learning curve."

"*KRO is honest about what it is.* It's composition, not abstraction. The developer CR expands into Kubernetes resources — you can see exactly what was created. There's no magic provider layer. That transparency is a feature."

"*KRO pairs naturally with ASO.* ASO handles the Azure side; KRO handles the app assembly. Together they give you a complete app-provisioning story without needing Crossplane."

"*When NOT to use KRO:* When you need to hide cloud-provider details completely, or when your compositions need complex conditional logic or multi-step provisioning workflows. Those cases push you toward Crossplane."

"The practical sweet spot: use KRO for app-level bundles, ASO for the Azure resources inside them, and introduce Crossplane when the abstraction requirements grow beyond what KRO can cleanly express."

---

## Transition

→ Next: Demo 4 — Terranetes
