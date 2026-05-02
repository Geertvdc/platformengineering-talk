# Slide 01 — Demo: Terranetes — Terraform Under Kubernetes Control

**Type:** Demo intro — bridging the Terraform investment with Kubernetes  
**Design:** Dark slide, large "TERRANETES." heading, subtitle "YOUR TERRAFORM. OUR CONTROL PLANE."

---

## Key Message

Terranetes runs Terraform and OpenTofu inside Kubernetes as controller-managed jobs. It brings existing Terraform modules under platform control — with policy gates, Git-tracked state, and GitOps delivery — without requiring a rewrite.

---

## Talking Points

"Every organisation I've worked with has Terraform. Years of it. Tested, trusted, working modules for every Azure resource they care about. And the number one objection to adopting Crossplane or ASO is: 'but we already have Terraform that does this.'"

"Terranetes' answer is: keep it. Don't throw it away. We'll run it inside Kubernetes."

"Here's how it works. You define a `Configuration` CR — it points to a Terraform module in a Git repo, with the input variables you want. The Terranetes controller spins up a Kubernetes job that runs Terraform apply inside a container. The results come back as Kubernetes status conditions. Outputs can be injected as Kubernetes secrets."

"The Terraform state is still managed — Terranetes handles that — but the whole lifecycle is now Kubernetes-native. You trigger it with YAML. You watch it with kubectl. You gate it with Kubernetes policies."

"And because it's all YAML in Git, Argo CD can deliver it just like everything else."

"This is the pragmatic path. Meet teams where they are. Bring their existing investments under platform control. Don't demand a rewrite before day one."

---

## Transition

→ Next: Demo — Terranetes Configuration CR runs existing Terraform module
