#!/usr/bin/env bash
# Set up GitHub credentials for Terranetes.
#
# Two purposes:
#
# 1. GITHUB_TOKEN → azure-provider-creds (for the integrations/github Terraform provider)
#    The Provider injects all secret keys as env vars into the OpenTofu runner pod.
#    The github Terraform provider picks up GITHUB_TOKEN automatically.
#
# 2. GIT_PASSWORD → git-module-creds (for cloning the private Terraform module from GitHub)
#    Terranetes source downloader uses GIT_PASSWORD env var for git HTTPS auth.
#    Must exist in the CloudResource namespace (terranetes-demo), referenced by
#    spec.configuration.auth in the Revision.
#
# Required PAT scopes: repo, delete_repo
#
# The token is NEVER written to disk or committed. Set it before the talk:
#   export GITHUB_TOKEN=ghp_...
#
# Prerequisites: 20-terranetes-azure-creds.sh must have run first.
set -euo pipefail

: "${GITHUB_TOKEN:?GITHUB_TOKEN must be set (PAT with repo + delete_repo scopes)}"

ENCODED=$(echo -n "${GITHUB_TOKEN}" | base64)

# 1. Patch GITHUB_TOKEN into azure-provider-creds (for the TF github provider)
echo "==> Patching GITHUB_TOKEN into terranetes-system/azure-provider-creds"
kubectl -n terranetes-system get secret azure-provider-creds > /dev/null
kubectl -n terranetes-system patch secret azure-provider-creds \
  --type=merge \
  -p "{\"data\":{\"GITHUB_TOKEN\":\"${ENCODED}\"}}"

# 2. Create git-module-creds in terranetes-demo (CloudResource namespace)
echo "==> Creating terranetes-demo/git-module-creds (GIT_PASSWORD for module download)"
kubectl create namespace terranetes-demo --dry-run=client -o yaml | kubectl apply -f -
kubectl -n terranetes-demo apply -f - <<YAML
apiVersion: v1
kind: Secret
metadata:
  name: git-module-creds
  namespace: terranetes-demo
type: Opaque
data:
  GIT_USERNAME: $(echo -n "x-access-token" | base64)
  GIT_PASSWORD: ${ENCODED}
YAML

echo "==> Done."
echo "    azure-provider-creds: GITHUB_TOKEN injected (for Terraform github provider)"
echo "    terranetes-demo/git-module-creds: GIT_PASSWORD set (for private module repo clone)"
echo "    Next: run demos/terranetes/bootstrap/40-configure-providers.sh"
