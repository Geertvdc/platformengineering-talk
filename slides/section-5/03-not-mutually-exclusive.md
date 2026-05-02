# Slide 03 — Not Mutually Exclusive

**Type:** Reassurance slide — these tools compose, not compete  
**Design:** Light slide, Venn-style or layered diagram showing tools as complementary layers

---

## Key Message

Real platforms use multiple tools simultaneously. The question is not "which tool wins" but "which tool owns which layer." Argo CD delivers all of them. They share the same GitOps foundation and the same Kubernetes API surface.

---

## Talking Points

"One thing I want to be explicit about before we dive into demos: these tools are not competing for the same job."

"I've seen teams spend months trying to pick a winner between Crossplane and Terranetes. That's the wrong question. They solve different problems. Many teams run both."

"Think of it in layers."

"The base layer is Argo CD and Git. Everything gets delivered through GitOps. That's non-negotiable — it's the delivery mechanism for everything else."

"The provisioning layer has multiple occupants. Crossplane owns the high-level platform abstractions — the stuff your developers interact with directly. ASO handles direct Azure resource management. Terranetes wraps existing Terraform. KRO handles app-level composition."

"A developer creating a new service might trigger a KRO ResourceGroup that spins up a namespace, a managed identity, and an ASO-managed database — all in one custom resource. And underneath that, Argo CD is watching the Git repo that contains the KRO definition, and automatically syncing any changes."

"The platform team's job is to assemble these layers thoughtfully — not to standardise on a single tool and force everything through it."

---

## Transition

→ Next: Demo 1 — ASO
