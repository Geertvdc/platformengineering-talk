#!/usr/bin/env bash
# Install Crossplane providers and wire credentials.
#
# Applies the three Provider packages and waits for each to become healthy
# before creating the ProviderConfigs. This ensures all Azure + GitHub CRDs
# are registered before Argo CD syncs the Compositions and claims.
#
# Prerequisites:
#   - Crossplane installed (10-install-crossplane.sh)
#   - azure-provider-creds Secret present (20-crossplane-azure-creds.sh)
#   - github-provider-creds Secret present (30-github-creds.sh)
#
# Run BEFORE the talk. Not part of the live demo.
set -euo pipefail

PROVIDER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/provider" && pwd)"
TIMEOUT="${PROVIDER_TIMEOUT:-5m}"

echo "==> Applying Crossplane Providers"
kubectl apply \
  -f "${PROVIDER_DIR}/provider-azure-resources.yaml" \
  -f "${PROVIDER_DIR}/provider-azure-storage.yaml" \
  -f "${PROVIDER_DIR}/provider-github.yaml"

echo "==> Waiting for Providers to become healthy (timeout: ${TIMEOUT})"
echo "    This pulls provider images — typically 2–3 minutes on first run."

for provider in \
  upbound-provider-azure-resources \
  upbound-provider-azure-storage \
  crossplane-contrib-provider-github; do
  echo "    Waiting for ${provider}..."
  kubectl wait provider "${provider}" \
    --for=condition=Healthy \
    --timeout="${TIMEOUT}"
done

echo "==> All Providers healthy. Applying ProviderConfigs"
kubectl apply \
  -f "${PROVIDER_DIR}/providerconfig.yaml" \
  -f "${PROVIDER_DIR}/providerconfig-github.yaml"

echo
echo "==> Done. Argo CD can now sync Compositions and claims without CRD errors."
echo "    Next: verify with 'kubectl get providers' and 'kubectl get providerconfig'"
