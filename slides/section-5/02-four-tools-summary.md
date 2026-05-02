# Slide 02 — The Four Tools at a Glance

**Type:** Reference slide — quick summary of each tool's identity  
**Design:** Dark slide, four rows with tool name, one-line description, and "best for" callout

---

## Key Message

Each tool has a clear identity. Knowing that identity in one sentence makes the decision much faster in practice.

---

## Talking Points

"Let me compress it to four sentences — one per tool — so you have something to take away."

"*ASO:* Azure resources in Git, as Kubernetes YAML. If you think in Azure terms and want GitOps, start here."

"*Crossplane:* You design the API your developers use. Everything Azure is hidden behind your abstractions. If you want full control over the platform contract, this is your tool."

"*KRO:* One custom resource that expands into many. Think of it as Helm for Kubernetes-native app concepts, without the templating complexity. Pairs beautifully with ASO."

"*Terranetes:* Your Terraform, under Kubernetes control. Policy-gated, Git-tracked, no rewrite required. The pragmatic choice for teams with existing modules."

"None of these require you to abandon the others. A mature platform often uses all four — ASO and KRO for app-level provisioning, Crossplane for platform-team-owned abstractions, Terranetes for legacy Terraform modules still doing their job."

---

## Transition

→ Next: Demo — ASO in action
