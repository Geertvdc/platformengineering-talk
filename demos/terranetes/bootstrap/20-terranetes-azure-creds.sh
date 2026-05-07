#!/usr/bin/env bash
# Bridge the shared azure-credentials Secret (from demos/gitops/bootstrap/30-azure-creds.sh)
# into the format expected by the Terranetes Azure provider (ARM_* env vars).
#
# Reads from:  azure-creds/azure-credentials  (four separate keys)
# Writes to:   terranetes-system/azure-provider-creds  (ARM_* keys for OpenTofu azurerm provider)
#
# No new service principal is created — the same SP is reused.
#
# Production note: prefer workload identity / federated credentials.
set -euo pipefail

SRC_NAMESPACE="azure-creds"
SRC_SECRET="azure-credentials"
DST_NAMESPACE="terranetes-system"
DST_SECRET="azure-provider-creds"

echo "==> Reading SP credentials from ${SRC_NAMESPACE}/${SRC_SECRET}"
TENANT_ID=$(kubectl -n "${SRC_NAMESPACE}" get secret "${SRC_SECRET}" \
  -o jsonpath='{.data.AZURE_TENANT_ID}' | base64 -d)
SUBSCRIPTION_ID=$(kubectl -n "${SRC_NAMESPACE}" get secret "${SRC_SECRET}" \
  -o jsonpath='{.data.AZURE_SUBSCRIPTION_ID}' | base64 -d)
CLIENT_ID=$(kubectl -n "${SRC_NAMESPACE}" get secret "${SRC_SECRET}" \
  -o jsonpath='{.data.AZURE_CLIENT_ID}' | base64 -d)
CLIENT_SECRET=$(kubectl -n "${SRC_NAMESPACE}" get secret "${SRC_SECRET}" \
  -o jsonpath='{.data.AZURE_CLIENT_SECRET}' | base64 -d)

echo "==> Ensuring namespace '${DST_NAMESPACE}' exists"
kubectl create namespace "${DST_NAMESPACE}" --dry-run=client -o yaml | kubectl apply -f -

echo "==> Creating/updating Secret '${DST_SECRET}' in namespace '${DST_NAMESPACE}'"
# Terranetes injects these as environment variables into the OpenTofu runner pod.
# The azurerm provider picks them up automatically.
kubectl -n "${DST_NAMESPACE}" create secret generic "${DST_SECRET}" \
  --from-literal=ARM_TENANT_ID="${TENANT_ID}" \
  --from-literal=ARM_SUBSCRIPTION_ID="${SUBSCRIPTION_ID}" \
  --from-literal=ARM_CLIENT_ID="${CLIENT_ID}" \
  --from-literal=ARM_CLIENT_SECRET="${CLIENT_SECRET}" \
  --dry-run=client -o yaml | kubectl apply -f -

echo "==> Done. Next step: run demos/terranetes/bootstrap/30-github-creds.sh"
