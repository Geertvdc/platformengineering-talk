# Architecture Diagram

> TODO: Create a visual diagram for Section 11 of the talk.

## What to show

```
┌─────────────────────────────────────────────────────┐
│                     Developer                        │
│         (simple CR or golden-path UI/CLI)            │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│                      Git                             │
│            (single source of truth)                  │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│                   Argo CD                            │
│         (GitOps delivery + reconciliation)           │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│              Kubernetes API (AKS)                    │
│                                                      │
│   ┌──────────┐  ┌────────────┐  ┌───────────────┐  │
│   │   ASO    │  │ Crossplane │  │      KRO      │  │
│   └────┬─────┘  └─────┬──────┘  └───────┬───────┘  │
│        │              │                  │           │
│        └──────────────┴──────────────────┘           │
│                        │                             │
│               ┌────────┴────────┐                    │
│               │   Terranetes    │                    │
│               │ (Terraform jobs)│                    │
│               └────────┬────────┘                    │
└────────────────────────┼─────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│                     Azure                            │
│   (databases, storage, managed services, identity)   │
└─────────────────────────────────────────────────────┘
```

## Touchpoints
- **Developer:** creates simple CRs or uses a golden-path UI/CLI
- **Platform team:** authors Compositions (Crossplane), ResourceGroups (KRO), Policies (Terranetes), ApplicationSets (Argo CD)
- **Everything flows through Git** → Argo CD watches and reconciles
- **Sovereignty:** the control plane API stays inside the Kubernetes cluster

## Notes for slide
- Emphasize: developer never talks directly to Azure
- Platform team sets the guardrails, developer gets self-service
- Closing message: self-service ✓  consistency ✓  clear boundaries ✓
