# Demo: Terranetes — Terraform under Kubernetes Control

> **Section 5** — ~5 min slot (≤ 3 min live, rest pre-bootstrapped).
> Builds on [Demo 1 (GitOps)][demo-gitops]: kind cluster + Argo CD + shared `azure-creds`.

---

## The talking point

Crossplane (Demo 3) requires a **Kubernetes provider** for each API it manages.
Terranetes takes a different approach: it runs **OpenTofu (open-source Terraform)
directly inside your cluster**, giving you access to the entire Terraform provider
ecosystem — 1 000+ providers — without writing a single line of Go.

The same multi-cloud story from Crossplane's `AppTeam` applies here, but now:

| | Crossplane | Terranetes |
|---|---|---|
| Abstraction | XRD + Composition (Go/YAML) | Terraform module (HCL) |
| Provider ecosystem | Upbound providers only | 1 000+ Terraform providers |
| State | Stored in K8s Secrets | Stored in K8s Secrets |
| GitOps | Yes (via Argo CD) | Yes (via Argo CD) |
| Developer UX | `AppTeam` claim | `CloudResource` YAML |

**Demo composition (mirrors Crossplane's AppTeam):**
One `CloudResource` → Terranetes runs OpenTofu → creates:
1. **Azure Resource Group** (`hashicorp/azurerm` provider)
2. **GitHub repository** (`integrations/github` provider)

---

## Prereqs

Everything from [Demo 1 (GitOps)][demo-gitops] plus:

| Tool | Version | Why |
|------|---------|-----|
| `helm` | ≥ v3.14 | Install Terranetes via Helm |
| Azure SP | Contributor on sandbox subscription | Same SP as other demos |
| `GITHUB_TOKEN` | PAT with `repo`, `delete_repo` scopes | GitHub provider authentication |

```bash
export GITHUB_TOKEN=ghp_...
```

---

## Bootstrap (run before the talk, NOT live)

### 1 — Ensure Demo 1 is bootstrapped

```bash
./demos/gitops/bootstrap/bootstrap.sh
```

### 2 — Install Terranetes

```bash
bash demos/terranetes/bootstrap/10-install-terranetes.sh
```

Installs the Terranetes controller into `terranetes-system` via Helm and waits
for it to be ready. Registers the Terranetes CRDs:

```bash
kubectl get crd | grep terraform.appvia.io
# configurations.terraform.appvia.io
# providers.terraform.appvia.io
# policies.terraform.appvia.io
# revisions.terraform.appvia.io
# cloudresources.terraform.appvia.io
```

### 3 — Create Azure and GitHub credentials Secrets

These secrets contain sensitive values and **cannot be stored in Git**.

**Azure credentials** (bridged from the shared SP secret created by Demo 1):

```bash
bash demos/terranetes/bootstrap/20-terranetes-azure-creds.sh
```

**GitHub credentials:**

```bash
export GITHUB_TOKEN=ghp_...   # PAT with repo + delete_repo scopes
bash demos/terranetes/bootstrap/30-github-creds.sh
```

### 4 — Configure the Azure Provider

```bash
bash demos/terranetes/bootstrap/40-configure-providers.sh
```

Applies `provider/provider-azure.yaml` and waits for the Provider to be ready.

### 5 — Let Argo CD sync the rest

Two Applications in `demos/gitops/apps/` are picked up automatically by the
App-of-Apps root:

| Application | Watches | What it deploys |
|---|---|---|
| `terranetes-configuration` | `configuration/` | Namespace + Revision (platform template) |
| `terranetes-team` | `samples/team/` | Namespace + live demo CloudResource instance |

```bash
kubectl get application -n argocd -l demo=demo-5
# NAME                        SYNC STATUS   HEALTH STATUS
# terranetes-configuration    Synced        Healthy
# terranetes-team             Synced        Healthy
```

---

## The ≤ 3-minute live demo script

```
Part A — What is Terranetes?   (30s — contrast with Crossplane)
Part B — Show the module       (30s — it's just Terraform HCL)
Part C — Apply via GitOps      (60s — watch ArgoCD sync + job run)
Part D — Verify results        (30s — Azure RG + GitHub repo exist)
```

---

### Part A — What is Terranetes?

```bash
kubectl get providers.terraform.appvia.io
# NAME    AGE    READY
# azure   2m     True
```

> _"Terranetes is a Kubernetes controller that runs OpenTofu — the open-source
> Terraform fork — inside your cluster. Instead of writing a new Kubernetes
> controller for every API, you write a Terraform module. 1 000 providers,
> no Go required."_

```bash
kubectl get crd | grep terraform.appvia.io
```

> _"The key resource is `Configuration`. You point it at a Terraform module,
> give it variables, and Terranetes reconciles it — forever. Drift in Azure?
> Next reconcile loop fixes it."_

---

### Part B — Show the Terraform module

```bash
cat demos/terranetes/module/main.tf
```

> _"This is the module. Two providers — azurerm and github. Stored in Git,
> versioned, reviewed like any other code. The developer never sees this — they
> just set variables in their Configuration."_

---

### Part C — Apply via GitOps (already running via Argo CD)

Show the Argo CD UI: `terranetes-team` Application should be **Synced / Healthy**
(or **Progressing** if you time it right).

Show the running OpenTofu job:

```bash
# The CloudResource (developer-facing object)
kubectl get cloudresource -n terranetes-demo

# The plan/apply Jobs run in terranetes-system (controller-managed namespace)
kubectl get jobs -n terranetes-system

# Stream logs from the running job
kubectl logs -n terranetes-system \
  -l terraform.appvia.io/configuration=azurefest-team-fth7r --tail=100 -f
```

> _"Terranetes spawned a Job that runs `tofu plan` then `tofu apply`. The state is
> stored in a Kubernetes Secret — no remote backend needed for the demo. In
> production, you'd point it at Azure Blob Storage."_

---

### Part D — Verify results

```bash
# Azure Resource Group
az group show --name rg-azurefest-demo-dev --query name -o tsv

# GitHub repository
gh repo view Geertvdc/azurefest-demo-platform-infra
```

> _"One CloudResource YAML. Two providers. Two cloud resources. The same
> multi-cloud story as Crossplane — but with the entire Terraform ecosystem
> available on day one."_

Show the outputs stored in Kubernetes:

```bash
kubectl get secret azurefest-team-outputs -n terranetes-demo -o yaml
```

---

## Repo layout

```
demos/terranetes/
├── bootstrap/
│   ├── 10-install-terranetes.sh       # install Terranetes controller via Helm
│   ├── 20-terranetes-azure-creds.sh   # bridge shared SP secret → ARM_* env vars
│   ├── 30-github-creds.sh             # create GITHUB_TOKEN secret
│   └── 40-configure-providers.sh      # apply provider-azure.yaml + wait
├── provider/
│   └── provider-azure.yaml            # Terranetes Provider (references secret)
├── module/                            # Terraform module — the platform team owns this
│   ├── main.tf                        # azurerm + github resources
│   ├── variables.tf                   # typed inputs with validation
│   └── outputs.tf                     # Azure RG name/id, GitHub repo URL
├── configuration/
│   └── teaminfra-revision.yaml        # Revision = platform template (managed by Argo CD)
├── samples/
│   └── team/                          # live demo instance (what the developer applies)
│       ├── namespace.yaml
│       └── cloudresource.yaml         # CloudResource references the Revision
└── README.md
```

Argo CD Application files live under `demos/gitops/apps/`:
- `terranetes.yaml` — placeholder comment
- `terranetes-configuration.yaml` — watches `configuration/`
- `terranetes-team.yaml` — watches `samples/team/`

---

## Shared Azure credential pattern

Same pattern as Demos 2–4:

- **One** Azure SP, **Contributor** on the sandbox subscription.
- Stored as `azure-creds/azure-credentials` by Demo 1 bootstrap.
- `20-terranetes-azure-creds.sh` reads the four keys and creates
  `terranetes-system/azure-provider-creds` with `ARM_*` env vars.
- `30-github-creds.sh` patches `GITHUB_TOKEN` into `azure-provider-creds`
  (so the Terraform `integrations/github` provider picks it up from the
  environment) and also creates `terranetes-demo/git-module-creds` with
  `GIT_USERNAME=x-access-token` + `GIT_PASSWORD=TOKEN` for authenticating
  the git clone of this private module repo (referenced via
  `spec.configuration.auth` in the Revision).

> **Production:** use workload identity / federated credentials + External Secrets
> Operator. The SP-with-secret pattern here is for demo speed only.

---

## Resetting between rehearsals

```bash
# Remove Terranetes resources (this destroys the cloud infrastructure)
kubectl delete cloudresource --all -n terranetes-demo

# Uninstall Terranetes
helm uninstall terranetes-controller -n terranetes-system
kubectl delete namespace terranetes-system terranetes-demo

# Reinstall
bash demos/terranetes/bootstrap/10-install-terranetes.sh
bash demos/terranetes/bootstrap/20-terranetes-azure-creds.sh
export GITHUB_TOKEN=ghp_...
bash demos/terranetes/bootstrap/30-github-creds.sh
bash demos/terranetes/bootstrap/40-configure-providers.sh
```

[demo-gitops]: ../gitops/README.md
