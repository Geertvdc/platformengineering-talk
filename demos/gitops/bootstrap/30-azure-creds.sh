#!/usr/bin/env bash
# Create the shared Azure service principal Secret consumed by the ASO,
# Crossplane, KRO and Terranetes demos (#2-#5).
#
# Reads credentials from environment variables so nothing sensitive is ever
# written to disk or committed. Populate these locally before the talk:
#
#   export AZURE_TENANT_ID=...
#   export AZURE_SUBSCRIPTION_ID=...
#   export AZURE_CLIENT_ID=...
#   export AZURE_CLIENT_SECRET=...
#
# Production note: this SP-with-secret pattern is purely for live-demo speed.
# In production, use workload identity / federated credentials instead.
set -euo pipefail

NAMESPACE="azure-creds"
SECRET_NAME="azure-credentials"

: "${AZURE_TENANT_ID:?AZURE_TENANT_ID must be set}"
: "${AZURE_SUBSCRIPTION_ID:?AZURE_SUBSCRIPTION_ID must be set}"
: "${AZURE_CLIENT_ID:?AZURE_CLIENT_ID must be set}"
: "${AZURE_CLIENT_SECRET:?AZURE_CLIENT_SECRET must be set}"

echo "==> Creating namespace '${NAMESPACE}'"
kubectl create namespace "${NAMESPACE}" --dry-run=client -o yaml | kubectl apply -f -

echo "==> Creating/updating Secret '${SECRET_NAME}' in namespace '${NAMESPACE}'"
kubectl create secret generic "${SECRET_NAME}" \
  --namespace "${NAMESPACE}" \
  --from-literal=AZURE_TENANT_ID="${AZURE_TENANT_ID}" \
  --from-literal=AZURE_SUBSCRIPTION_ID="${AZURE_SUBSCRIPTION_ID}" \
  --from-literal=AZURE_CLIENT_ID="${AZURE_CLIENT_ID}" \
  --from-literal=AZURE_CLIENT_SECRET="${AZURE_CLIENT_SECRET}" \
  --dry-run=client -o yaml | kubectl apply -f -

echo "==> Done."
