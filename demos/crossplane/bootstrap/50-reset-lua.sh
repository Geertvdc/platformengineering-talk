#!/usr/bin/env bash
# Reset argocd-cm to the minimal XRD-only Lua health check.
#
# Use this between rehearsals to restore the "before" state so you can repeat
# the Part D reveal (applying argocd-cm-crossplane-health.yaml live on stage).
#
# What this does:
#   1. Overwrites argocd-cm with the minimal bootstrap version (XRD + claim
#      health checks only — no Provider/ResourceGroup/Account/Repository checks)
#   2. Restarts argocd-repo-server so the change takes effect immediately
#
# After running this, all Crossplane managed resources will show as Healthy in
# Argo CD the moment YAML is applied — which is the "before" state you want to
# contrast with the full health checks.
#
# To apply the full health checks again (the reveal):
#   kubectl apply -f demos/crossplane/bootstrap/argocd-cm-crossplane-health.yaml
#   kubectl rollout restart -n argocd deploy/argocd-repo-server
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PATCH_FILE="${SCRIPT_DIR}/../../gitops/bootstrap/argocd-cm-patch.yaml"

echo "==> Resetting argocd-cm to minimal Lua health check (XRD + claims only)"
kubectl apply -f "${PATCH_FILE}"

echo "==> Restarting argocd-repo-server to pick up the change"
kubectl rollout restart -n argocd deploy/argocd-repo-server
kubectl rollout status -n argocd deploy/argocd-repo-server --timeout=2m

echo
echo "==> Done. argocd-cm is back to the minimal bootstrap state."
echo "    Argo CD will now show all managed resources as Healthy immediately."
echo
echo "    To apply the full health checks (Part D reveal):"
echo "      kubectl apply -f demos/crossplane/bootstrap/argocd-cm-crossplane-health.yaml"
echo "      kubectl rollout restart -n argocd deploy/argocd-repo-server"
