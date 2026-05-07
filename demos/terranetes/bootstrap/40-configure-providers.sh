#!/usr/bin/env bash
# Apply Terranetes Provider resources and wait for them to be ready.
#
# Prerequisites:
#   - Terranetes installed (10-install-terranetes.sh)
#   - azure-provider-creds Secret present (20-terranetes-azure-creds.sh)
#   - github-provider-creds Secret present (30-github-creds.sh)
#
# Run BEFORE the talk. Not part of the live demo.
set -euo pipefail

PROVIDER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../provider" && pwd)"
TIMEOUT="${PROVIDER_TIMEOUT:-3m}"

echo "==> Applying Terranetes Providers"
kubectl apply -f "${PROVIDER_DIR}/provider-azure.yaml"

echo "==> Waiting for azure provider to be ready (timeout: ${TIMEOUT})"
kubectl wait provider.terraform.appvia.io azure \
  --for=condition=Ready \
  --timeout="${TIMEOUT}"

echo "==> Provider status:"
kubectl get providers.terraform.appvia.io

echo
echo "==> Done. Argo CD can now sync Configurations without provider errors."
echo "    Next: verify with 'kubectl get providers.terraform.appvia.io'"
