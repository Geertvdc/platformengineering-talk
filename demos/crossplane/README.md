# Demo: Crossplane — Build Your Own Platform API

> **Section 7** — ~5 min slot (≤ 3 min live, rest pre-bootstrapped).
> Builds on [Demo 1 (GitOps)][demo-gitops]: kind cluster + Argo CD + shared `azure-creds`.
> Independent of Demo 2 (ASO).

---

## Why Crossplane, why `AppStorage`?

**ASO** (Demo 2) exposes Azure CRDs directly — great for Azure-native teams, but
developers must know Azure concepts (SKUs, replication types, resource groups).

**Crossplane** flips this: the *platform team* owns the abstraction. A developer
writes a 10-line `AppStorage` claim with `name` and `size`. Crossplane's
Composition translates that into an Azure Storage Account + Blob Container with
all platform-mandated settings (region, tags, naming convention, TLS baseline)
baked in. The developer never sees an Azure field.

### Why Storage Account (not PostgreSQL or SQL)?

Azure Storage Account provisions in **< 60 seconds** — well inside the 3-minute
live demo budget. Flexible Server / SQL take 5–10 minutes and kill the demo.

### Why `AppStorage` (not `AppDatabase` from the slides)?

`AppStorage` with a size tier (`small` / `medium` / `large` → LRS / GRS / RAGRS)
exposes a genuinely different abstraction from Demo 2 while still showing the
same Crossplane power. The platform team encodes the replication strategy; the
developer only picks a logical tier.

---

## Prereqs

Everything from [Demo 1 (GitOps)][demo-gitops] plus:

| Tool | Version | Why |
|------|---------|-----|
| `helm` | ≥ v3.14 | Install Crossplane via Helm |
| Azure SP | Contributor on `rg-platform-demo` | Same SP as other demos |

The sandbox resource group **`rg-platform-demo`** must exist in `westeurope`
(the Composition hardcodes it). Create it once:

```bash
az group create \
  --name rg-platform-demo \
  --location westeurope \
  --tags managed-by=crossplane platform=true environment=demo
```

---

## Bootstrap (run before the talk, NOT live)

### 1 — Ensure Demo 1 is bootstrapped

```bash
./demos/gitops/bootstrap/bootstrap.sh
```

This creates the kind cluster, installs Argo CD, registers the GitHub repo,
and creates the shared `azure-credentials` Secret in `azure-creds`.

### 2 — Install Crossplane

```bash
bash demos/crossplane/bootstrap/10-install-crossplane.sh
```

Installs Crossplane `v1.17.1` via Helm into `crossplane-system`.
See `bootstrap/install-crossplane.md` for details.

### 3 — Create the provider credentials Secret

```bash
bash demos/crossplane/bootstrap/20-crossplane-azure-creds.sh
```

Reads the four fields from `azure-creds/azure-credentials` (the shared SP
Secret) and writes `crossplane-system/azure-provider-creds` as a JSON blob
for the Crossplane Azure provider. **No new service principal is created.**

### 4 — Let Argo CD sync the rest

The `crossplane-demo` Application is registered in `demos/gitops/apps/crossplane.yaml`.
Argo CD picks it up automatically and applies, in order:

| Resource | Kind | Source |
|----------|------|--------|
| `upbound-provider-azure-storage` | `Provider` | `bootstrap/provider/` |
| `default` | `ProviderConfig` | `bootstrap/provider/` |
| `xappstorages.platform.demo.io` | `CompositeResourceDefinition` | `composition/` |
| `xappstorages-azure` | `Composition` | `composition/` |
| `crossplane-demo` | `Namespace` | `samples/` |
| `demo-app-store` | `AppStorage` | `samples/` |

Wait for the Provider to become healthy (pulls provider image, ~2–3 min):

```bash
kubectl get provider upbound-provider-azure-storage -w
# NAME                              INSTALLED   HEALTHY
# upbound-provider-azure-storage   True        True
```

Verify XRD is established and offered:

```bash
kubectl get xrd xappstorages.platform.demo.io
# NAME                              ESTABLISHED   OFFERED   AGE
# xappstorages.platform.demo.io   True          True      ...
```

---

## The ≤ 3-minute live demo script

| # | Action | Expected output |
|---|--------|-----------------|
| 1 | Show the **developer CR** | `demos/crossplane/samples/appstorage.yaml` — 10 lines, only `name` and `size` |
| 2 | Show the **Composition** side-by-side | `demos/crossplane/composition/composition-appstorage.yaml` — tags, naming, RG, TLS all platform-owned |
| 3 | `git commit && git push` the developer CR (or it's already in repo) | Argo CD picks it up in ≤ 30 s |
| 4 | `kubectl -n crossplane-demo get appstorage` | Claim appears, `SYNCED=True`, `READY=True` |
| 5 | `kubectl get xappstorage` | Composite resource visible |
| 6 | `kubectl get account` | Managed resource: `stdemosapp` in Azure |
| 7 | Azure Portal | Storage Account `stdemoapp` present with tags `managed-by=crossplane` |

**Useful commands:**

```bash
# Watch the claim status
kubectl -n crossplane-demo get appstorage demo-app-store -w

# See what Crossplane composed
kubectl get xappstorage
kubectl get account
kubectl get container.storage

# Describe the managed resource for full detail
kubectl describe account stdemoapp
```

**One-liner for the audience:**

> _"The developer wrote 10 lines with a name and a size. The Composition added
> the resource group, the region, the TLS settings, the tags — and spun up
> the Storage Account and the container. Developer experience and platform
> standards, fully separated."_

---

## Fallback (if Azure provisioning is slow)

If the Storage Account hasn't appeared yet:

1. Show the **pre-provisioned** resource from a rehearsal run in the Azure Portal
2. Walk through the Composition YAML (`composition/composition-appstorage.yaml`)
   and narrate each platform opinion — this is compelling even without live provisioning

---

## Workload Identity Note

> **On stage:** "We're using a service principal with a client secret here for
> demo speed. In production you'd use workload identity / federated credentials —
> no secrets at all. Crossplane supports `source: InjectedIdentity` in the
> ProviderConfig for exactly this."

The ProviderConfig (`bootstrap/provider/providerconfig.yaml`) uses
`source: Secret` for the demo. Swap to `source: InjectedIdentity` and remove
the `secretRef` block to enable workload identity.

---

## Repo layout

```
demos/crossplane/
├── bootstrap/
│   ├── install-crossplane.md          # Full bootstrap guide
│   ├── 10-install-crossplane.sh       # Helm install (run before talk)
│   ├── 20-crossplane-azure-creds.sh   # Bridge SP creds to Crossplane format
│   └── provider/
│       ├── provider-azure-storage.yaml  # Crossplane Provider package (Argo CD managed)
│       └── providerconfig.yaml          # ProviderConfig → azure-provider-creds (Argo CD managed)
├── composition/
│   ├── xrd-appstorage.yaml            # Platform API definition (XRD)
│   └── composition-appstorage.yaml    # Implementation (Storage Account + Container)
├── samples/
│   ├── namespace.yaml                 # crossplane-demo namespace
│   └── appstorage.yaml                # Developer-facing claim (10 lines, name + size only)
└── README.md
```

Argo CD Application: `demos/gitops/apps/crossplane.yaml`

---

## Resetting between rehearsals

Delete the managed resources and re-apply:

```bash
kubectl -n crossplane-demo delete appstorage demo-app-store
# Wait for Azure resources to deprovision, then re-commit the file
```

Or nuke and recreate the whole cluster:

```bash
kind delete cluster --name platformeng-demo
./demos/gitops/bootstrap/bootstrap.sh
bash demos/crossplane/bootstrap/10-install-crossplane.sh
bash demos/crossplane/bootstrap/20-crossplane-azure-creds.sh
```

[demo-gitops]: ../gitops/README.md
