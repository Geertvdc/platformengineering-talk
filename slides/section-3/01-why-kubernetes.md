# Slide 01 — Why Kubernetes

**Type:** Section opener — Kubernetes as the platform API
**Design:** Dark slide, big impact heading, watermark "API"

---

## Key Message

Kubernetes is not a container scheduler. It's an extensible, declarative API with a reconciliation loop built in. That is what makes it the right substrate for a platform — not the pods.

---

## Talking Points

"Whenever I bring up Kubernetes in a platform conversation, someone asks: 'Do we really need Kubernetes just to run containers?' And the honest answer is — no, you don't. If running containers was the only thing you needed, you'd pick something simpler."

"That question misses the point. The reason Kubernetes is the foundation of cloud native platforms isn't the container scheduler. It's the API."

"Think about what Kubernetes actually gives you: a uniform, declarative API. Every resource — pods, services, secrets, ingress — is described as desired state. You write YAML, you apply it, and a controller in the background works to make reality match what you described."

"That loop — observe, diff, act, repeat — is called reconciliation. It runs forever. If something drifts, it gets pulled back. If something fails, it gets retried. You don't write retry logic. You don't write rollback scripts. The platform does it."

"And the second thing — the API is *extensible*. Custom Resource Definitions let you add your own types. ASO adds Azure resources. Crossplane adds whatever you want. Argo CD adds Applications. The same API, the same RBAC, the same audit log — for everything."

"That's why we build platforms on Kubernetes. Not because we love YAML. Because the API and the reconciliation loop are the right primitives for self-service infrastructure."

---

## Transition

→ Next: What declarative actually means, and why it changes how you operate
