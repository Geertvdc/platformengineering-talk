# Slide 01 — Demo: ASO — Azure Resources as Kubernetes CRDs

**Type:** Demo intro — what ASO is and why it matters  
**Design:** Dark slide, large "ASO." heading, Microsoft logo / Kubernetes logo pairing, subtitle

---

## Key Message

Azure Service Operator (ASO) is maintained by Microsoft and lets you manage Azure resources directly through Kubernetes manifests. Apply YAML, get an Azure resource. Delete YAML, the Azure resource is gone. It's the lowest-friction on-ramp for Azure-native teams who want GitOps control.

---

## Talking Points

"Let's start with ASO — Azure Service Operator. This one is maintained by Microsoft, which is significant. It's not a community project you need to worry about support and longevity for. Microsoft uses it internally and is actively developing it."

"What ASO does is conceptually very simple: it maps Azure ARM resource types directly to Kubernetes custom resource definitions. Every resource you can create in Azure — storage accounts, databases, container registries, key vaults — has a corresponding CRD in your cluster."

"You write a Kubernetes manifest. The ASO controller reads it and calls the Azure API on your behalf. The resource appears in Azure. Delete the manifest, the resource gets deleted. Update the manifest, the resource gets updated."

"For teams that already think in Azure terms — who know what a storage account needs, who understand managed identities and resource groups — this is the most natural path into GitOps-controlled infrastructure. There's no new abstraction to learn. The concepts are the same Azure concepts you already know, just expressed as YAML."

"Let me show you what that looks like."

---

## Transition

→ Next: Demo in terminal
