# Demo: KRO — Compose Multi-Resource App Concepts

> **~5 min total. ≤ 3 min live, the rest pre-bootstrapped.**

---

## What you will show

One developer CR (`MyApp`) → KRO composes it into three real resources:
a Kubernetes **Namespace**, a **RoleBinding**, and an **ASO-managed Azure Storage Account**.

The platform team encodes all Azure opinions (region, resource group, SKU mapping, TLS settings) once in a `ResourceGraphDefinition`. The developer writes three fields: name, team, size.

---

## Why KRO (say this on stage)

> _"KRO composes. Crossplane abstracts. Pick KRO when you want to bundle resources that already exist as CRDs. Pick Crossplane when you need a brand-new API that didn't exist before."_

| | Crossplane | KRO |
|---|---|---|
| Model | Builds a new platform API on top of providers | Composes existing CRDs (Kubernetes + ASO) behind a single CR |
| When to use | Need a multi-cloud or multi-provider abstraction | Need to bundle K8s + ASO resources into one simple CR |
| Provider setup | Provider pods + ProviderConfig | None — KRO uses whatever CRDs are already installed |
| Credentials | Crossplane manages its own | None for KRO itself; ASO handles Azure auth |

---

## How the naming works

The `spec.name` field drives all derived resource names. With `spec.name: myapp`:

| Resource | Name | Where |
|---|---|---|
| Namespace | `myapp` | Kubernetes |
| RoleBinding | `platform-team-edit` | in namespace `myapp` |
| StorageAccount | `stmyapp` | Azure, in `kro-demo-rg` |

The developer never sees resource groups, SKU names, or regions — those are encoded in the RGD.

---

## Pre-demo checklist

Everything below must be in place **before you walk on stage**:

| # | What | How |
|---|---|---|
| 1 | `platformeng-demo` kind cluster running | `demos/gitops/bootstrap/bootstrap.sh` |
| 2 | Argo CD installed and App-of-Apps healthy | included in step 1 |
| 3 | ASO v2 controller installed and healthy | `demos/aso/bootstrap/bootstrap.sh` |
| 4 | KRO controller installed (`kro-system`) | `demos/kro/bootstrap/bootstrap.sh` ✓ |
| 5 | Azure resource group `kro-demo-rg` created | `demos/kro/bootstrap/bootstrap.sh` ✓ |
| 6 | `rgd-myapp.yaml` patched with correct subscription ID | `demos/kro/bootstrap/bootstrap.sh` ✓ |
| 7 | `kro-demo` namespace exists | `demos/kro/bootstrap/bootstrap.sh` ✓ |
| 8 | `ResourceGraphDefinition myapp` is `Active` and `Ready: True` | verify below |

Steps 4–7 are all handled by the bootstrap script.

---

## One-time bootstrap

```bash
# From the repo root
bash demos/kro/bootstrap/bootstrap.sh
```

The script:
1. Checks the shared platform (kind cluster, Argo CD, ASO) is already running.
2. Installs the KRO controller via Helm into `kro-system`.
3. Creates the dedicated Azure resource group `kro-demo-rg`.
4. Patches `demos/kro/composition/rgd-myapp.yaml` with your subscription ID and applies it.
5. Creates the `kro-demo` namespace where MyApp instances are submitted.

If you use Argo CD to manage the RGD, also push the patched file:

```bash
git add demos/kro/composition/rgd-myapp.yaml
git commit -m "kro: set subscription ID and resource group"
git push
```

### Verify readiness

```bash
kubectl get resourcegraphdefinition myapp
# NAME    APIVERSION   KIND    STATE    READY
# myapp   v1alpha1     MyApp   Active   True

kubectl get crd myapps.kro.run
# NAME             CREATED AT
# myapps.kro.run   ...
```

### Pre-validate end-to-end (rehearsal)

```bash
# Submit the developer CR
kubectl apply -f demos/kro/samples/myapp.yaml

# KRO creates these immediately (< 1 s):
kubectl get namespace myapp
kubectl get rolebinding -n myapp              # platform-team-edit

# ASO provisions the Azure resource (~30–60 s):
kubectl get storageaccount -n myapp -w
# NAME      READY   SEVERITY   REASON      MESSAGE
# stmyapp   True               Succeeded

# Reset
kubectl delete -f demos/kro/samples/myapp.yaml
# KRO removes the namespace and everything in it automatically.
# The Azure Storage Account deletion is triggered by ASO when the CR is removed.
```

---

## Live demo script (≤ 3 min)

| # | You do | Audience sees |
|---|---|---|
| 1 | Open `demos/kro/composition/rgd-myapp.yaml` | Point out the template: namespace, RoleBinding, ASO StorageAccount — all wired together. Highlight that region, RG, SKU, TLS are all encoded here. |
| 2 | Open `demos/kro/samples/myapp.yaml` | "Three fields. Name, team, size. That's the entire developer interface." |
| 3 | `kubectl apply -f demos/kro/samples/myapp.yaml` | `myapp.kro.run/myapp created` |
| 4 | `kubectl get namespace myapp` | Namespace appears in < 1 s |
| 5 | `kubectl get rolebinding -n myapp` | `platform-team-edit` present |
| 6 | `kubectl get storageaccount -n myapp -w` | Status transitions `Reconciling → Succeeded` (~30–60 s) |
| 7 | Open Azure Portal → Storage Accounts, filter `kro-demo-rg` | `stmyapp` is there |
| 8 | Verbal contrast with Crossplane | _"KRO composes; Crossplane abstracts."_ |

**Talking points:**

- *"The ResourceGraphDefinition is the platform team's blueprint. They write it once. It bundles the namespace, the RBAC, and the Azure Storage Account into one composable unit."*
- *"The developer writes three fields. They don't know about Azure SKUs, resource groups, or TLS settings — the platform encoded all of that in the RGD."*
- *"One `kubectl apply` produces three real resources: a namespace, RBAC, and an Azure Storage Account — all consistently named and labelled."*
- *"KRO doesn't need its own credential setup. It reuses ASO, which already handles Azure auth. Fewer moving parts than Crossplane for this use case."*
- *"When you delete the CR, KRO removes the namespace and everything in it. ASO cascades that to Azure and deletes the Storage Account. One delete, full cleanup."*

---

## Fallback plan

**Azure is slow (30–60 s is normal, up to 90 s on conference Wi-Fi):**

- Show the namespace and RoleBinding immediately — they appear in < 1 s.
  Say: *"The Kubernetes resources are instant. The Storage Account is provisioning in the background — this normally finishes in under a minute."*
- If you pre-applied `myapp.yaml` before the talk, open the Azure Portal immediately and show `stmyapp` already there. Then walk through the composed Kubernetes resources.

**Cluster unreachable:**

- Open the Azure Portal and show the Storage Account in `kro-demo-rg`.
- Walk through the RGD YAML in the editor and explain the composition without running anything live.

---

## Resetting between runs

```bash
# Delete the developer CR — KRO removes the namespace, RoleBinding, and StorageAccount CR.
# ASO then deletes the Azure Storage Account.
kubectl delete -f demos/kro/samples/myapp.yaml

# Confirm the namespace is gone (KRO handles this automatically):
kubectl get namespace myapp
# Error from server (NotFound): ...

# Confirm the Azure resource is being deleted:
# (may take 30–60 s for ASO to finish)
az storage account show --name stmyapp --resource-group kro-demo-rg 2>&1 | grep provisioningState
```

---

## Repo layout

```
demos/kro/
├── bootstrap/
│   └── bootstrap.sh          # one-command setup: KRO + Azure RG + RGD patch + kro-demo namespace
├── composition/
│   └── rgd-myapp.yaml        # ResourceGraphDefinition (namespace + RBAC + ASO StorageAccount)
├── samples/
│   └── myapp.yaml            # what a developer writes (three fields)
└── README.md                 # this file
```

Related (managed by the platform bootstrap, do not modify from this demo):

```
demos/gitops/apps/
└── kro.yaml                  # Argo CD Application pointing at demos/kro/composition/
```
