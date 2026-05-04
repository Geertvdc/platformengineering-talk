#!/usr/bin/env bash
# Bridge the shared azure-credentials Secret (from demos/gitops/bootstrap/30-azure-creds.sh)
# into the JSON format expected by the Crossplane Azure provider.
#
# Reads from:  azure-creds/azure-credentials  (four separate keys)
# Writes to:   crossplane-system/azure-provider-creds  (single JSON key: credentials)
#
# No new service principal is created — the same SP is reused.
#
# Production note: prefer workload identity / federated credentials.
set -euo pipefail

SRC_NAMESPACE="azure-creds"
SRC_SECRET="azure-credentials"
DST_NAMESPACE="crossplane-system"
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

CREDS=$(cat <<EOF
{
  "clientId":                       "${CLIENT_ID}",
  "clientSecret":                   "${CLIENT_SECRET}",
  "subscriptionId":                 "${SUBSCRIPTION_ID}",
  "tenantId":                       "${TENANT_ID}",
  "activeDirectoryEndpointUrl":     "https://login.microsoftonline.com",
  "resourceManagerEndpointUrl":     "https://management.azure.com/",
  "activeDirectoryGraphResourceId": "https://graph.windows.net/",
  "sqlManagementEndpointUrl":       "https://management.core.windows.net:8443/",
  "galleryEndpointUrl":             "https://gallery.azure.com/",
  "managementEndpointUrl":          "https://management.core.windows.net/"
}
EOF
)

echo "==> Ensuring namespace '${DST_NAMESPACE}' exists"
kubectl create namespace "${DST_NAMESPACE}" --dry-run=client -o yaml | kubectl apply -f -

echo "==> Creating/updating Secret '${DST_SECRET}' in namespace '${DST_NAMESPACE}'"
kubectl -n "${DST_NAMESPACE}" create secret generic "${DST_SECRET}" \
  --from-literal=credentials="${CREDS}" \
  --dry-run=client -o yaml | kubectl apply -f -

echo "==> Done. Argo CD will now reconcile the ProviderConfig against this Secret."
