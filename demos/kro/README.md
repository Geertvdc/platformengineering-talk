# Demo: KRO — Compose Multi-Resource App Concepts

> **Section 8 — ~5 min total (≤ 3 min live, rest pre-bootstrapped).**
> Builds on [Demo #1 (GitOps)][demo-gitops] and [Demo #2 (ASO)][demo-aso]:
> kind cluster + Argo CD App-of-Apps + ASO controller + shared `azure-creds`.

---

## Goal

Show KRO as the lighter-weight alternative to Crossplane (Demo #3) when you
only need to **compose** existing Kubernetes / ASO resources rather than design
a new abstraction. One developer CR → namespace + RBAC + ASO-managed Azure
Storage Account + connection secret, all wired together — all on the local
kind cluster.

---

## Why KRO?

| | Crossplane (Demo #3) | KRO |
|---|---|---|
| What it does | Builds a new platform API on top of providers | Composes existing CRDs (K8s + ASO) into a single CR |
| When to use | Need a brand-new abstraction (multi-cloud, multi-provider) | Need to bundle existing K8s/ASO resources behind a simple CR |
| Provider setup | Requires provider pods + ProviderConfig | None — KRO uses whatever CRDs are already installed |
| Credentials | Crossplane manages its own provider credentials | None for KRO itself; ASO reuses the shared `azure-creds` |

**Verbal contrast (say this on stage):**
> _"KRO composes. Crossplane abstracts. Pick KRO when you want to bundle
> resources that already exist as CRDs. Pick Crossplane when you need a new
> API that didn't exist before."_

---

## Prereqs

Everything below must be in place **before you walk on stage**:

| # | What | Where |
|---|---|---|
| 1 | `platformeng-demo` kind cluster running | `demos/gitops/bootstrap/` |
| 2 | Argo CD installed + App-of-Apps healthy | `demos/gitops/bootstrap/10-install-argocd.sh` |
| 3 | Shared `azure-creds/azure-credentials` Secret present | `demos/gitops/bootstrap/30-azure-creds.sh` |
| 4 | ASO v2 controller installed + healthy | `demos/aso/bootstrap/install-aso.md` |
| 5 | Sandbox resource group `aso-demo-rg` pre-created in Azure | Azure Portal / `az group create` |
| 6 | KRO controller installed in `kro-system` | `demos/kro/bootstrap/install-kro.md` |
| 7 | `REPLACE_WITH_SUBSCRIPTION_ID` replaced in `rgd-myapp.yaml` | See bootstrap Step 4 |
| 8 | `kro-demo` Argo CD Application synced + RGD Ready | Verify with `kubectl get resourcegraphdefinition myapp` |

---

## One-time bootstrap (run before the talk)

### 1 — Run the shared bootstrap (if not already done)

```bash
./demos/gitops/bootstrap/bootstrap.sh
```

### 2 — Install ASO (if not already done)

Follow `demos/aso/bootstrap/install-aso.md`.

### 3 — Install the KRO controller

Follow `demos/kro/bootstrap/install-kro.md` in full.

Short version:

```bash
helm repo add kro https://kro.run/charts && helm repo update
helm upgrade --install kro kro/kro \
  --namespace kro-system --create-namespace \
  --version 0.2.1 --wait
```

### 4 — Replace the subscription ID placeholder

```bash
SUBSCRIPTION_ID=$(az account show --query id -o tsv)
sed -i "s/REPLACE_WITH_SUBSCRIPTION_ID/${SUBSCRIPTION_ID}/" \
  demos/kro/composition/rgd-myapp.yaml
git add demos/kro/composition/rgd-myapp.yaml
git commit -m "kro: set subscription ID in RGD"
git push
```

### 5 — Verify Argo CD has synced the RGD

```bash
kubectl get application kro-demo -n argocd
# SYNC STATUS: Synced   HEALTH STATUS: Healthy

kubectl get resourcegraphdefinition myapp
# NAME    SYNCED   READY
# myapp   True     True
```

### 6 — Pre-validate end-to-end (rehearsal)

```bash
kubectl apply -f demos/kro/samples/myapp.yaml
kubectl get namespace myapp              # should appear immediately
kubectl get rolebinding -n myapp         # platform-team-edit
kubectl get storageaccount -n myapp -w   # waits for ASO (~30-60 s)
kubectl get secret myapp-connection -n myapp  # written by ASO when Ready

# Reset after rehearsal
kubectl delete -f demos/kro/samples/myapp.yaml
kubectl delete namespace myapp
```

---

## ≤ 3-minute live demo script

| # | Action | Expected output |
|---|---|---|
| 1 | Open `demos/kro/composition/rgd-myapp.yaml` in the editor | Point out: it's *just templating* — namespace, RoleBinding, ASO StorageAccount, connection secret wired together |
| 2 | Open `demos/kro/samples/myapp.yaml` | "Three fields. Name, team, size. That's it." |
| 3 | `git commit -m "demo: add myapp instance" && git push` (or merge the prepared branch) | Push completes |
| 4 | Switch to Argo CD UI | `kro-demo` Application picks up the change and syncs |
| 5 | `kubectl get namespace myapp` | Namespace created by KRO |
| 6 | `kubectl get rolebinding -n myapp` | `platform-team-edit` RoleBinding present |
| 7 | `kubectl get storageaccount -n myapp -w` | Transitions `Provisioning → Succeeded` (~30-60 s) |
| 8 | `kubectl get secret myapp-connection -n myapp` | Connection secret written by ASO |
| 9 | Contrast verbally with Demo #3 | _"KRO composes; Crossplane abstracts."_ |

**Talking points between steps:**

- *"The ResourceGraphDefinition is the platform team's blueprint. They write it
  once. It bundles the namespace, the RBAC, the ASO Storage Account, and the
  connection secret into one composable unit."*
- *"The developer writes three fields: a name, their team, and a size. They don't
  know about Azure SKUs, resource groups, or TLS settings — the platform encoded
  all of that in the RGD."*
- *"One `kubectl apply` — or one Git commit through Argo CD — produces four
  real Kubernetes + Azure resources, all consistently named and labelled."*
- *"KRO doesn't need its own credential setup. It reuses ASO, which already
  has the `azure-creds` Secret from our GitOps bootstrap. Less moving parts
  than Crossplane for this use case."*

---

## Fallback plan (if Azure provisioning is slow on stage)

Conference Wi-Fi or a cold Azure region can slow Storage Account provisioning
to 60–90 s. If you're under time pressure:

1. **Show a pre-provisioned resource** — before the talk, apply `myapp.yaml`
   on `main` so all resources already exist. During the demo, open the Portal
   and say _"This was already provisioned — I committed it before the talk.
   Let me show you the composed resources."_ Then walk through
   `kubectl get namespace`, `rolebinding`, `storageaccount`, `secret`.

2. **Use a cached watch output** — record
   `kubectl get storageaccount -n myapp -w` during rehearsal and play it back
   if the live cluster is unresponsive. Audiences accept recordings for
   long-running operations.

3. **Skip ASO and show K8s resources only** — if Azure is completely
   unavailable, the namespace and RoleBinding appear immediately (< 1 s). Show
   those and say _"The namespace and RBAC appeared instantly. The Storage
   Account is in progress — on a warm cluster this finishes in under a
   minute."_

---

## Repo layout

```
demos/kro/
├── bootstrap/
│   └── install-kro.md                 # Helm install + pre-validation steps
├── composition/
│   └── rgd-myapp.yaml                 # ResourceGraphDefinition (ns + RBAC + ASO + secret)
├── samples/
│   └── myapp.yaml                     # what a developer writes (≤ 10 lines)
└── README.md                          # this file
```

Related files managed by Demo #1 (do not modify):

```
demos/gitops/
└── apps/
    └── kro.yaml                       # Argo CD Application for this demo
```

---

## Resetting between rehearsals

```bash
# Delete the developer CR — KRO reconciles and removes composed K8s resources
kubectl delete -f demos/kro/samples/myapp.yaml

# ASO-managed Azure resource is NOT deleted by KRO; delete it explicitly
kubectl delete storageaccount stmyapp -n myapp

# Wait for ASO to remove the Azure Storage Account
kubectl get storageaccount -n myapp -w

# Remove the app namespace (also removes the connection secret)
kubectl delete namespace myapp
```

To fully reset the KRO controller (e.g. after a version change):

```bash
helm upgrade --install kro kro/kro \
  --namespace kro-system --create-namespace \
  --version 0.2.1 --wait
```

---

[demo-gitops]: ../gitops/README.md
[demo-aso]: ../aso/README.md
