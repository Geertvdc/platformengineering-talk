# S3-07 — How GitOps Works

**Type:** Architecture Diagram (dark)
**Design:** Dark slide with pull-loop flow diagram: DEVELOPER → GIT REPO ← ARGO CD → KUBERNETES CLUSTER. Argo CD box is highlighted in white to show it as the active agent. Step labels (1 git push, 2 argo pulls, 3 apply). Drift detection annotation. Three bottom insight panels.
**Key Message:** GitOps is a pull-based model. The cluster never gets pushed to — Argo CD watches Git and reconciles continuously.

---

## Talking Points

- Traditional CI/CD pushes to clusters — that means storing cluster credentials in your pipeline and hoping the push succeeds.
- GitOps flips the model: **Git is the source of truth, and the cluster pulls toward it.**
- Step 1: Developer opens a PR and merges to main. That's it for the developer.
- Step 2: Argo CD is watching the Git repo. It detects the new commit and computes the diff.
- Step 3: Argo CD applies the change to the cluster — only the delta, only what changed.
- No push credentials in CI. No imperative scripts. No "who deployed what at 3am?"
- **Drift detection**: if someone `kubectl apply`s something directly, Argo CD sees the divergence and reconciles back to Git. Always converging.
- The key insight: the cluster is always trying to be what Git says it should be.

---

## Transition

So that's the mechanism. Now let's look at how you actually structure your Argo CD setup at scale — App of Apps and ApplicationSets.

→ See S3-08 (Argo CD Patterns)
