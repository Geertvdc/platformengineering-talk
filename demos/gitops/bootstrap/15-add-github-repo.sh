#!/usr/bin/env bash
# Register the GitHub repository with Argo CD so it can clone private repos.
#
# Reads credentials from environment variables – never commit real values.
# Add to your bootstrap/.env (which is gitignored):
#
#   export GITHUB_TOKEN=ghp_...
#   export GITHUB_USER=<your-github-username>   # optional, defaults to 'git'
#
# The token needs at minimum read access to the repository contents.
set -euo pipefail

REPO_URL="https://github.com/Geertvdc/platformengineering-talk"
ARGOCD_NAMESPACE="argocd"

: "${GITHUB_TOKEN:?GITHUB_TOKEN must be set (a GitHub PAT with repo read access)}"
GITHUB_USER="${GITHUB_USER:-git}"

echo "==> Registering GitHub repo with Argo CD"
kubectl create secret generic argocd-repo-platformengineering-talk \
  --namespace "${ARGOCD_NAMESPACE}" \
  --from-literal=type=git \
  --from-literal=url="${REPO_URL}" \
  --from-literal=username="${GITHUB_USER}" \
  --from-literal=password="${GITHUB_TOKEN}" \
  --dry-run=client -o yaml \
| kubectl label --local -f - \
    "argocd.argoproj.io/secret-type=repository" \
    --dry-run=client -o yaml \
| kubectl apply -f -

echo "==> GitHub repo registered."
