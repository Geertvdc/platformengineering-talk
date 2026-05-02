# Slide 05 — Argo CD

**Type:** Tool — the GitOps engine in practice
**Design:** Dark slide, "ARGO CD." impact heading, three-pattern strip, demo callout, watermark "ARGO"

---

## Key Message

Argo CD turns GitOps principles into a working delivery system. Three patterns matter for platforms: App of Apps, ApplicationSets, and drift detection with self-healing.

---

## Talking Points

"Argo CD is the workhorse. It runs in the cluster, watches your Git repos, applies the manifests it finds there, and watches for drift. It is the GitOps agent we just talked about — and it's become the de-facto standard for a reason."

"Three patterns matter for platforms."

"*App of Apps.* You describe one Argo CD Application that points at a directory of Applications. That bootstraps your whole platform from a single root. One commit, the cluster wires itself up. New cluster spins up empty? Point Argo at the root, walk away."

"*ApplicationSets.* When you have many tenants — many teams, many environments, many clusters — you don't want to write an Application by hand for each one. ApplicationSets generate them from a template plus a list. Add a team to a config file, their environment shows up. Remove them, it's gone."

"*Drift detection and self-healing.* Argo continuously compares Git to the cluster. If they diverge — a manual `kubectl edit`, a half-finished hotfix, a controller-induced change — Argo flags it, and if you let it, fixes it back to what Git says. Production becomes Git, all the time."

"This is what we'll demo in a moment. We'll change something in the cluster directly, watch Argo notice, and watch it heal. It's a small demo but it captures the whole point of GitOps in 90 seconds."

> Demo wiring lives in [#1](https://github.com/Geertvdc/platformengineering-talk/issues/1) — a brief Argo CD drift / self-healing segment, ~2 minutes.

---

## Transition

→ Next: Where all this runs — Azure as the cloud layer
