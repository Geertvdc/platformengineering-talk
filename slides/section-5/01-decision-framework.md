# Slide 01 — Decision Framework: Which Tool for Which Problem

**Type:** Framework overview — the decision table  
**Design:** Light slide, table layout with four tools as rows, three dimensions as columns

---

## Key Message

Four tools, four different answers to the same question: how do I provision infrastructure through my Kubernetes platform? The right choice depends on abstraction level, team skills, and whether you're building net-new or integrating existing assets.

---

## Talking Points

"Let's put the four tools side by side. This is the question I get most: which one should I use?"

"The honest answer is: it depends. But here's the framework."

"*ASO — Azure Service Operator.* Maintained by Microsoft. Maps Azure resources directly to Kubernetes CRDs. You write YAML, Azure resources appear. Low abstraction — it looks a lot like Azure ARM, just in Kubernetes. Best choice when your team is Azure-native and you want direct GitOps control without building your own API."

"*Crossplane.* High abstraction. The platform team writes Compositions — complex, reusable templates that encode your platform standards. Developers see only a simple custom resource: give me a database. They don't know or care how it's provisioned. Best choice when you want to hide the complexity and own your abstraction layer completely."

"*KRO — Kubernetes Resource Orchestrator.* Medium abstraction. You define a ResourceGroup — a bundle of multiple Kubernetes resources that deploy as one unit. Simpler than Crossplane, but powerful enough to compose app-level concepts. Best choice when you want self-service for whole app setups without building full Crossplane compositions."

"*Terranetes.* Bridges Terraform and Kubernetes. Your existing Terraform modules run as Kubernetes-controlled jobs, with policy gates before they apply. Best choice when you have Terraform you trust and want to bring it into the platform without a rewrite."

"And again: Argo CD sits under all of them. It's the delivery mechanism, not the provisioning tool."

---

## Transition

→ Next: Let's look at each one with a demo, starting with ASO
