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

echo "==> Patching argocd-cm: custom health checks for Crossplane XRDs"
# Argo CD needs to know that a CompositeResourceDefinition is only 'Healthy'
# once Crossplane has finished establishing it (i.e. the AppStorage / AppTeam
# CRDs are actually registered). Without this, Argo CD advances to the next
# sync-wave before the claim CRD exists and the sync fails with:
#   "The Kubernetes API could not find platform.demo.io/AppStorage"
kubectl -n "${ARGOCD_NAMESPACE}" patch configmap argocd-cm --type merge -p '
data:
  resource.customizations.health.apiextensions.crossplane.io_CompositeResourceDefinition: |
    hs = {}
    hs.status = "Progressing"
    hs.message = "Waiting for XRD to be established and offered"
    if obj.status ~= nil and obj.status.conditions ~= nil then
      local established = false
      local offered = false
      for _, c in ipairs(obj.status.conditions) do
        if c.type == "Established" and c.status == "True" then
          established = true
        end
        if c.type == "Offered" and c.status == "True" then
          offered = true
        end
      end
      if established and offered then
        hs.status = "Healthy"
        hs.message = "XRD is established and offered"
      end
    end
    return hs
'

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
