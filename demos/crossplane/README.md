# Demo: Crossplane — Build Your Own Platform API

> **Section 7** — ~5 min slot (≤ 3 min live, rest pre-bootstrapped).
> Builds on [Demo 1 (GitOps)][demo-gitops]: kind cluster + Argo CD + shared `azure-creds`.
> Independent of Demo 2 (ASO).

---

## Two compositions — two talking points

This demo includes **two independent compositions** to illustrate different aspects of Crossplane:

| Composition | Claim | Provisions | Key talking point |
|---|---|---|---|
| `AppStorage` | `name` + `size` | Azure Storage Account + Blob Container | Platform-owned abstraction vs ASO's raw CRDs |
| `AppTeam` | `teamName` + `githubOrg` | Azure RG + Storage Account **+** GitHub repo | **Multi-cloud**: one claim, two providers |

Use `AppStorage` to contrast with Demo 2 (ASO), then introduce `AppTeam` to land Crossplane's multi-provider differentiation.

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

## Why `AppTeam`? The multi-cloud moment

The `AppTeam` composition is the "wow" moment: a developer applies **one 10-line
claim** and Crossplane simultaneously:

1. Creates an **Azure Resource Group** (`rg-team-<name>`) with platform tags
2. Creates an **Azure Storage Account** (`stteam<name>`) inside that RG
3. Creates a **private GitHub repository** (`<name>-platform-infra`) in the org

Two providers, two clouds, one claim — no Azure knowledge, no GitHub API
familiarity required from the developer. This is a capability ASO and KRO
cannot offer alone.

---

## Prereqs

Everything from [Demo 1 (GitOps)][demo-gitops] plus:

| Tool | Version | Why |
|------|---------|-----|
| `helm` | ≥ v3.14 | Install Crossplane via Helm |
| Azure SP | Contributor on sandbox subscription | Same SP as other demos |
| `GITHUB_TOKEN` | PAT with `repo`, `read:org`, `delete_repo` scopes | GitHub provider authentication |

For `AppStorage`: the Composition targets `rg-platform-demo`. Pre-create it:

```bash
az group create \
  --name rg-platform-demo \
  --location westeurope \
  --tags managed-by=crossplane platform=true environment=demo
```

For `AppTeam`: the Composition dynamically creates `rg-team-<teamName>` — no
pre-creation needed (the Azure provider creates it). Ensure the SP has
**Resource Group create** permissions on the subscription.

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

Installs Crossplane `v2.2.1` via Helm into `crossplane-system`.
See `bootstrap/install-crossplane.md` for details.

### 3 — Create the Azure provider credentials Secret

```bash
bash demos/crossplane/bootstrap/20-crossplane-azure-creds.sh
```

Reads the four fields from `azure-creds/azure-credentials` (the shared SP
Secret) and writes `crossplane-system/azure-provider-creds` as a JSON blob
for the Crossplane Azure provider. **No new service principal is created.**

### 4 — Create the GitHub provider credentials Secret

```bash
export GITHUB_TOKEN=ghp_...   # PAT with repo + read:org + delete_repo scopes
export GITHUB_OWNER=Geertvdc  # your GitHub username or org
bash demos/crossplane/bootstrap/30-github-creds.sh
```

Writes `crossplane-system/github-provider-creds` with key `credentials` as a JSON blob
`{"token":"...","owner":"..."}`. The same `GITHUB_TOKEN` already set for Argo CD
(Demo 1) works here if it has the required scopes.

### 5 — Install Providers and wait for CRDs

```bash
bash demos/crossplane/bootstrap/40-install-providers.sh
```

Applies the three Provider packages and **blocks until each is `HEALTHY=True`**
(~2–3 min on first run while images pull). This pre-registers all Azure and
GitHub CRDs so Argo CD never encounters a missing resource during sync.

### 6 — Let Argo CD sync the rest

The `crossplane-demo` Application is registered in `demos/gitops/apps/crossplane.yaml`.
It watches only `composition/` and `samples/` (providers live in `bootstrap/` and
are managed imperatively). Argo CD applies in three sync waves:

| Resource | Kind | Wave |
|----------|------|------|
| `xappstorages.platform.demo.io` | `CompositeResourceDefinition` | 1 |
| `xappteams.platform.demo.io` | `CompositeResourceDefinition` | 1 |
| `xappstorages-azure` | `Composition` | 2 |
| `xappteams-azure-github` | `Composition` | 2 |
| `crossplane-demo` | `Namespace` | 3 |
| `demo-app-store` | `AppStorage` | 3 |
| `alpha-team` | `AppTeam` | 3 |

Wait for all Providers to become healthy (~2–3 min while images pull):

```bash
kubectl get providers -w
# NAME                                INSTALLED   HEALTHY
# upbound-provider-azure-resources   True        True
# upbound-provider-azure-storage     True        True
# crossplane-contrib-provider-github True        True
```

Verify XRDs are established and offered:

```bash
kubectl get xrd
# NAME                              ESTABLISHED   OFFERED
# xappstorages.platform.demo.io   True          True
# xappteams.platform.demo.io      True          True
```

---

## The ≤ 3-minute live demo script

### Part A — AppStorage (contrast with ASO)

| # | Action | Expected output |
|---|--------|-----------------|
| 1 | Show the **developer CR** | `demos/crossplane/samples/appstorage.yaml` — 11 lines, only `name` and `size` |
| 2 | Show the **Composition** side-by-side | `composition/composition-appstorage.yaml` — tags, naming, RG, TLS all platform-owned |
| 3 | `kubectl -n crossplane-demo get appstorage` | Claim `SYNCED=True`, `READY=True` |
| 4 | `kubectl get account` | Managed resource `stdemoapp` visible |
| 5 | Azure Portal | Storage Account present with tags `managed-by=crossplane` |

### Part B — AppTeam (the multi-cloud moment)

| # | Action | Expected output |
|---|--------|-----------------|
| 1 | Show `samples/appteam.yaml` | 10 lines: just `teamName: alpha` and `githubOrg: Geertvdc` |
| 2 | Show `composition/composition-appteam.yaml` | Three sections: RG, Storage Account, GitHub repo |
| 3 | `git commit && git push` the AppTeam claim (or it's already in repo) | Argo CD picks it up |
| 4 | `kubectl -n crossplane-demo get appteam alpha-team -w` | Claim becomes `READY=True` |
| 5 | `kubectl get resourcegroup` + `kubectl get account` | Azure RG + Storage Account |
| 6 | GitHub → `Geertvdc/alpha-platform-infra` | Private repo created automatically |

**Useful commands:**

```bash
# Watch both claims
kubectl -n crossplane-demo get appstorage,appteam

# Inspect all composed managed resources
kubectl get managed

# Show the Azure and GitHub resources side by side
kubectl get resourcegroup,account,repository.github

# Describe the AppTeam XR to see all status fields
kubectl describe xappteam
```

**One-liner for the audience:**

> _"The developer wrote 10 lines with a team name and a GitHub org. Crossplane's
> Composition created an Azure Resource Group, a Storage Account inside it, AND
> a private GitHub repo — all from a single claim. Two providers, two clouds,
> one platform API. No Azure knowledge, no GitHub API token, no manual steps."_

---

## Fallback (if Azure provisioning is slow)

If the Storage Account or RG hasn't appeared yet:

1. Show the **pre-provisioned** resource from a rehearsal run in the Azure Portal
   and the GitHub org
2. Walk through the Composition YAML (`composition/composition-appteam.yaml`)
   and narrate each section — this is compelling even without live provisioning

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
│   ├── 30-github-creds.sh             # Create github-provider-creds from GITHUB_TOKEN + GITHUB_OWNER
│   ├── 40-install-providers.sh        # Apply Providers + wait for healthy + apply ProviderConfigs
│   └── provider/
│       ├── provider-azure-resources.yaml  # Azure Resources provider (ghcr.io, v2.5.0)
│       ├── provider-azure-storage.yaml    # Azure Storage provider (ghcr.io, v2.5.0)
│       ├── provider-github.yaml           # GitHub provider (ghcr.io, v0.19.0)
│       ├── providerconfig.yaml            # Azure ProviderConfig → azure-provider-creds
│       └── providerconfig-github.yaml     # GitHub ProviderConfig → github-provider-creds
├── composition/
│   ├── appstorage/
│   │   ├── xrd-appstorage.yaml            # Platform API: AppStorage (name + size)
│   │   └── composition-appstorage.yaml    # Azure Storage Account + Container
│   └── appteam/
│       ├── xrd-appteam.yaml               # Platform API: AppTeam (teamName + githubOrg)
│       └── composition-appteam.yaml       # Azure RG + Storage Account + GitHub Repo
├── samples/
│   ├── appstorage/
│   │   ├── namespace.yaml                 # crossplane-demo namespace
│   │   └── appstorage.yaml                # AppStorage claim (name + size only)
│   └── appteam/
│       ├── namespace.yaml                 # crossplane-demo namespace
│       └── appteam.yaml                   # AppTeam claim (teamName + githubOrg)
└── README.md
```

Argo CD Applications (both labelled `demo: demo-3`):
- `demos/gitops/apps/crossplane-appstorage.yaml` — XRD + Composition + claim for AppStorage
- `demos/gitops/apps/crossplane-appteam.yaml` — XRD + Composition + claim for AppTeam

---

## Resetting between rehearsals

Delete the managed resources and re-apply:

```bash
kubectl -n crossplane-demo delete appstorage demo-app-store
kubectl -n crossplane-demo delete appteam alpha-team
# Wait for Azure resources and GitHub repo to deprovision, then re-commit the files
```

Or nuke and recreate the whole cluster:

```bash
kind delete cluster --name platformeng-demo
./demos/gitops/bootstrap/bootstrap.sh
bash demos/crossplane/bootstrap/10-install-crossplane.sh
bash demos/crossplane/bootstrap/20-crossplane-azure-creds.sh
export GITHUB_TOKEN=ghp_...
bash demos/crossplane/bootstrap/30-github-creds.sh
```

[demo-gitops]: ../gitops/README.md
