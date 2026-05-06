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

It also applies `demos/gitops/bootstrap/argocd-cm-patch.yaml` — a ConfigMap
that adds a custom Lua health check for `CompositeResourceDefinition` so that
Argo CD treats an XRD as `Healthy` only once Crossplane has set
`Established=True` **and** `Offered=True`. This is what allows the claims
Applications to wait safely for the CRDs to be registered before syncing.

### 2 — Wait for Argo CD to install Crossplane

Crossplane is managed GitOps-style via `demos/gitops/apps/crossplane-install.yaml`.
Argo CD installs it automatically from the Helm chart once the app-of-apps syncs.
Run this script to block until Crossplane is healthy before proceeding:

```bash
bash demos/crossplane/bootstrap/10-install-crossplane.sh
```

To upgrade Crossplane, change `targetRevision` in `crossplane-install.yaml` and push — Argo CD does the rest.

### 3 — Create the Azure and GitHub provider credentials Secrets

These secrets contain sensitive values and **cannot be stored in Git**. They must
be created imperatively before the providers can authenticate.

> **Production note:** in a real environment you would use
> [External Secrets Operator](https://external-secrets.io) (pulling from Azure Key Vault)
> or [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets) to manage
> these GitOps-style. For demo speed we create them directly.

**Azure credentials** (bridged from the shared SP secret created by Demo 1):

```bash
bash demos/crossplane/bootstrap/20-crossplane-azure-creds.sh
```

**GitHub credentials:**

```bash
export GITHUB_TOKEN=ghp_...   # PAT with repo + read:org + delete_repo scopes
export GITHUB_OWNER=Geertvdc  # your GitHub username or org
bash demos/crossplane/bootstrap/30-github-creds.sh
```

### 3 — Install Providers and wait for CRDs

```bash
bash demos/crossplane/bootstrap/40-install-providers.sh
```

Applies the three Provider packages and **blocks until each is `HEALTHY=True`**
(~2–3 min on first run while images pull). This pre-registers all Azure and
GitHub CRDs so Argo CD never encounters a missing resource during sync.

### 4 — Let Argo CD sync the rest

Providers live in `bootstrap/` and are managed imperatively (step 5 above).
Everything else — XRDs, Compositions, and claims — is managed by Argo CD via
four Applications in `demos/gitops/apps/`, all labelled `demo: demo-3`:

| Application | Watches | What it deploys |
|---|---|---|
| `crossplane-appstorage` | `composition/appstorage/` | XRD + Composition for AppStorage |
| `crossplane-appstorage-claims` | `samples/appstorage/` | `crossplane-demo` namespace + AppStorage claim |
| `crossplane-appteam` | `composition/appteam/` | XRD + Composition for AppTeam |
| `crossplane-appteam-claims` | `samples/appteam/` | `crossplane-demo` namespace + AppTeam claim |

**Why four apps, not one?**
Argo CD validates *all* resources in an Application before any sync wave runs.
If the XRD and the claim are in the same app, Argo CD fails the entire sync
because the `AppStorage`/`AppTeam` CRD doesn't exist yet — so wave 1 (the XRD)
never gets applied. Splitting compositions and claims into separate Applications
means:

1. `crossplane-appstorage` syncs and Crossplane registers the `AppStorage` CRD.
2. A custom Lua health check in `argocd-cm` (applied by `10-install-argocd.sh`)
   keeps the XRD app in `Progressing` until `Established=True` **and**
   `Offered=True` — only then does Argo CD consider it `Healthy`.
3. `crossplane-appstorage-claims` syncs and the claim is applied against an
   already-registered CRD.

The `crossplane.yaml` file in `demos/gitops/apps/` is intentionally empty
(placeholder comment only) — it exists so the app-of-apps directory structure
is self-documenting.

Wait for all Providers to become healthy (~2–3 min while images pull):

```bash
kubectl get providers.pkg.crossplane.io -w
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

Verify all four Argo CD Applications are healthy:

```bash
kubectl get application -n argocd -l demo=demo-3
# NAME                           SYNC STATUS   HEALTH STATUS
# crossplane-appstorage          Synced        Healthy
# crossplane-appstorage-claims   Synced        Healthy
# crossplane-appteam             Synced        Healthy
# crossplane-appteam-claims      Synced        Healthy
```

---

## The ≤ 3-minute live demo script

### Part 0 — Argo CD sees Crossplane resources as black boxes (setup for the reveal)

Before showing anything, point to the Argo CD UI and note that all resources
are already green — **Argo CD has no idea what state the underlying cloud
resources are actually in**. It just knows the YAML was applied.

Then apply the health checks:

```bash
kubectl apply -f demos/crossplane/bootstrap/argocd-cm-crossplane-health.yaml
kubectl rollout restart -n argocd deploy/argocd-repo-server
```

> _"Now Argo CD can see what Crossplane is actually doing — each resource
> reflects the real provisioning state from Azure and GitHub."_

Watch the apps update in the UI: yellow (provisioning) → green (ready).

---

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
│   ├── 40-install-providers.sh        # Apply Providers + wait for Healthy + apply ProviderConfigs
│   ├── argocd-cm-crossplane-health.yaml  # Full health checks — apply LIVE during demo (Part 0)
│   └── provider/
│       ├── provider-azure-resources.yaml  # Azure Resources provider (v2.5.4)
│       ├── provider-azure-storage.yaml    # Azure Storage provider (v2.5.4)
│       ├── provider-github.yaml           # GitHub provider (v0.19.0)
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

Argo CD Applications in `demos/gitops/apps/` (all labelled `demo: demo-3`):

| File | Watches | Purpose |
|---|---|---|
| `crossplane-install.yaml` | Helm chart | Installs Crossplane v2.2.1 via Argo CD (GitOps-managed) |
| `crossplane-appstorage.yaml` | `composition/appstorage/` | Syncs XRD + Composition for AppStorage |
| `crossplane-appstorage-claims.yaml` | `samples/appstorage/` | Syncs namespace + AppStorage claim |
| `crossplane-appteam.yaml` | `composition/appteam/` | Syncs XRD + Composition for AppTeam |
| `crossplane-appteam-claims.yaml` | `samples/appteam/` | Syncs namespace + AppTeam claim |
| `crossplane.yaml` | — | Intentional placeholder (empty); documents the split |

The compositions and claims are in **separate Applications** by design — see
step 6 of the bootstrap section for the full explanation.

The Lua health check that makes the sequencing safe lives in
`demos/gitops/bootstrap/argocd-cm-patch.yaml` and is applied by
`demos/gitops/bootstrap/10-install-argocd.sh`.

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
