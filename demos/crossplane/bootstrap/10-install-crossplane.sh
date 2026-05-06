#!/usr/bin/env bash
# Wait for Crossplane to be installed by Argo CD.
#
# Crossplane is now managed GitOps-style via:
#   demos/gitops/apps/crossplane-install.yaml
#
# Argo CD installs Crossplane from the Helm chart automatically once the
# app-of-apps syncs. This script just blocks until the rollout is healthy
# so that subsequent bootstrap steps (provider creds, 40-install-providers.sh)
# don't race ahead before the Crossplane CRDs are registered.
#
# To change the Crossplane version: edit targetRevision in crossplane-install.yaml.
# Run BEFORE the talk. Not part of the live demo.
set -euo pipefail

NAMESPACE="crossplane-system"

echo "==> Waiting for Argo CD to sync the Crossplane Helm Application..."
kubectl -n argocd wait application/crossplane \
  --for=jsonpath='{.status.health.status}'=Healthy \
  --timeout=5m

echo "==> Waiting for Crossplane pods to be ready"
kubectl rollout status -n "${NAMESPACE}" deploy/crossplane --timeout=3m
kubectl rollout status -n "${NAMESPACE}" deploy/crossplane-rbac-manager --timeout=3m

echo "==> Crossplane pods:"
kubectl -n "${NAMESPACE}" get pods

echo
echo "==> Done. Next step: run demos/crossplane/bootstrap/20-crossplane-azure-creds.sh"
