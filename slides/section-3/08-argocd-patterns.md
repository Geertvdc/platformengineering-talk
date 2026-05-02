# S3-08 — Argo CD Patterns

**Type:** Architecture Diagram (light)
**Design:** Light slide with two-column layout. Left: App of Apps tree (ROOT-APP orchestrating INFRA-APP, PLATFORM-APP, APPS-APP). Right: ApplicationSets fan-out (one APPSET TEMPLATE generating dev-cluster, staging-cluster, prod-cluster instances). Bottom dark strip: drift detection callout.
**Key Message:** Argo CD scales through two patterns — App of Apps for hierarchy and ApplicationSets for templated multi-cluster/multi-env deployment.

---

## Talking Points

- Once you have GitOps working, the next question is: how do you structure Argo CD itself for a real platform?
- **App of Apps**: one root Application manages all other Applications. You commit the root-app to Git once — from then on, adding a new app is just adding a manifest to the repo. The platform team owns the root; product teams own their app manifests.
- **ApplicationSets**: a single template that generates multiple Application objects based on a generator (cluster list, Git directory, pull request, etc.). One template → N environments. Change the template, all environments update.
- These two patterns together give you a GitOps-native way to manage hundreds of clusters and environments without writing custom automation.
- **Drift detection** is built-in: Argo CD continuously compares desired state (Git) to live state (cluster). If they diverge, it alerts — and by default, reconciles within seconds.
- This is what "self-healing infrastructure" actually means in practice. Not magic. Just a tight reconciliation loop.

---

## Transition

AKS is where all of this runs — but it's just the substrate. Let's talk about what that means for a platform team.

→ See S3-06 (AKS as the Substrate) for context on Azure
