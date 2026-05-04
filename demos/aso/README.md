# Demo: Azure Service Operator (ASO)

> **Section 6 — ≤ 5 min total (≤ 3 min live, rest pre-bootstrapped).**
> Builds on demo #1 (kind cluster + Argo CD App-of-Apps + shared `azure-creds`
> Secret). If demo #1 isn't running, start there first.

---

## Goal

Show the lowest-friction on-ramp to Azure resource management on Kubernetes:
a plain YAML manifest committed to Git → an Azure resource appears in the
portal, fully controlled through the GitOps loop — with **no Terraform, no
Bicep, no SDK**.

---

## Prereqs

Everything below must be in place **before you walk on stage**:

| # | What | Where |
|---|---|---|
| 1 | `platformeng-demo` kind cluster running | `demos/gitops/bootstrap/` |
| 2 | Argo CD installed + App-of-Apps healthy | `demos/gitops/bootstrap/10-install-argocd.sh` |
| 3 | Shared `azure-creds/azure-credentials` Secret present | `demos/gitops/bootstrap/30-azure-creds.sh` |
| 4 | ASO v2 controller installed + healthy | `demos/aso/bootstrap/install-aso.md` |
| 5 | Credentials wired to ASO controller | `demos/aso/bootstrap/identity/40-wire-aso-creds.sh` |
| 6 | Sandbox resource group pre-created in Azure | Azure Portal / `az group create` |
| 7 | `demos/aso/samples/storageaccount.yaml` customised | Replace the two `REPLACE_WITH_*` placeholders |

---

## One-time bootstrap (run before the talk)

### 1 — Run the shared bootstrap (if not already done)

```bash
./demos/gitops/bootstrap/bootstrap.sh
```

### 2 — Install the ASO controller

Follow `demos/aso/bootstrap/install-aso.md` in full.

Short version (requires Azure env vars exported):

```bash
helm repo add aso2 https://raw.githubusercontent.com/Azure/azure-service-operator/main/v2/charts
helm repo update
helm install --devel aso2 aso2/azure-service-operator \
  --create-namespace \
  --namespace azureserviceoperator-system \
  --set azureSubscriptionID="${AZURE_SUBSCRIPTION_ID}" \
  --set azureTenantID="${AZURE_TENANT_ID}" \
  --set azureClientID="${AZURE_CLIENT_ID}" \
  --set azureClientSecret="${AZURE_CLIENT_SECRET}" \
  --wait --timeout=5m
```

### 3 — Create the sandbox resource group

```bash
az group create \
  --name aso-demo-rg \
  --location westeurope
```

Replace `aso-demo-rg` and `westeurope` with your preferred values — just
make sure they match the placeholders in `samples/storageaccount.yaml`.

### 4 — Customise the sample manifest

Open `demos/aso/samples/storageaccount.yaml` and replace:

| Placeholder | Replace with |
|---|---|
| `REPLACE_WITH_SUBSCRIPTION_ID` | Your Azure subscription ID |
| `REPLACE_WITH_RESOURCE_GROUP` | The RG name from step 3 (e.g. `aso-demo-rg`) |
| `asoplatengdemo` | A **globally unique** Storage Account name (3–24 lowercase letters/digits only, no hyphens) |

Commit and push to `main` so Argo CD can sync it during the demo (or use a
ready branch to merge live — see the live script below).

### 5 — Verify the Argo CD Application exists

```bash
kubectl get application aso-demo -n argocd
```

If it isn't there yet, confirm `demos/gitops/apps/aso.yaml` is on `main`
and Argo CD has synced the App-of-Apps.

---

## ≤ 3-minute live demo script

| # | Action | Expected output |
|---|---|---|
| 1 | Open `demos/aso/samples/storageaccount.yaml` in the editor | Point out: it's just YAML — no Terraform, no Bicep, no SDK |
| 2 | `git commit -m "demo: add storage account" && git push` (or merge the ready branch) | Push completes |
| 3 | Switch to Argo CD UI | `aso-demo` Application picks up the change and goes **Syncing** |
| 4 | `kubectl get storageaccount -n aso-demo -w` | Status field transitions from `Provisioning` → `Succeeded` (~15–30 s) |
| 5 | Open Azure Portal → Storage Accounts | Resource is there — ASO created it via ARM |
| 6 | *(if time)* `git revert HEAD && git push` | Argo CD prunes the manifest → ASO deletes the Storage Account |

**Talking points between steps:**

- *"ASO is a Kubernetes operator that understands Azure resource types as
  Custom Resource Definitions. Any resource you can create in ARM, you can
  describe as a Kubernetes manifest."*
- *"The controller watches for these objects and calls the Azure ARM API on
  your behalf. Kubernetes becomes the control plane for Azure."*
- *"Delete the manifest from Git and the Azure resource disappears — the same
  GitOps loop that self-heals your workloads manages your infrastructure."*

---

## Fallback plan (if Azure provisioning is slow on stage)

Conference Wi-Fi or a cold Azure region can slow Storage Account provisioning
to 60–90 s. If you're under time pressure:

1. **Show the pre-provisioned resource** — before the talk, commit the manifest
   on `main` so the resource is already in Azure. During the demo, open the
   Portal immediately and say _"It's already there — I committed this before
   coming on stage. Let's watch what happens when I delete it."_ Then do the
   delete live (deletion is usually faster than creation).

2. **Use a cached watch output** — record `kubectl get storageaccount -n
   aso-demo -w` during rehearsal and play it back if the live cluster is
   unresponsive. Audiences accept recordings for long-running operations.

---

## Workload identity note (say this on stage)

> _"We're using a service principal with a client secret here — that's purely
> for demo speed. In production you'd use **Azure Workload Identity**:
> the controller pod gets a managed identity via a federated credential, there's
> no secret to rotate, and the blast radius is minimal. ASO v2 supports workload
> identity natively."_

---

## Repo layout

```
demos/aso/
├── bootstrap/
│   ├── install-aso.md                        # Helm install + credential wiring steps
│   └── identity/
│       ├── aso-controller-settings.template.yaml   # Secret shape reference (no values)
│       └── 40-wire-aso-creds.sh              # Copies shared azure-creds → ASO namespace
├── samples/
│   └── storageaccount.yaml                   # the live demo resource
└── README.md                                 # this file
```

Related files managed by demo #1 (do not modify):

```
demos/gitops/
├── bootstrap/
│   └── 30-azure-creds.sh                     # creates the shared azure-creds Secret
└── apps/
    └── aso.yaml                              # Argo CD Application for this demo
```

---

## Resetting between rehearsals

```bash
# Delete the Storage Account manifest so ASO removes the Azure resource
kubectl delete storageaccount asoplatengdemo -n aso-demo

# Wait for Azure deletion
kubectl get storageaccount -n aso-demo -w

# Re-stage the file on a branch (or just re-add it to main)
```

To fully reset the ASO controller (e.g. after credential rotation):

```bash
bash demos/aso/bootstrap/identity/40-wire-aso-creds.sh
```
