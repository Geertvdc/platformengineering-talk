# Slide 03 — ASO Takeaway

**Type:** Synthesis — when ASO is the right choice  
**Design:** Light slide, three-point summary with a "when to use / when not to use" framing

---

## Key Message

ASO is the right choice for Azure-first teams who want GitOps control over Azure resources without building custom abstractions. It's the lowest-overhead path to infrastructure-as-code in a Kubernetes platform. Its limitation is that it doesn't hide Azure — which is exactly right for some teams and wrong for others.

---

## Talking Points

"What did we learn from that demo?"

"*ASO is fast to start with.* You install the operator, configure identity, and you're provisioning resources. No custom schemas, no platform API to design. Day-one productivity is high."

"*ASO is transparent.* The developer writing the manifest knows they're provisioning an Azure resource. That's a feature for some teams — Azure engineers feel at home. It's a liability for others — if you want to hide Azure behind a platform API so developers don't need Azure knowledge, ASO alone isn't the answer."

"*ASO composes well.* It pairs naturally with KRO — you define a ResourceGroup in KRO that creates a namespace, assigns RBAC, and provisions an ASO database, all as one custom resource. That gives you a higher-level developer experience on top of ASO's direct Azure control."

"*When NOT to use ASO alone:* When you want the developer experience to be cloud-agnostic or when your platform needs to encode complex opinions that aren't expressible as simple resource properties. That's when Crossplane's composition model becomes more appropriate."

"Bottom line: if your team thinks in Azure, speaks YAML, and wants to move fast — ASO is your fastest path to GitOps-controlled infrastructure."

---

## Transition

→ Next: Demo 2 — Crossplane
