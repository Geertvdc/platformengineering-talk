# Installing Azure Service Operator (ASO) v2

> **Run this once before the talk, NOT live.** The controller is heavy enough
> that installing it on stage would waste your time slot.

## Prerequisites

- `helm` ≥ 3.14
- `kubectl` pointing at the `platformeng-demo` kind cluster
- The shared `azure-creds/azure-credentials` Secret already created by
  `demos/gitops/bootstrap/30-azure-creds.sh`

---

## Step 1 — Add the ASO Helm repository

```bash
helm repo add aso2 https://raw.githubusercontent.com/Azure/azure-service-operator/main/v2/charts
helm repo update
```

## Step 1b — Install cert-manager (required by ASO)

```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.yaml

# Wait for cert-manager to be ready before proceeding
kubectl rollout status deployment/cert-manager -n cert-manager --timeout=3m
kubectl rollout status deployment/cert-manager-webhook -n cert-manager --timeout=3m
kubectl rollout status deployment/cert-manager-cainjector -n cert-manager --timeout=3m

# Verify cert-manager CRDs are installed
kubectl get crds | grep cert-manager.io
# Expected: certificates.cert-manager.io, issuers.cert-manager.io, clusterissuers.cert-manager.io, etc.

# Verify all cert-manager pods are running
kubectl get pods -n cert-manager
# Expected: all pods in Running state
```

---

## Step 2 — Install the ASO v2 controller

Install into `azureserviceoperator-system`. The `--set` flags inject
credentials directly so the controller starts authenticated immediately.
These env vars must already be exported in your shell (set by your
`bootstrap/.env` or the terminal session running the full bootstrap).

```bash
helm install --devel aso2 aso2/azure-service-operator \
  --create-namespace \
  --namespace azureserviceoperator-system \
  --set azureSubscriptionID="${AZURE_SUBSCRIPTION_ID}" \
  --set azureTenantID="${AZURE_TENANT_ID}" \
  --set azureClientID="${AZURE_CLIENT_ID}" \
  --set azureClientSecret="${AZURE_CLIENT_SECRET}" \
  --set crdPattern="resources.azure.com/*;storage.azure.com/*;managedidentity.azure.com/*" \
  --wait --timeout=10m
```

> **Timeout note:** On a kind cluster the controller image pull can take a few
> minutes. If you still hit a timeout, check progress with:
> ```bash
> kubectl get pods -n azureserviceoperator-system
> kubectl describe pod -n azureserviceoperator-system -l app=azure-service-operator
> ```
> Common causes:
> - **`ContainerCreating`** — image is still pulling, just wait.
> - **`CrashLoopBackOff`** — the controller started but immediately exited, almost always a credential problem. Check the logs:
>   ```bash
>   kubectl logs -n azureserviceoperator-system -l app=azure-service-operator --previous
>   ```
>   Then verify your env vars are actually set before re-running the install:
>   ```bash
>   echo $AZURE_SUBSCRIPTION_ID $AZURE_TENANT_ID $AZURE_CLIENT_ID $AZURE_CLIENT_SECRET
>   ```
>   If any are empty, re-source your `.env` file and uninstall before retrying:
>   ```bash
>   helm uninstall aso2 -n azureserviceoperator-system
>   source demos/aso/bootstrap/.env
>   # then re-run the helm install
>   ```

> **What this does:** Helm deploys the CRD bundle (which includes
> `StorageAccount`, `ResourceGroup`, `RoleAssignment`, and hundreds of other
> Azure resource types) and the controller Deployment into
> `azureserviceoperator-system`. The credentials are stored in a Secret named
> `aso-controller-settings` in that namespace.

---

## Step 3 — Verify the controller is healthy

```bash
kubectl get deployment -n azureserviceoperator-system
# Expected: azureserviceoperator-controller-manager   1/1   Running
```

---

## Step 4 — Wire the shared `azure-creds` Secret (if re-deploying)

If you need to update the ASO credentials after the initial install — for
example after rotating the service principal or re-running bootstrap — use
the helper script rather than re-running Helm:

```bash
bash demos/aso/bootstrap/identity/40-wire-aso-creds.sh
```

This reads the four credential fields from `azure-creds/azure-credentials`
and creates (or updates) `aso-controller-settings` in
`azureserviceoperator-system`, then restarts the controller to pick them up.

The template `identity/aso-controller-settings.template.yaml` documents the
shape of that Secret for reference — never commit a populated copy.

---

## Credential model (explain on stage)

| Layer | Mechanism used here | Production path |
|---|---|---|
| Azure auth | Service principal + client secret | Workload identity / federated credentials |
| Credential storage | K8s Secret in controller namespace | Azure Key Vault + CSI driver |
| Scope | Contributor on one sandbox RG | Least-privilege role per-resource |

> **Talking point:** "This demo uses a service principal for speed. On a real
> cluster you'd use workload identity — the pod gets a managed identity and
> there's no secret to rotate."

---

## Uninstalling

```bash
helm uninstall aso2 -n azureserviceoperator-system
```

> **Warning:** Uninstalling the controller while ASO-managed resources exist
> will leave those Azure resources **orphaned** (not deleted). Delete the
> Kubernetes resources first, wait for them to disappear from Azure, then
> uninstall the controller.
