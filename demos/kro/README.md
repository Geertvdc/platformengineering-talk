# Demo: KRO — Compose Multi-Resource App Concepts

> **~5 min total. ≤ 3 min live, the rest pre-bootstrapped.**

---

## What you will show

One developer CR (`MyApp`) → KRO composes it into four real resources:
a Kubernetes **Namespace**, a **RoleBinding**, an **ASO-managed Azure Storage Account**, and a **connection Secret**.

The platform team encodes all the Azure opinions (region, resource group, SKU mapping, TLS settings) once in the `ResourceGraphDefinition`. The developer writes three fields: name, team, size.

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
| 7 | `ResourceGraphDefinition myapp` is `Ready: True` | verify below |

Steps 4–6 are all handled by the bootstrap script.

---

## One-time bootstrap

```bash
# From the repo root
bash demos/kro/bootstrap/bootstrap.sh
```

The script:
1. Checks that the shared platform (kind cluster, Argo CD, ASO) is already running.
2. Installs the KRO controller via Helm into `kro-system`.
3. Creates the dedicated Azure resource group `kro-demo-rg` (separate from any other demo).
4. Patches `demos/kro/composition/rgd-myapp.yaml` with your subscription ID and applies it.

If you use Argo CD to manage the RGD, also push the patched file:

```bash
git add demos/kro/composition/rgd-myapp.yaml
git commit -m "kro: set subscription ID and resource group"
git push
```

### Verify readiness

```bash
kubectl get resourcegraphdefinition myapp
# NAME    SYNCED   READY
# myapp   True     True

kubectl get crd myapps.kro.run
# NAME              ESTABLISHED
# myapps.kro.run   True
```

### Pre-validate end-to-end (rehearsal)

```bash
kubectl apply -f demos/kro/samples/myapp.yaml
kubectl get namespace myapp                    # appears in < 1 s
kubectl get rolebinding -n myapp               # platform-team-edit
kubectl get storageaccount -n myapp -w         # Provisioning → Succeeded (~30-60 s)
kubectl get secret myapp-connection -n myapp   # written by ASO on success

# Reset
kubectl delete -f demos/kro/samples/myapp.yaml
kubectl delete namespace myapp --ignore-not-found
```

---

## Live demo script (≤ 3 min)

| # | You do | Audience sees |
|---|---|---|
| 1 | Open `demos/kro/composition/rgd-myapp.yaml` | Point out the template: namespace, RoleBinding, ASO StorageAccount, connection secret — all wired together in one file |
| 2 | Open `demos/kro/samples/myapp.yaml` | "Three fields. Name, team, size. That's it." |
| 3 | `kubectl apply -f demos/kro/samples/myapp.yaml` | Apply completes |
| 4 | `kubectl get namespace myapp` | Namespace created immediately |
| 5 | `kubectl get rolebinding -n myapp` | `platform-team-edit` present |
| 6 | `kubectl get storageaccount -n myapp -w` | Status: `Provisioning → Succeeded` (~30-60 s) |
| 7 | `kubectl get secret myapp-connection -n myapp` | Connection secret written by ASO |
| 8 | Verbal contrast with Crossplane | _"KRO composes; Crossplane abstracts."_ |

**Talking points:**

- *"The ResourceGraphDefinition is the platform team's blueprint. They write it once. The developer writes three fields."*
- *"One `kubectl apply` — or one Git commit through Argo CD — produces four real resources: a namespace, RBAC, an Azure Storage Account, and a connection secret."*
- *"KRO doesn't need its own credential setup. It reuses ASO, which already handles Azure auth. Fewer moving parts than Crossplane for this use case."*
- *"The developer doesn't know about Azure SKUs, resource groups, or TLS settings. The platform encoded all of that in the RGD."*

---

## Fallback plan

**Azure is slow (60–90 s is normal on conference Wi-Fi):**

- Show the namespace and RoleBinding immediately — they appear in < 1 s.
  Say: *"The Kubernetes resources are instant. The Storage Account is in progress — this normally finishes in under a minute."*

- If you pre-applied `myapp.yaml` before the talk, skip the apply live and go straight to showing the resources. Walk through the Portal to prove the Azure resource is real.

- Record `kubectl get storageaccount -n myapp -w` during rehearsal and play it back as a fallback. Audiences accept recordings for long-running operations.

**Cluster unreachable:**

- Open the Azure Portal directly and show the Storage Account in `kro-demo-rg`.
- Walk through the RGD YAML in the editor and explain the composition without running anything live.

---

## Resetting between runs

```bash
# Remove the developer CR — KRO removes the composed Kubernetes resources
kubectl delete -f demos/kro/samples/myapp.yaml

# ASO does NOT cascade-delete Azure resources when the StorageAccount CR is removed
# by KRO. Delete it explicitly to clean up Azure:
kubectl delete storageaccount stmyapp -n myapp --ignore-not-found

# Wait for Azure deletion, then remove the namespace
kubectl get storageaccount -n myapp -w   # until gone
kubectl delete namespace myapp --ignore-not-found
```

To fully reset the KRO controller:

```bash
helm upgrade --install kro oci://registry.k8s.io/kro/charts/kro \
  --namespace kro-system \
  --create-namespace \
  --version 0.9.1 \
  --wait
```

---

## Repo layout

```
demos/kro/
├── bootstrap/
│   └── bootstrap.sh          # one-command setup: KRO + Azure RG + RGD patch
├── composition/
│   └── rgd-myapp.yaml        # ResourceGraphDefinition (namespace + RBAC + ASO + secret)
├── samples/
│   └── myapp.yaml            # what a developer writes (three fields)
└── README.md                 # this file
```

Related (managed by the platform bootstrap, do not modify from this demo):

```
demos/gitops/apps/
└── kro.yaml                  # Argo CD Application pointing at demos/kro/composition/
```
