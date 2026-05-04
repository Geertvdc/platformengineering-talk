# Demo: GitOps with Argo CD

> **Section 3 — first live demo of the talk.** This demo establishes the
> foundation every later demo (ASO, Crossplane, KRO, Terranetes) builds on:
> a local kind cluster, Argo CD installed, an App-of-Apps repo layout, and a
> shared Azure credential Secret. If you change anything here, update the
> other demo issues too.

---

## Why kind, not AKS

We run a local **kind** cluster on the laptop:

- Boots in seconds — no Azure provisioning latency between demos
- Fully reproducible: `kind delete cluster && kind create cluster` resets everything
- Survives flaky conference Wi-Fi (only outbound traffic is to Azure ARM for
  the resource creations done in later demos)

**Trade-off:** workload identity is awkward inside kind. We use a service
principal + client secret for Azure auth in the demos. **In production, use
workload identity / federated credentials.** Call this out on stage.

---

## Prereqs

Install on the laptop before the talk:

- Docker (running)
- [`kind`](https://kind.sigs.k8s.io/) ≥ v0.24
- `kubectl` ≥ v1.30
- `helm` ≥ v3.14 (only needed if you swap the manifest install for the chart)
- A **GitHub Personal Access Token** (PAT) with `repo` (or `contents: read`)
  access — needed so Argo CD can clone this repository if it is private:

  ```bash
  export GITHUB_TOKEN=ghp_...
  export GITHUB_USER=<your-github-username>   # optional, defaults to 'git'
  ```

  These are read by `bootstrap/15-add-github-repo.sh` and registered as an
  Argo CD repository secret. They are **never** written to disk and **never**
  committed.

- An Azure service principal with **Contributor** on a single sandbox resource
  group, exported as env vars:

  ```bash
  export AZURE_TENANT_ID=...
  export AZURE_SUBSCRIPTION_ID=...
  export AZURE_CLIENT_ID=...
  export AZURE_CLIENT_SECRET=...
  ```

  These are read by `bootstrap/30-azure-creds.sh`. They are **never** written
  to disk and **never** committed.

---

## Bootstrap (run before the talk, NOT live)

Single command:

```bash
./demos/gitops/bootstrap/bootstrap.sh
```

This wraps the four numbered scripts:

1. `00-create-cluster.sh` — creates the `platformeng-demo` kind cluster from
   `kind-config.yaml`
2. `10-install-argocd.sh` — installs Argo CD into the `argocd` namespace and
   applies the App-of-Apps root (`20-apply-root-app.yaml`)
3. `15-add-github-repo.sh` — registers this GitHub repo with Argo CD using
   `GITHUB_TOKEN` so Argo CD can clone it (required if the repo is private)
4. `30-azure-creds.sh` — creates the shared `azure-credentials` Secret in the
   `azure-creds` namespace from your env vars (skipped if env vars are unset)

Then, in a separate terminal, port-forward the Argo CD UI and grab the admin
password:

```bash
kubectl -n argocd port-forward svc/argocd-server 8080:443 &
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath='{.data.password}' | base64 -d && echo
```

Open <https://localhost:8080> (user: `admin`) and confirm the `app-of-apps`
and `gitops-demo` Applications are **Synced** and **Healthy**. Now you're
ready to present.

---

## The 2-minute live demo script

Goal: make GitOps visceral — drift detection + self-healing on a trivial
workload — so the audience trusts the reconciliation loop before later demos
provision real Azure resources through it.

| # | Action | Expected UI / output |
|---|---|---|
| 1 | Open Argo CD UI | `app-of-apps` and `gitops-demo` both **Synced / Healthy** |
| 2 | `kubectl -n gitops-demo edit deploy/demo-nginx` and change `replicas: 2` → `5`, save | Deployment briefly scales to 5 pods |
| 3 | Switch to the Argo CD UI, watch `gitops-demo` | Goes **OutOfSync** (red) within seconds |
| 4 | Wait | Auto-sync + self-heal revert it back to 2 replicas, **Synced / Healthy** again in &lt; 30s |
| 5 | One-liner | _"Everything you'll see in the next four demos flows through this exact loop."_ |

Total target: **≤ 2 minutes** with a stopwatch.

---

## Repo layout

```
demos/gitops/
├── bootstrap/
│   ├── bootstrap.sh              # one-shot wrapper for the three scripts below
│   ├── kind-config.yaml          # kind cluster definition
│   ├── 00-create-cluster.sh      # create / recreate the kind cluster
│   ├── 10-install-argocd.sh      # install Argo CD + apply root App
│   ├── 15-add-github-repo.sh     # register GitHub repo creds with Argo CD
│   ├── 20-apply-root-app.yaml    # App-of-Apps root Application
│   ├── 30-azure-creds.sh         # creates the shared Secret from env vars
│   └── azure-creds.template.yaml # SP credential Secret template (no values)
├── apps/                         # App-of-Apps targets (one file per demo)
│   └── gitops-demo.yaml          # this demo's Application (nginx workload)
│   # aso.yaml         <-- added by demo #2
│   # crossplane.yaml  <-- added by demo #3
│   # kro.yaml         <-- added by demo #4
│   # terranetes.yaml  <-- added by demo #5
├── workloads/
│   └── nginx/                    # tiny workload used for the drift demo
│       ├── deployment.yaml
│       └── service.yaml
└── README.md
```

---

## Shared Azure credential pattern

Used by demos #2 (ASO), #3 (Crossplane), #4 (KRO), #5 (Terranetes).

- **One** Azure service principal with **Contributor** on a single sandbox
  resource group.
- Stored as a single Kubernetes Secret named `azure-credentials` in
  namespace `azure-creds`, with these keys:
  - `AZURE_TENANT_ID`
  - `AZURE_SUBSCRIPTION_ID`
  - `AZURE_CLIENT_ID`
  - `AZURE_CLIENT_SECRET`
- Each tool demo references this Secret (or copies the needed fields into
  its own controller namespace). **No demo creates its own service
  principal.**
- `bootstrap/azure-creds.template.yaml` shows the shape; never commit a
  populated copy. The repo `.gitignore` excludes `azure-creds.local.*` and
  `*.env` to make this hard to do by accident.

> **Production:** workload identity / federated credentials. The SP-with-
> secret pattern here is for demo speed only.

---

## Conventions for later demos (#2–#5)

Every later demo MUST:

1. Add **exactly one** `Application` file under `demos/gitops/apps/`,
   pointing at its own folder (`demos/aso/`, `demos/crossplane/`,
   `demos/kro/`, `demos/terranetes/`).
2. Set `spec.syncPolicy.automated.selfHeal: true` on that Application.
3. Deploy into its **own destination namespace** (do not share namespaces
   between demos).
4. Consume the shared `azure-creds/azure-credentials` Secret rather than
   provisioning its own identity.
5. **Not** modify anything under `bootstrap/` or another demo's folder.

The App-of-Apps root in `bootstrap/20-apply-root-app.yaml` recurses
`demos/gitops/apps/`, so a new demo just drops its file in and Argo CD
picks it up on the next sync.

---

## Resetting between rehearsals

```bash
kind delete cluster --name platformeng-demo
./demos/gitops/bootstrap/bootstrap.sh
```

Everything is declarative — the cluster comes back identical.
