#!/usr/bin/env bash
# Install Terranetes controller via Helm and wait for it to be ready.
#
# Run BEFORE the talk. Not part of the live demo.
set -euo pipefail

NAMESPACE="terranetes-system"
TERRANETES_VERSION="0.8.0"

echo "==> Adding Terranetes Helm repo"
helm repo add appvia https://terranetes-controller.appvia.io
helm repo update

echo "==> Installing Terranetes controller ${TERRANETES_VERSION}"
helm upgrade --install terranetes-controller appvia/terranetes-controller \
  --namespace "${NAMESPACE}" \
  --create-namespace \
  --version "${TERRANETES_VERSION}" \
  --wait

echo "==> Waiting for Terranetes controller to be ready"
kubectl rollout status -n "${NAMESPACE}" deploy/terranetes-controller --timeout=3m

echo "==> Terranetes pods:"
kubectl -n "${NAMESPACE}" get pods

echo
echo "==> Verifying Terranetes CRDs are installed"
kubectl get crd | grep terraform.appvia.io

echo
echo "==> Done. Next step: run demos/terranetes/bootstrap/20-terranetes-azure-creds.sh"
