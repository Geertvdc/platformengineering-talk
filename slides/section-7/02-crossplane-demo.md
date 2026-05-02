# Slide 02 — Demo: Crossplane in Action

**Type:** Live demo — XRD + Composition + developer CR  
**Design:** Split slide — left: simple developer CR, right: what Crossplane creates in Azure

---

## Key Message

The developer manifest is trivially simple. The Composition is where the platform team encodes complexity. This separation — simple public API, complex private implementation — is the core Crossplane value proposition.

---

## Demo Script

**Setup:** AKS cluster with Crossplane installed, Azure provider configured, XRD and Composition already applied.

**What to show:**
1. Show the developer-facing CR — `AppDatabase` with 3 fields (name, size, owner)
2. Apply it: `kubectl apply -f demos/crossplane/app-database.yaml`
3. Watch Crossplane create the composite resource and the managed resources
4. Show what it provisioned in Azure — PostgreSQL flexible server, private endpoint, secret in Key Vault
5. Show the Composition briefly — highlight how platform opinions are encoded (region, backup, tags)
6. Developer never sees any of this complexity

**Key commands:**
```bash
kubectl apply -f demos/crossplane/app-database.yaml
kubectl get appdatabase -w
kubectl get managed
kubectl describe postgresqlflexibleserver
```

---

## Talking Points

"Here's the developer manifest. Three fields. Name, size, owner. That's the entire API surface the developer interacts with."

"I apply it. Crossplane picks it up, reads the Composition, and starts provisioning. Watch the managed resources appear."

"In Azure: a PostgreSQL flexible server, in the right region, with the right networking, tagged correctly, with backup enabled. All of that is in the Composition — written once by the platform team, applied every time."

"The developer didn't write any of that. They asked for a database. The platform delivered one."

"And if the platform team changes the Composition — updates the backup policy, changes the default region — every future `AppDatabase` picks it up. One change, consistent across the whole platform."

---

## Transition

→ Next: Crossplane takeaway
