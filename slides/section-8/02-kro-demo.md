# Slide 02 — Demo: KRO in Action

**Type:** Live demo — ResourceGroup definition + single developer CR  
**Design:** Split slide — left: ResourceGroup YAML template, right: developer CR + what gets created

---

## Key Message

One developer CR triggers an entire application setup. The ResourceGroup definition lives in the platform Git repo; the developer just applies their instance. Everything else is automatic.

---

## Demo Script

**Setup:** AKS cluster with KRO installed, ASO installed for Azure resources.

**What to show:**
1. Show the ResourceGroup definition — a template with variables (app name, owner, db size)
2. Show the developer CR — `AppEnvironment` with name and owner fields
3. Apply it: `kubectl apply -f demos/kro/app-environment.yaml`
4. Watch Kubernetes create the child resources: namespace, service account, role binding, managed identity (ASO), PostgreSQL (ASO)
5. Show that all resources reference each other correctly — the database is in the right namespace, the managed identity has the right permissions

**Key commands:**
```bash
kubectl apply -f demos/kro/app-environment.yaml
kubectl get appenv -w
kubectl get all -n my-app
kubectl get managedidentity,postgresqlflexibleserver -n my-app
```

---

## Talking Points

"Here's the ResourceGroup definition. Think of it as the template the platform team writes once. It takes three inputs: app name, owner, and database size."

"Here's what the developer writes. Seven lines. Apply it."

"Watch what Kubernetes creates: a namespace named after the app, a service account, RBAC bindings, a managed identity in Azure via ASO, and a PostgreSQL database — all connected, all named consistently."

"The developer didn't have to understand RBAC, managed identities, or ASO. They said 'I need an app environment.' The platform delivered one."

"And because this all flows through Argo CD in our GitOps setup, it's tracked, auditable, and self-healing."

---

## Transition

→ Next: KRO takeaway
