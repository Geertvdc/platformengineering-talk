#!/usr/bin/env bash
# Create the GitHub provider credentials Secret from a Personal Access Token.
#
# Reads from: GITHUB_TOKEN and GITHUB_OWNER environment variables.
# Writes to:  crossplane-system/github-provider-creds  (key: credentials)
#
# The new provider-upjet-github (v0.19+) expects a JSON blob with both
# "token" and "owner" fields under the key "credentials".
#
# Required PAT scopes:
#   repo, read:org, delete_repo
#
# The token is NEVER written to disk or committed. Set it before the talk:
#   export GITHUB_TOKEN=ghp_...
#   export GITHUB_OWNER=Geertvdc   # your GitHub username or org
set -euo pipefail

: "${GITHUB_TOKEN:?GITHUB_TOKEN must be set (PAT with repo + read:org + delete_repo scopes)}"
: "${GITHUB_OWNER:?GITHUB_OWNER must be set (your GitHub username or org, e.g. Geertvdc)}"

DST_NAMESPACE="crossplane-system"
DST_SECRET="github-provider-creds"

CREDS=$(cat <<EOF
{"token":"${GITHUB_TOKEN}","owner":"${GITHUB_OWNER}"}
EOF
)

echo "==> Ensuring namespace '${DST_NAMESPACE}' exists"
kubectl create namespace "${DST_NAMESPACE}" --dry-run=client -o yaml | kubectl apply -f -

echo "==> Creating/updating Secret '${DST_SECRET}' in namespace '${DST_NAMESPACE}'"
kubectl -n "${DST_NAMESPACE}" create secret generic "${DST_SECRET}" \
  --from-literal=credentials="${CREDS}" \
  --dry-run=client -o yaml | kubectl apply -f -

echo "==> Done. Argo CD will now reconcile the GitHub ProviderConfig against this Secret."
