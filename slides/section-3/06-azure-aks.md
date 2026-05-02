# Slide 06 — Azure / AKS

**Type:** Substrate — AKS as the platform's home, not its boundary
**Design:** Light slide, two-line impact heading, watermark "AZURE"

---

## Key Message

AKS is where the platform runs. But the platform doesn't end at the cluster boundary — it reaches out into the rest of Azure: managed databases, identity, networking, storage. The Kubernetes API is the entry point; Azure is the implementation.

---

## Talking Points

"Let's anchor this in reality. We're building on Azure, and AKS is where this platform lives — the Kubernetes cluster that hosts Argo CD, the controllers, and most of the platform's own components."

"But here's the subtle part: AKS is the *home* of the platform, not the *limit* of it. If we tried to run literally everything inside Kubernetes — every database as a stateful set, every queue as an in-cluster broker — we'd be reinventing managed services badly, and giving up the things Azure already does well."

"The pattern is different. The Kubernetes API stays the entry point — the place developers and pipelines go to ask for things. But behind that API, the actual work often happens in Azure managed services: Azure Database for PostgreSQL, Service Bus, Storage Accounts, managed identities, Key Vault."

"That's why the next four tools we'll look at — ASO, Crossplane, KRO, Terranetes — all matter. Each of them is a different way to take a Kubernetes resource someone applied, and turn it into real Azure infrastructure outside the cluster."

"So the picture is: AKS in the middle, running the control plane and the workloads that belong there. Azure managed services around it, doing the heavy lifting where it makes sense. And one consistent API — the Kubernetes API — that ties them together."

"Kubernetes inside. Azure outside. One platform."

---

## Transition

→ Next (Section 4): Designing for the messy reality — multiple teams, clouds, tools, and existing investments
