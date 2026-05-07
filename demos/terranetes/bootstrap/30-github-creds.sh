#!/usr/bin/env bash
# Create the GitHub credentials Secret for use inside Terranetes OpenTofu runs.
#
# Reads from: GITHUB_TOKEN environment variable.
# Writes to:  terranetes-system/github-provider-creds  (GITHUB_TOKEN key)
#
# Terranetes injects this into the OpenTofu runner pod as an env var.
# The integrations/github Terraform provider picks it up automatically.
#
# Required PAT scopes:
#   repo, delete_repo
#
# The token is NEVER written to disk or committed. Set it before the talk:
#   export GITHUB_TOKEN=ghp_...
set -euo pipefail

: "${GITHUB_TOKEN:?GITHUB_TOKEN must be set (PAT with repo + delete_repo scopes)}"

DST_NAMESPACE="terranetes-system"
DST_SECRET="github-provider-creds"

echo "==> Ensuring namespace '${DST_NAMESPACE}' exists"
kubectl create namespace "${DST_NAMESPACE}" --dry-run=client -o yaml | kubectl apply -f -

echo "==> Creating/updating Secret '${DST_SECRET}' in namespace '${DST_NAMESPACE}'"
kubectl -n "${DST_NAMESPACE}" create secret generic "${DST_SECRET}" \
  --from-literal=GITHUB_TOKEN="${GITHUB_TOKEN}" \
  --dry-run=client -o yaml | kubectl apply -f -

echo "==> Done. Next step: run demos/terranetes/bootstrap/40-configure-providers.sh"
