# Slide 02 — Demo: ASO in Action

**Type:** Live demo — creating an Azure resource via Kubernetes manifest  
**Design:** Terminal / code-focused slide, dark background, YAML on screen

---

## Key Message

A single Kubernetes manifest is the only input needed. ASO handles authentication, API calls, status tracking, and drift reconciliation. The Azure resource lifecycle is fully managed through Git.

---

## Demo Script

**Setup:** AKS cluster with ASO installed. Azure credentials configured via workload identity or managed identity.

**What to show:**
1. Open the demo manifest — a simple `StorageAccount` or `FlexibleServer` (PostgreSQL) CRD
2. Apply it with `kubectl apply -f`
3. Watch the resource appear in the Azure portal or via `az` CLI
4. Show `kubectl get storageaccount` — status conditions, ready state
5. Update a property in the manifest (e.g. SKU tier), re-apply, show Azure picking up the change
6. Show what happens if you manually change something in Azure — ASO reconciles it back
7. Delete the manifest — show the Azure resource being cleaned up

**Key commands:**
```bash
kubectl apply -f demos/aso/storage-account.yaml
kubectl get storageaccount -w
kubectl describe storageaccount myplatformstorage
kubectl delete -f demos/aso/storage-account.yaml
```

---

## Talking Points

"Here's the manifest. This is all you write. Name, resource group, location, SKU. Standard Azure concepts."

"Apply it. Watch the status. ASO is calling the Azure API right now in the background."

"A few seconds later — there it is. The storage account exists in Azure. I didn't open the portal. I didn't run an ARM template. I didn't write a Terraform plan. I applied a YAML file."

"Now watch what happens if I change the SKU here and re-apply. Azure gets updated. That's the reconciliation loop — same as Kubernetes workloads, but for cloud resources."

"And this is GitOps-ready out of the box. Put this manifest in your Git repo, point Argo CD at it, and your Azure infrastructure is now managed through pull requests."

---

## Transition

→ Next: Takeaway — when to use ASO
