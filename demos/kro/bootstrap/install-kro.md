# Install KRO — Bootstrap Guide

> **Run before the talk, NOT live.**
> KRO installs as a controller inside the kind cluster. The
> `ResourceGraphDefinition` is applied via Argo CD so that the custom `MyApp`
> CRD is registered and ready before the developer CR is committed during the
> live demo.

---

## Prerequisites

- `kubectl` context pointing at the `platformeng-demo` kind cluster
  (`kubectl config use-context kind-platformeng-demo`)
- `helm` ≥ v3.14
- Demo #1 (GitOps / Argo CD App-of-Apps) already running
- Demo #2 (ASO) already installed and healthy — KRO composes ASO resources
- Shared `azure-credentials` Secret in the `azure-creds` namespace
  (created by `demos/gitops/bootstrap/30-azure-creds.sh`)
- Sandbox resource group `aso-demo-rg` pre-created in Azure (same RG as Demo #2)

---

## Step 1 — Install the KRO controller via Helm

```bash
helm repo add kro https://kro.run/charts
helm repo update

helm upgrade --install kro kro/kro \
  --namespace kro-system \
  --create-namespace \
  --version 0.2.1 \
  --wait
```

Verify:

```bash
kubectl -n kro-system get pods
# NAME                             READY   STATUS    RESTARTS
# kro-controller-manager-xxxx     1/1     Running   0
```

---

## Step 2 — Confirm the Argo CD Application is registered

The `kro.yaml` Application was added to `demos/gitops/apps/` when this demo
was bootstrapped. Check that Argo CD has picked it up:

```bash
kubectl get application kro-demo -n argocd
# NAME       SYNC STATUS   HEALTH STATUS
# kro-demo   Synced        Healthy
```

If the Application is missing, confirm `demos/gitops/apps/kro.yaml` is on
`main` and the App-of-Apps has synced:

```bash
kubectl get application app-of-apps -n argocd
```

---

## Step 3 — Apply the ResourceGraphDefinition

The `rgd-myapp.yaml` is tracked by Argo CD in the `kro.yaml` Application.
If you need to apply it manually (e.g., during bootstrap before the Argo CD
sync runs):

```bash
# Edit the REPLACE_WITH_SUBSCRIPTION_ID placeholder first
sed -i "s/REPLACE_WITH_SUBSCRIPTION_ID/${AZURE_SUBSCRIPTION_ID}/" \
  demos/kro/composition/rgd-myapp.yaml

kubectl apply -f demos/kro/composition/rgd-myapp.yaml
```

Verify the custom CRD is registered by KRO:

```bash
kubectl get resourcegraphdefinition myapp
# NAME    SYNCED   READY
# myapp   True     True

kubectl get crd myapps.kro.run
# NAME              ESTABLISHED
# myapps.kro.run   True
```

---

## Step 4 — Customise the subscription ID placeholder

Open `demos/kro/composition/rgd-myapp.yaml` and replace
`REPLACE_WITH_SUBSCRIPTION_ID` with your Azure subscription ID. Commit and
push to `main` so Argo CD can sync it:

```bash
SUBSCRIPTION_ID=$(az account show --query id -o tsv)
sed -i "s/REPLACE_WITH_SUBSCRIPTION_ID/${SUBSCRIPTION_ID}/" \
  demos/kro/composition/rgd-myapp.yaml
git add demos/kro/composition/rgd-myapp.yaml
git commit -m "kro: set subscription ID in RGD"
git push
```

---

## Step 5 — Pre-validate end-to-end (rehearsal only)

```bash
# Apply the developer CR
kubectl apply -f demos/kro/samples/myapp.yaml

# Wait for KRO to reconcile (~5 s for K8s resources, ~30-60 s for ASO)
kubectl get myapp myapp -n kro-demo -w

# Check composed resources
kubectl get namespace myapp
kubectl get rolebinding -n myapp
kubectl get storageaccount -n myapp -w   # waits for ASO to provision
kubectl get secret myapp-connection -n myapp  # written by ASO on success

# Clean up after rehearsal
kubectl delete -f demos/kro/samples/myapp.yaml
kubectl delete namespace myapp
```
