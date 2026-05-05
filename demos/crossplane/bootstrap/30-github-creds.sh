#!/usr/bin/env bash
# Create the GitHub provider credentials Secret from a Personal Access Token.
#
# Reads from: GITHUB_TOKEN environment variable (already set for Argo CD
# repo registration in demos/gitops/bootstrap/15-add-github-repo.sh).
# Writes to:  crossplane-system/github-provider-creds  (key: token)
#
# Required PAT scopes:
#   repo, read:org, delete_repo
#
# The token is NEVER written to disk or committed. Set it before the talk:
#   export GITHUB_TOKEN=ghp_...
set -euo pipefail

: "${GITHUB_TOKEN:?GITHUB_TOKEN must be set (PAT with repo + read:org + delete_repo scopes)}"

DST_NAMESPACE="crossplane-system"
DST_SECRET="github-provider-creds"

echo "==> Ensuring namespace '${DST_NAMESPACE}' exists"
kubectl create namespace "${DST_NAMESPACE}" --dry-run=client -o yaml | kubectl apply -f -

echo "==> Creating/updating Secret '${DST_SECRET}' in namespace '${DST_NAMESPACE}'"
kubectl -n "${DST_NAMESPACE}" create secret generic "${DST_SECRET}" \
  --from-literal=token="${GITHUB_TOKEN}" \
  --dry-run=client -o yaml | kubectl apply -f -

echo "==> Done. Argo CD will now reconcile the GitHub ProviderConfig against this Secret."
