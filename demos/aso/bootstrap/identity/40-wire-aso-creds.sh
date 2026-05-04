#!/usr/bin/env bash
# Wire the shared azure-creds/azure-credentials Secret into ASO's controller
# namespace so that ASO can authenticate to Azure without a separate SP.
#
# This script MUST be run AFTER:
#   1. bootstrap/30-azure-creds.sh  (creates azure-creds/azure-credentials)
#   2. The ASO Helm install (creates azureserviceoperator-system namespace)
#
# It reads the four credential fields from the shared Secret and creates (or
# updates) the `aso-controller-settings` Secret that ASO's controller reads at
# startup.
#
# Production note: use workload identity / federated credentials instead.
set -euo pipefail

SOURCE_NAMESPACE="azure-creds"
SOURCE_SECRET="azure-credentials"
TARGET_NAMESPACE="azureserviceoperator-system"
TARGET_SECRET="aso-controller-settings"

echo "==> Reading credentials from '${SOURCE_NAMESPACE}/${SOURCE_SECRET}'"

AZURE_SUBSCRIPTION_ID="$(kubectl get secret "${SOURCE_SECRET}" \
  --namespace "${SOURCE_NAMESPACE}" \
  -o jsonpath='{.data.AZURE_SUBSCRIPTION_ID}' | base64 -d)"

AZURE_TENANT_ID="$(kubectl get secret "${SOURCE_SECRET}" \
  --namespace "${SOURCE_NAMESPACE}" \
  -o jsonpath='{.data.AZURE_TENANT_ID}' | base64 -d)"

AZURE_CLIENT_ID="$(kubectl get secret "${SOURCE_SECRET}" \
  --namespace "${SOURCE_NAMESPACE}" \
  -o jsonpath='{.data.AZURE_CLIENT_ID}' | base64 -d)"

AZURE_CLIENT_SECRET="$(kubectl get secret "${SOURCE_SECRET}" \
  --namespace "${SOURCE_NAMESPACE}" \
  -o jsonpath='{.data.AZURE_CLIENT_SECRET}' | base64 -d)"

echo "==> Creating/updating '${TARGET_SECRET}' in namespace '${TARGET_NAMESPACE}'"
kubectl create secret generic "${TARGET_SECRET}" \
  --namespace "${TARGET_NAMESPACE}" \
  --from-literal=AZURE_SUBSCRIPTION_ID="${AZURE_SUBSCRIPTION_ID}" \
  --from-literal=AZURE_TENANT_ID="${AZURE_TENANT_ID}" \
  --from-literal=AZURE_CLIENT_ID="${AZURE_CLIENT_ID}" \
  --from-literal=AZURE_CLIENT_SECRET="${AZURE_CLIENT_SECRET}" \
  --dry-run=client -o yaml | kubectl apply -f -

echo "==> Restarting ASO controller to pick up the new credentials"
kubectl rollout restart deployment/azureserviceoperator-controller-manager \
  --namespace "${TARGET_NAMESPACE}"
kubectl rollout status deployment/azureserviceoperator-controller-manager \
  --namespace "${TARGET_NAMESPACE}" --timeout=3m

echo "==> Done. ASO is now authenticated using the shared azure-creds Secret."
