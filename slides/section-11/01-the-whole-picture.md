# Slide 01 — The Whole Picture

**Type:** Architecture synthesis — the complete platform stack  
**Design:** Dark slide, full-width architecture diagram: Git → Argo CD → Kubernetes API → four provisioning tools → Azure

---

## Key Message

The complete platform is a layered architecture: Git as source of truth, Argo CD as the delivery engine, the Kubernetes API as the unified control plane, and four provisioning tools covering every infrastructure scenario. Developers interact with simple CRs; the platform delivers Azure resources consistently and safely.

---

## Talking Points

"Let's put it all together."

"At the top: Git. Every infrastructure intent — every application manifest, every database request, every policy — starts as a commit in Git. Immutable, auditable, reversible."

"Below that: Argo CD. It watches Git and continuously reconciles the cluster to match. It doesn't matter what kind of resource it's applying — Crossplane Composition, ASO manifest, KRO ResourceGroup, Terranetes Configuration. Argo CD delivers it."

"In the middle: the Kubernetes API. This is the unified control plane. The single entry point for everything. Every team, every tool, every automation goes through here."

"Below the API: the four provisioning tools. Each one owns its lane. ASO owns direct Azure resource management. Crossplane owns high-level platform abstractions. KRO owns app-level composition. Terranetes owns existing Terraform modules."

"At the bottom: Azure. The actual cloud infrastructure. Managed identities, databases, storage, container registries — all provisioned by the tools above, all tracked by the control plane above that."

"Two kinds of people interact with this stack. Developers see simple custom resources — AppDatabase, AppEnvironment, StorageConfig. They don't see Azure. They don't run Terraform. They apply YAML and the platform handles the rest."

"Platform teams see the other side — Compositions, ResourceGroups, Terranetes policies, ApplicationSets, Argo CD apps. They build and maintain the abstractions. They set the guardrails. They own the control plane."

---

## Transition

→ Next: Closing
