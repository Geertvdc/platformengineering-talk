#!/usr/bin/env bash
# Bootstrap the KRO demo on top of the shared platform.
#
# Assumes already running (installed by demos/gitops/bootstrap/bootstrap.sh):
#   - kind cluster  platformeng-demo
#   - Argo CD       (argocd namespace)
#   - ASO v2        (azureserviceoperator-system namespace)
#   - Shared azure-creds Secret (azure-creds/azure-credentials)
#
# This script is responsible ONLY for what belongs to the KRO demo:
#   1. Install the KRO controller (kro-system)
#   2. Create a dedicated Azure resource group  kro-demo-rg
#   3. Patch the subscription ID + RG into the RGD manifest
#   4. Apply the RGD (or remind to push if using GitOps)
#
# Idempotent — safe to re-run.
#
# Required env vars (sourced from demos/gitops/bootstrap/.env if present):
#   AZURE_SUBSCRIPTION_ID
#   AZURE_TENANT_ID       (needed for az CLI login check only)
#
# Optional overrides:
#   KRO_RESOURCE_GROUP   (default: kro-demo-rg)
#   KRO_LOCATION         (default: westeurope)
#   KRO_VERSION          (default: 0.2.1)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"

# ── Load shared .env if present ──────────────────────────────────────────────
ENV_FILE="${REPO_ROOT}/demos/gitops/bootstrap/.env"
if [[ -f "${ENV_FILE}" ]]; then
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
fi

# ── Validate required vars ───────────────────────────────────────────────────
: "${AZURE_SUBSCRIPTION_ID:?AZURE_SUBSCRIPTION_ID must be set (check demos/gitops/bootstrap/.env)}"

# ── Configurable defaults ────────────────────────────────────────────────────
KRO_RESOURCE_GROUP="${KRO_RESOURCE_GROUP:-kro-demo-rg}"
KRO_LOCATION="${KRO_LOCATION:-westeurope}"
KRO_VERSION="${KRO_VERSION:-0.9.1}"

RGD_FILE="${REPO_ROOT}/demos/kro/composition/rgd-myapp.yaml"

echo "════════════════════════════════════════════════════════════"
echo " KRO demo bootstrap"
echo "  Resource group : ${KRO_RESOURCE_GROUP}"
echo "  Location       : ${KRO_LOCATION}"
echo "  KRO version    : ${KRO_VERSION}"
echo "════════════════════════════════════════════════════════════"

# ── Guard: shared platform must already be running ───────────────────────────
echo
echo "==> Checking shared platform prerequisites..."

if ! kubectl get namespace argocd &>/dev/null; then
  echo "ERROR: Argo CD namespace not found. Run demos/gitops/bootstrap/bootstrap.sh first."
  exit 1
fi

if ! kubectl get namespace azureserviceoperator-system &>/dev/null; then
  echo "ERROR: ASO namespace not found. Run demos/aso/bootstrap/bootstrap.sh first."
  exit 1
fi

echo "    Shared platform looks good."

# ── Step 1: KRO controller ───────────────────────────────────────────────────
echo
echo "==> [1/3] Installing KRO controller (v${KRO_VERSION})..."
helm upgrade --install kro oci://registry.k8s.io/kro/charts/kro \
  --namespace kro-system \
  --create-namespace \
  --version "${KRO_VERSION}" \
  --wait
echo "    KRO ready."

# ── Step 2: Azure resource group (kro-specific, not shared with other demos) ─
echo
echo "==> [2/3] Creating Azure resource group '${KRO_RESOURCE_GROUP}' in '${KRO_LOCATION}'..."
az group create \
  --name "${KRO_RESOURCE_GROUP}" \
  --location "${KRO_LOCATION}" \
  --output table
echo "    Resource group ready."

# ── Step 3: Patch RGD manifest with subscription ID + RG ────────────────────
echo
echo "==> [3/3] Patching RGD manifest with subscription ID and resource group..."

ARM_ID="/subscriptions/${AZURE_SUBSCRIPTION_ID}/resourceGroups/${KRO_RESOURCE_GROUP}"

# Replace the armId line regardless of the current placeholder or previous value
sed -i.bak "s|armId:.*|armId: ${ARM_ID}|g" "${RGD_FILE}"
rm -f "${RGD_FILE}.bak"

echo "    armId set to: ${ARM_ID}"

# Apply directly to the cluster
kubectl apply -f "${RGD_FILE}"

# Create the namespace where MyApp instances are submitted
kubectl create namespace kro-demo --dry-run=client -o yaml | kubectl apply -f -

echo
echo "    Waiting for KRO to register the MyApp CRD (up to 30 s)..."
for i in $(seq 1 30); do
  if kubectl get crd myapps.kro.run &>/dev/null; then
    echo "    CRD myapps.kro.run registered."
    break
  fi
  if [[ "${i}" -eq 30 ]]; then
    echo "    WARNING: CRD not yet registered. Check: kubectl get resourcegraphdefinition myapp"
  fi
  sleep 1
done

# If using GitOps (Argo CD), also commit the patched file
if git -C "${REPO_ROOT}" rev-parse --is-inside-work-tree &>/dev/null; then
  echo
  echo "    Git repo detected. Commit the patched manifest so Argo CD stays in sync:"
  echo "      git add demos/kro/composition/rgd-myapp.yaml"
  echo "      git commit -m 'kro: set subscription ID and resource group'"
  echo "      git push"
fi

echo
echo "════════════════════════════════════════════════════════════"
echo " Bootstrap complete."
echo
echo " Verify:"
echo "   kubectl get resourcegraphdefinition myapp"
echo "   kubectl get crd myapps.kro.run"
echo
echo " Pre-validate (rehearsal):"
echo "   kubectl apply -f demos/kro/samples/myapp.yaml"
echo "   kubectl get namespace myapp"
echo "   kubectl get rolebinding -n myapp"
echo "   kubectl get storageaccount -n myapp -w"
echo "   kubectl get secret myapp-connection -n myapp"
echo
echo " Reset after rehearsal:"
echo "   kubectl delete -f demos/kro/samples/myapp.yaml"
echo "   kubectl delete namespace myapp --ignore-not-found"
echo "════════════════════════════════════════════════════════════"
