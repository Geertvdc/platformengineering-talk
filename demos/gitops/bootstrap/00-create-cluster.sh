#!/usr/bin/env bash
# Create the kind cluster used by every demo in the talk.
# Idempotent: re-running deletes and recreates the cluster.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLUSTER_NAME="platformeng-demo"

if kind get clusters 2>/dev/null | grep -qx "${CLUSTER_NAME}"; then
  echo "==> Existing kind cluster '${CLUSTER_NAME}' found, deleting for a clean slate"
  kind delete cluster --name "${CLUSTER_NAME}"
fi

echo "==> Creating kind cluster '${CLUSTER_NAME}'"
kind create cluster --config "${SCRIPT_DIR}/kind-config.yaml"

echo "==> Cluster ready:"
kubectl cluster-info --context "kind-${CLUSTER_NAME}"
