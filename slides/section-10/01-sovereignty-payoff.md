# Slide 01 — Sovereignty Revisited: The Control Plane Stays With You

**Type:** Connecting thread — all four tools share one property  
**Design:** Dark slide, heading "YOUR API. YOUR STATE. YOUR AUDIT TRAIL."

---

## Key Message

Every tool in this talk — ASO, Crossplane, KRO, Terranetes — runs as a Kubernetes operator inside your cluster. The control plane is yours. No state in a vendor backend. No audit trail you can't access. No outage you can't work around. This is the sovereignty payoff.

---

## Talking Points

"Let me connect the dots on sovereignty now that you've seen all four tools."

"Every single one of them runs inside your Kubernetes cluster. ASO — controller in your cluster. Crossplane — controllers in your cluster. KRO — controller in your cluster. Terranetes — controller in your cluster, jobs in your cluster."

"The Kubernetes API is the entry point for every infrastructure request in your organisation. Want to know what's running? `kubectl get`. Want the audit trail? It's in your Git history and Kubernetes events. Want to rotate credentials? You control the identity."

"Compare that to a SaaS platform-as-a-service where your resource definitions live in the vendor's database, their API is the entry point, and their outage is your outage."

"I'm not saying every organisation needs maximum sovereignty. But I am saying: the choice should be deliberate. The architecture we've shown today defaults to sovereignty — you opt out of it intentionally, not accidentally."

"For European organisations with GDPR obligations, financial services with regulatory requirements, government organisations — this isn't a nice-to-have. It's a hard requirement. And this architecture delivers it."

---

## Transition

→ Next: AI makes this more important, not less
