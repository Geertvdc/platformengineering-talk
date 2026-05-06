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

### 2 — Install Crossplane

```bash
bash demos/crossplane/bootstrap/10-install-crossplane.sh
```

This adds the Crossplane Helm repo and runs `helm upgrade --install` to deploy
Crossplane into `crossplane-system`, then waits for both Deployments to be ready.

To change the Crossplane version, edit the `CROSSPLANE_VERSION` variable at the
top of the script.

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

### 4 — Install Providers and wait for CRDs

```bash
bash demos/crossplane/bootstrap/40-install-providers.sh
```

Applies the three Provider packages and **blocks until each is `HEALTHY=True`**
(~2–3 min on first run while images pull). This pre-registers all Azure and
GitHub CRDs so Argo CD never encounters a missing resource during sync.

### 4 — Let Argo CD sync the rest

Providers live in `bootstrap/` and are managed imperatively (step 4 above).
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

## The ≤ 5-minute live demo script

The demo builds in four parts. Each part is a talking point layer — you're not
rushing to provision things live, you're **narrating a story** with running
resources as props.

```
Part A — What is Crossplane?       (concepts, build the mental model)
Part B — AppStorage                (developer UX vs ASO, contrast)
Part C — AppTeam                   (multi-cloud, the wow moment)
Part D — Lua health checks         (GitOps observability, the reveal)
```

---

### Part A — Crossplane concepts walkthrough

> _"Before I show you a demo, let me walk you through the three building blocks.
> Once you have these three concepts the whole thing clicks."_

**1 — Providers**

```bash
kubectl get providers.pkg.crossplane.io
```

> _"A Provider is a Kubernetes controller that knows how to talk to a cloud API.
> Think of it as a driver. We have one for Azure Resources, one for Azure Storage,
> and one for GitHub. Each one registers its own CRDs — one CRD per cloud
> resource type it can manage."_

```bash
# Show the CRDs that the Azure storage provider registered
kubectl get crd | grep storage.azure.upbound.io
```

**2 — Managed Resources**

> _"A Managed Resource is a single cloud resource represented as a Kubernetes
> object. This is the raw, unabstracted layer — every field maps directly to
> the Azure API. You can use them directly, but developers would need to know
> every Azure field. That's what ASO gives you — and it's great for
> platform-native teams. Crossplane lets you go one level higher."_

```bash
# Show a live managed resource and its status
kubectl get account    # Azure Storage Account managed resource
kubectl get resourcegroup
kubectl get repository.repo.github.upbound.io
```

**3 — Compositions and XRDs**

> _"A CompositeResourceDefinition — XRD — is a custom API you define for your
> platform. You pick the fields developers are allowed to set. Everything else
> is fixed by the platform team. Then a Composition wires that API to the
> underlying managed resources. The developer sees your API. The platform team
> owns the implementation."_

```bash
kubectl get xrd
# xappstorages.platform.demo.io   Established=True   Offered=True
# xappteams.platform.demo.io      Established=True   Offered=True
```

> _"Two platform APIs, registered as Kubernetes CRDs, owned by us."_

---

### Part B — AppStorage (contrast with ASO)

> _"Let's look at the first one. AppStorage. Compare this to what you saw in
> the ASO demo — where developers wrote Azure YAML with SKUs and replication
> types. Here's what the developer writes with Crossplane:"_

**Show the claim:**

```bash
cat demos/crossplane/samples/appstorage/appstorage.yaml
```

> _"Eleven lines. A name and a size tier. No Azure fields. No resource group.
> No region. No replication type. The platform team chose all of that. The
> developer picked `small`."_

**Show the Composition:**

```bash
cat demos/crossplane/composition/appstorage/composition-appstorage.yaml
```

> _"This is what the platform team wrote. The `size` field maps to an LRS,
> GRS, or RAGRS replication type. Tags, naming conventions, TLS baseline —
> all baked in here. The developer never sees any of this."_

**Show it running:**

```bash
kubectl -n crossplane-appstorage-demo get appstorage demo-app-store
# SYNCED=True   READY=True

kubectl get managed | grep demoapp
```

| # | Action | Expected output |
|---|--------|-----------------|
| 1 | `cat samples/appstorage/appstorage.yaml` | 11 lines: `name` + `size` only |
| 2 | `cat composition/appstorage/composition-appstorage.yaml` | Platform-owned: tags, naming, RG, TLS |
| 3 | `kubectl -n crossplane-appstorage-demo get appstorage` | `SYNCED=True READY=True` |
| 4 | `kubectl get account` | Managed resource `stdemoapp` visible |
| 5 | Azure Portal | Storage Account with `managed-by=crossplane` tag |

---

### Part C — AppTeam (the multi-cloud moment)

> _"Now here's where Crossplane does something ASO and KRO genuinely cannot do
> alone. One claim, two cloud providers."_

**Show the claim:**

```bash
cat demos/crossplane/samples/appteam/appteam.yaml
```

> _"Ten lines. A team name and a GitHub org. That's it. Watch what happens."_

**Show the Composition:**

```bash
cat demos/crossplane/composition/appteam/composition-appteam.yaml
```

> _"Three sections. An Azure Resource Group. An Azure Storage Account inside
> that RG. And a private GitHub repository — via a completely different
> provider, a completely different cloud. One Composition, two providers."_

**Show it running:**

```bash
kubectl -n crossplane-appteam-demo get appteam techorama-team
# SYNCED=True   READY=True

kubectl get resourcegroup   # Azure RG: rg-team-techorama
kubectl get account         # Azure Storage: stteamtechorama
kubectl get repository.repo.github.upbound.io   # GitHub: techorama-platform-infra
```

> _"The developer wrote ten lines. Crossplane created an Azure Resource Group,
> a Storage Account inside it, AND a private GitHub repository — two providers,
> two clouds, one platform API."_

| # | Action | Expected output |
|---|--------|-----------------|
| 1 | `cat samples/appteam/appteam.yaml` | 10 lines: `teamName` + `githubOrg` |
| 2 | `cat composition/appteam/composition-appteam.yaml` | Three sections: RG, Account, GitHub repo |
| 3 | `kubectl -n crossplane-appteam-demo get appteam techorama-team` | `SYNCED=True READY=True` |
| 4 | `kubectl get resourcegroup,account` | Azure RG + Storage Account live |
| 5 | GitHub → `Geertvdc/techorama-platform-infra` | Private repo exists |

---

### Part D — Lua health checks (the GitOps observability reveal)

> _"One last thing. Everything you just saw is running and healthy — but watch
> what Argo CD thinks right now."_

Open the Argo CD UI and point at `crossplane-appteam-claims`. All resources
show **green hearts immediately**. There's no provisioning state. Argo CD just
knows the YAML was applied — it has no idea whether Azure actually did anything.

> _"Argo CD has no built-in knowledge of Crossplane's resource lifecycle. The
> moment the YAML lands in the cluster, it calls it Healthy. That's fine for
> YAML resources — but these aren't YAML resources. These are cloud API calls
> that might be in flight, or failing, right now."_

**Apply the full health checks:**

```bash
kubectl apply -f demos/crossplane/bootstrap/argocd-cm-crossplane-health.yaml
kubectl rollout restart -n argocd deploy/argocd-repo-server
```

> _"I've just loaded a ConfigMap with Lua scripts — one per resource kind.
> Each script reads the `Synced` and `Ready` conditions Crossplane writes onto
> every managed resource and maps them to Argo CD health states."_

Watch the UI update: **yellow** (Progressing — Crossplane is reconciling) →
**green** (Healthy — the cloud resource is live and ready).

> _"Now Argo CD actually reflects reality. Yellow means Crossplane is talking
> to Azure or GitHub right now. Green means the resource exists. Red means
> something went wrong and here's the error message. This is what GitOps
> observability looks like for cloud resources."_

**Commands to watch the transition:**

```bash
# Watch claim status
kubectl -n crossplane-appteam-demo get appteam techorama-team -w

# Watch all managed resources at once
kubectl get managed -w

# Check the argocd-cm to see what was applied
kubectl -n argocd get cm argocd-cm -o yaml | grep "resource.customizations"
```

**Reset Lua to minimal (to repeat the reveal):**

```bash
bash demos/crossplane/bootstrap/50-reset-lua.sh
```

This reverts `argocd-cm` to the minimal XRD-only health check and restarts
repo-server — so Argo CD goes back to showing everything green immediately,
ready for you to do the reveal again.

---

**Useful commands (any part):**

```bash
# All claims at once
kubectl get appstorage,appteam -A

# Everything Crossplane manages
kubectl get managed

# Azure + GitHub resources side by side
kubectl get resourcegroup,account,repository.repo.github.upbound.io

# Full XR status (shows all composed resource refs)
kubectl describe xappstorage
kubectl describe xappteam
```

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
│   ├── argocd-cm-crossplane-health.yaml  # Full health checks — apply LIVE during demo (Part D)
│   ├── 50-reset-lua.sh                # Revert argocd-cm to minimal — resets Part D reveal
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
