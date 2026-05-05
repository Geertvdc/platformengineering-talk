#!/usr/bin/env bash
# Install Crossplane into the platformeng-demo kind cluster.
# Pinned to a specific chart version for reproducibility on stage.
#
# Run BEFORE the talk. Not part of the live demo.
# See demos/crossplane/bootstrap/install-crossplane.md for full context.
set -euo pipefail

CROSSPLANE_VERSION="${CROSSPLANE_VERSION:-2.2.1}"
NAMESPACE="crossplane-system"

echo "==> Adding Crossplane Helm repo"
helm repo add crossplane-stable https://charts.crossplane.io/stable
helm repo update

echo "==> Installing Crossplane ${CROSSPLANE_VERSION} into namespace '${NAMESPACE}'"
helm upgrade --install crossplane crossplane-stable/crossplane \
  --namespace "${NAMESPACE}" \
  --create-namespace \
  --version "${CROSSPLANE_VERSION}" \
  --wait

echo "==> Crossplane pods:"
kubectl -n "${NAMESPACE}" get pods

echo
echo "==> Done. Next step: run demos/crossplane/bootstrap/20-crossplane-azure-creds.sh"
