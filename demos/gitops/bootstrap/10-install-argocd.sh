#!/usr/bin/env bash
# Install Argo CD into the kind cluster and apply the App-of-Apps root.
# Pinned to a stable Argo CD release so the demo is reproducible on stage.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARGOCD_NAMESPACE="argocd"
ARGOCD_VERSION="${ARGOCD_VERSION:-v2.13.1}"

echo "==> Creating namespace '${ARGOCD_NAMESPACE}'"
kubectl create namespace "${ARGOCD_NAMESPACE}" --dry-run=client -o yaml | kubectl apply -f -

echo "==> Installing Argo CD ${ARGOCD_VERSION}"
kubectl apply -n "${ARGOCD_NAMESPACE}" \
  -f "https://raw.githubusercontent.com/argoproj/argo-cd/${ARGOCD_VERSION}/manifests/install.yaml"

echo "==> Waiting for Argo CD server to become ready (this can take a minute on first install)"
kubectl rollout status -n "${ARGOCD_NAMESPACE}" deploy/argocd-server --timeout=5m
kubectl rollout status -n "${ARGOCD_NAMESPACE}" deploy/argocd-repo-server --timeout=5m

echo "==> Applying App-of-Apps root Application"
kubectl apply -f "${SCRIPT_DIR}/20-apply-root-app.yaml"

cat <<EOF

Argo CD is installed.

Get the initial admin password:
  kubectl -n ${ARGOCD_NAMESPACE} get secret argocd-initial-admin-secret \\
    -o jsonpath='{.data.password}' | base64 -d && echo

Port-forward the UI in a separate terminal:
  kubectl -n ${ARGOCD_NAMESPACE} port-forward svc/argocd-server 8080:443

Then open https://localhost:8080 (user: admin).
EOF
