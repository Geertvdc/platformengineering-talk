# Install Crossplane — Bootstrap Guide

> **Run before the talk, NOT live.**
> Crossplane installs as a controller inside the kind cluster. The Azure Storage
> provider and a shared credential Secret are also pre-configured here so that
> the XRD + Composition are immediately available when the developer applies
> the sample CR during the live demo.

---

## Prerequisites

- `kubectl` context pointing at the `platformeng-demo` kind cluster
  (`kubectl config use-context kind-platformeng-demo`)
- `helm` ≥ v3.14
- Shared `azure-credentials` Secret already in `azure-creds` namespace
  (created by `demos/gitops/bootstrap/30-azure-creds.sh`)

---

## Step 1 — Install Crossplane via Helm

```bash
helm repo add crossplane-stable https://charts.crossplane.io/stable
helm repo update

helm upgrade --install crossplane crossplane-stable/crossplane \
  --namespace crossplane-system \
  --create-namespace \
  --version 1.17.1 \
  --wait
```

Verify:

```bash
kubectl -n crossplane-system get pods
# NAME                                       READY   STATUS    RESTARTS
# crossplane-xxxx                            1/1     Running   0
# crossplane-rbac-manager-xxxx              1/1     Running   0
```

---

## Step 2 — Create the Azure provider credentials Secret

The Crossplane Azure provider expects credentials as a single JSON blob.
Run the bridge script to derive it from the shared `azure-credentials` Secret:

```bash
bash demos/crossplane/bootstrap/20-crossplane-azure-creds.sh
```

This reads the four fields from `azure-creds/azure-credentials` and writes a
new Secret `crossplane-system/azure-provider-creds` with key `credentials`
(JSON format). **No new service principal is created — the same SP is reused.**

> **Production:** Use workload identity / federated credentials. The
> SP-with-secret pattern here is for demo speed only.

---

## Step 3 — Let Argo CD sync the Provider + ProviderConfig

Once the `crossplane-demo` Application is registered (added to
`demos/gitops/apps/crossplane.yaml`), Argo CD automatically applies:

- `bootstrap/provider/provider-azure-storage.yaml` — installs the
  `upbound/provider-azure-storage` package into Crossplane
- `bootstrap/provider/providerconfig.yaml` — wires the Provider to the
  `azure-provider-creds` Secret

Wait for the Provider to become healthy (typically 2–3 minutes while the
provider image pulls):

```bash
kubectl get provider upbound-provider-azure-storage
# NAME                              INSTALLED   HEALTHY   PACKAGE
# upbound-provider-azure-storage   True        True      ...
```

---

## Step 4 — Verify XRD + Composition are ready

Argo CD also applies the XRD and Composition from `composition/`. Confirm:

```bash
kubectl get compositeresourcedefinition xappstorages.platform.demo.io
# NAME                              ESTABLISHED   OFFERED   AGE
# xappstorages.platform.demo.io   True          True      ...

kubectl get composition xappstorages-azure
# NAME                  AGE
# xappstorages-azure   ...
```

---

## Step 5 — Pre-create the sandbox resource group

The Composition targets `rg-platform-demo`. Create it if it does not exist:

```bash
az group create --name rg-platform-demo --location westeurope \
  --tags managed-by=crossplane platform=true environment=demo
```

---

## Done — cluster is warm for the live demo

At this point:
- Crossplane controller is running
- Azure Storage provider is healthy
- XRD + Composition are applied (developer CR resolves immediately)
- Sandbox RG exists

Proceed to `demos/crossplane/README.md` for the live demo script.
