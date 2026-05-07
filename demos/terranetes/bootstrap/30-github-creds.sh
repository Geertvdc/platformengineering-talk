#!/usr/bin/env bash
# Add GITHUB_TOKEN to the azure-provider-creds secret.
#
# Terranetes Providers inject ALL keys from their secretRef as environment
# variables into the OpenTofu runner pod. By patching GITHUB_TOKEN into
# the same secret used by the 'azure' Provider, the integrations/github
# Terraform provider picks it up automatically — no second Provider needed.
#
# Reads from: GITHUB_TOKEN environment variable.
# Patches:    terranetes-system/azure-provider-creds  (adds GITHUB_TOKEN key)
#
# Required PAT scopes:
#   repo, delete_repo
#
# The token is NEVER written to disk or committed. Set it before the talk:
#   export GITHUB_TOKEN=ghp_...
#
# Prerequisites: 20-terranetes-azure-creds.sh must have run first.
set -euo pipefail

: "${GITHUB_TOKEN:?GITHUB_TOKEN must be set (PAT with repo + delete_repo scopes)}"

NAMESPACE="terranetes-system"
SECRET="azure-provider-creds"

echo "==> Verifying '${SECRET}' exists in namespace '${NAMESPACE}'"
kubectl -n "${NAMESPACE}" get secret "${SECRET}" > /dev/null

echo "==> Patching GITHUB_TOKEN into '${NAMESPACE}/${SECRET}'"
ENCODED=$(echo -n "${GITHUB_TOKEN}" | base64)
kubectl -n "${NAMESPACE}" patch secret "${SECRET}" \
  --type=merge \
  -p "{\"data\":{\"GITHUB_TOKEN\":\"${ENCODED}\"}}"

echo "==> Done. The 'azure' Provider will now inject GITHUB_TOKEN into OpenTofu runner pods."
echo "    Next: run demos/terranetes/bootstrap/40-configure-providers.sh"
