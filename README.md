# Cloud native platform engineering on Azure

## Abstract

Cloud native platform engineering starts with Kubernetes and the CNCF ecosystem, but it also needs to take sovereignty and control into account. In this session we look at how to design a platform around cloud native principles while working in Azure. The focus is on choosing the right tools for the right problem and bringing them together into a platform that enables self service, consistency, and clear boundaries.

Geert will demo several tools from the cloud native ecosystem, including GitOps approaches, Argo CD, Crossplane, and Terranetes, and explain when to use each of them. The session also discusses how sovereignty requirements and AI driven development influence platform design decisions. The result is a clearer understanding of how to combine Azure and cloud native tools into a practical platform architecture.

---

## Repo structure

```
slides/          # Slide content and speaker notes
demos/           # Demo scripts and manifests per tool/topic
  gitops/        # GitOps with Argo CD
  crossplane/    # Crossplane resource compositions
  terranetes/    # Terranetes controller demos
docs/            # Supporting notes, research, references
assets/          # Images, diagrams, logos
```

## Topics covered

- Cloud native platform design principles
- GitOps with Argo CD
- Infrastructure as code with Crossplane
- Terraform-based provisioning with Terranetes
- Sovereignty, control, and compliance
- AI-driven development and platform design
- Self-service, consistency, and clear boundaries
