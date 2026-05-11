# Stage Runbook

## Argo CD UI (open before going on stage)

```bash
kubectl -n argocd port-forward svc/argocd-server 8080:443 &
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath='{.data.password}' | base64 -d && echo
```

https://localhost:8080 — user: `admin`

---

## DEMO 1 — GitOps

```bash
kubectl -n gitops-demo edit deploy/demo-nginx
# change replicas: 2 → 5, save
```

Switch to Argo CD UI → `gitops-demo` goes OutOfSync (red) → auto-heals back to 2 in <30s.

---

## DEMO 2 — ASO

```bash
git add demos/aso/samples/storageaccount.yaml
git commit -m "demo: add storage account"
git push

kubectl get storageaccount -n aso-demo -w
```

Open Azure Portal → confirm Storage Account exists.

---

## DEMO 3 — Crossplane

```bash
# Providers + XRDs
kubectl get providers.pkg.crossplane.io
kubectl get xrd

# AppStorage — show the abstraction
cat demos/crossplane/samples/appstorage/appstorage.yaml
cat demos/crossplane/composition/appstorage/composition-appstorage.yaml
kubectl -n crossplane-appstorage-demo get appstorage
kubectl get account

# AppTeam — multi-cloud
cat demos/crossplane/samples/appteam/appteam.yaml
cat demos/crossplane/composition/appteam/composition-appteam.yaml
kubectl -n crossplane-appteam-demo get appteam techorama-team
kubectl get resourcegroup,account
kubectl get repository.repo.github.upbound.io

# Lua health check reveal — show Argo CD UI first (all green, no real state)
kubectl apply -f demos/crossplane/bootstrap/argocd-cm-crossplane-health.yaml
kubectl rollout restart -n argocd deploy/argocd-repo-server
# UI updates: yellow (Progressing) → green (Healthy)
kubectl -n crossplane-appteam-demo get appteam techorama-team -w
```

---

## DEMO 4 — KRO

```bash
# Show the platform blueprint and the 3-field developer interface
cat demos/kro/composition/rgd-myapp.yaml
cat demos/kro/samples/myapp.yaml.dontdeployyet

# Trigger
git mv demos/kro/samples/myapp.yaml.dontdeployyet demos/kro/samples/myapp.yaml
git commit -m "demo: deploy myapp"
git push

# Watch
kubectl get namespace myapp
kubectl get rolebinding -n myapp
kubectl get storageaccount -n myapp -w
```

Open Azure Portal → Storage Accounts → filter `kro-demo-rg`.

---

## DEMO 5 — Terranetes

```bash
# Show it's just Terraform
kubectl get providers.terraform.appvia.io
cat demos/terranetes/module/main.tf

# Show the running job
kubectl get cloudresource -n terranetes-demo
kubectl get jobs -n terranetes-system
kubectl logs -n terranetes-system \
  -l terraform.appvia.io/configuration=techorama-team-fth7r --tail=100 -f

# Verify results
az group show --name rg-techorama-demo-dev --query name -o tsv
gh repo view Geertvdc/techorama-demo-platform-infra
kubectl get secret techorama-team-outputs -n terranetes-demo -o yaml
```
