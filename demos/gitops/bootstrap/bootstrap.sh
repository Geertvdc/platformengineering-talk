#!/usr/bin/env bash
# Single-command bootstrap for the GitOps demo (and every later demo).
# Runs cluster create, Argo CD install, and (if Azure SP env vars are set)
# the shared azure-creds Secret.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "${SCRIPT_DIR}/00-create-cluster.sh"
bash "${SCRIPT_DIR}/10-install-argocd.sh"

if [[ -n "${AZURE_TENANT_ID:-}" && -n "${AZURE_SUBSCRIPTION_ID:-}" \
   && -n "${AZURE_CLIENT_ID:-}" && -n "${AZURE_CLIENT_SECRET:-}" ]]; then
  bash "${SCRIPT_DIR}/30-azure-creds.sh"
else
  echo "==> Skipping azure-creds (AZURE_* env vars not all set)."
  echo "    Run bootstrap/30-azure-creds.sh later, before demos #2-#5."
fi

echo
echo "Bootstrap complete."
