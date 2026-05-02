# Slide 01 — Demo: KRO — Compose Multi-Resource App Concepts

**Type:** Demo intro — what KRO is and the gap it fills  
**Design:** Dark slide, large "KRO." heading, subtitle "ONE CR. MANY RESOURCES."

---

## Key Message

KRO (Kubernetes Resource Orchestrator) lets you bundle multiple Kubernetes resources into a single custom resource called a ResourceGroup. It fills the gap between raw ASO manifests and full Crossplane compositions — simpler to write, but powerful enough for app-level self-service.

---

## Talking Points

"So we have ASO for direct Azure control, and Crossplane for full platform API ownership. KRO sits in the middle — and I think it's underrated."

"The problem KRO solves: in real platforms, self-service is rarely 'give me one resource.' It's 'give me everything my service needs to exist.' A namespace. RBAC. A managed identity. A database. A Key Vault reference. All wired together."

"Without KRO, you either write all of that separately and hope the developer applies them in the right order — or you build a Crossplane Composition, which is powerful but has a learning curve."

"KRO lets you define a ResourceGroup: a template that expands one developer-facing CR into all the Kubernetes resources that service needs. It's closer in spirit to Helm — but without the templating gymnastics, and with first-class Kubernetes API integration."

"It's a CNCF Sandbox project but it's moving fast, and for teams already using ASO it's a very natural pairing — KRO handles the app-level assembly, ASO handles the Azure provisioning."

---

## Transition

→ Next: Demo — one KRO ResourceGroup CR provisions namespace + identity + ASO database
