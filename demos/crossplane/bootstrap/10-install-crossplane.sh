#!/usr/bin/env bash
# Install Crossplane via Helm and wait for it to be ready.
#
# Run BEFORE the talk. Not part of the live demo.
set -euo pipefail

NAMESPACE="crossplane-system"
CROSSPLANE_VERSION="2.2.1"

echo "==> Adding Crossplane Helm repo"
helm repo add crossplane-stable https://charts.crossplane.io/stable
helm repo update

echo "==> Installing Crossplane ${CROSSPLANE_VERSION}"
helm upgrade --install crossplane crossplane-stable/crossplane \
  --namespace "${NAMESPACE}" \
  --create-namespace \
  --version "${CROSSPLANE_VERSION}" \
  --wait

echo "==> Waiting for Crossplane pods to be ready"
kubectl rollout status -n "${NAMESPACE}" deploy/crossplane --timeout=3m
kubectl rollout status -n "${NAMESPACE}" deploy/crossplane-rbac-manager --timeout=3m

echo "==> Crossplane pods:"
kubectl -n "${NAMESPACE}" get pods

echo
echo "==> Done. Next step: run demos/crossplane/bootstrap/20-crossplane-azure-creds.sh"
