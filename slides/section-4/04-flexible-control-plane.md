# Slide 04 — The Flexible Control Plane

**Type:** Synthesis — framing the four tools as one coherent strategy  
**Design:** Light slide, architecture diagram or tool grid with Argo CD as the base layer

---

## Key Message

The platform is not a single tool — it's a control plane. Argo CD is the delivery layer underneath everything. On top of it, you choose the provisioning tools that match your team's skills, existing investments, and abstraction requirements. These tools are not mutually exclusive.

---

## Talking Points

"Here's the framing I want you to carry into the next section."

"We're not choosing one tool for everything. We're building a control plane — a Kubernetes API that is the single entry point for infrastructure intent across the entire organisation."

"Argo CD sits underneath all of it. It's the delivery engine. Every resource definition — whether it's a Crossplane Composition, an ASO manifest, a KRO ResourceGroup, or a Terranetes Configuration — gets delivered through GitOps. Argo CD doesn't care what it's applying. It just watches Git and makes the cluster match."

"On top of that base, the four tools solve different problems:"

"*ASO* — if you're Azure-first and you want direct GitOps control over Azure resources without building an abstraction layer."

"*Crossplane* — if you want to build your own platform API. The developer never touches Azure concepts directly. They create an AppDatabase and the platform figures out the rest."

"*KRO* — if you want to compose multiple Kubernetes resources into one app-level concept, without the full weight of Crossplane."

"*Terranetes* — if you have Terraform you trust and don't want to throw it away, but you want to bring it under Kubernetes control and add policy gates."

"Use one. Use all four. Use two. That's the point — the control plane is flexible."

---

## Transition

→ Next: Let's put this in a table — decision framework
