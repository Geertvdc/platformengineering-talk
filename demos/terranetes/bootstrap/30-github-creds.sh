#!/usr/bin/env bash
# Set up GitHub credentials for Terranetes.
#
# Two purposes:
#
# 1. GITHUB_TOKEN → azure-provider-creds (for the integrations/github Terraform provider)
#    The Provider injects all secret keys as env vars into the OpenTofu runner pod.
#    The github Terraform provider picks up GITHUB_TOKEN automatically.
#
# 2. GIT_PASSWORD → git-module-creds (a separate auth secret for cloning the private
#    Terraform module from GitHub). Terranetes source downloader uses GIT_PASSWORD
#    env var to authenticate git clone via token. Referenced in Revision spec.configuration.auth.
#
# Required PAT scopes: repo, delete_repo
#
# The token is NEVER written to disk or committed. Set it before the talk:
#   export GITHUB_TOKEN=ghp_...
#
# Prerequisites: 20-terranetes-azure-creds.sh must have run first.
set -euo pipefail

: "${GITHUB_TOKEN:?GITHUB_TOKEN must be set (PAT with repo + delete_repo scopes)}"

NAMESPACE="terranetes-system"

# 1. Patch GITHUB_TOKEN into the azure-provider-creds (for the TF github provider)
PROVIDER_SECRET="azure-provider-creds"
echo "==> Verifying '${PROVIDER_SECRET}' exists in namespace '${NAMESPACE}'"
kubectl -n "${NAMESPACE}" get secret "${PROVIDER_SECRET}" > /dev/null

echo "==> Patching GITHUB_TOKEN into '${NAMESPACE}/${PROVIDER_SECRET}'"
ENCODED=$(echo -n "${GITHUB_TOKEN}" | base64)
kubectl -n "${NAMESPACE}" patch secret "${PROVIDER_SECRET}" \
  --type=merge \
  -p "{\"data\":{\"GITHUB_TOKEN\":\"${ENCODED}\"}}"

# 2. Create git-module-creds secret for cloning the private module repo
MODULE_SECRET="git-module-creds"
echo "==> Creating/updating '${NAMESPACE}/${MODULE_SECRET}' (GIT_PASSWORD for module download)"
GIT_ENCODED=$(echo -n "${GITHUB_TOKEN}" | base64)
kubectl -n "${NAMESPACE}" apply -f - <<YAML
apiVersion: v1
kind: Secret
metadata:
  name: ${MODULE_SECRET}
  namespace: ${NAMESPACE}
type: Opaque
data:
  GIT_PASSWORD: ${GIT_ENCODED}
YAML

echo "==> Done."
echo "    azure-provider-creds: GITHUB_TOKEN injected (for Terraform github provider)"
echo "    git-module-creds: GIT_PASSWORD set (for private module repo clone)"
echo "    Next: run demos/terranetes/bootstrap/40-configure-providers.sh"
