# Slide Outline

## 1. The chaos before the platform (~7 min)
- Opening scenario: new team joins the org — what do they need and how long does it take?
- The "ticket to the platform team" anti-pattern
- The snowflake problem: every team's infra looks different
- Multiple clouds, multiple tools, multiple teams → inconsistency compounds
- Platform team as perpetual bottleneck
- **Closing beat:** what if the platform team's job was to make themselves unnecessary?

## 2. Platform engineering as an answer (~4 min)
- Platform engineering ≠ ops team doing tickets
- The Internal Developer Platform (IDP) — a product your developers consume
- The golden path: opinionated but not mandatory
- Key outcomes: self-service, consistency, clear boundaries
- CNCF definition and ecosystem

## 3. Cloud native + GitOps as the foundation (~5 min)
- Why Kubernetes: the API, the reconciliation loop, the extension model
- Declarative everything: describe intent, let controllers converge
- The CNCF ecosystem as a toolkit, not a single product
- GitOps: Git as single source of truth — auditability, rollback, self-healing
- Argo CD: App of Apps, ApplicationSets, drift detection
- **BRIEF DEMO (~2 min):** Argo CD drift detection and self-healing
- Azure as the cloud layer: AKS is where the platform runs, but not where it stops

## 4. Designing for real-world complexity (~4 min)
- Reality: multiple teams, multiple cloud accounts, multiple tools, existing investments
- Challenge: self-service + consistency + guardrails across all of it
- Sovereignty is one dimension: data residency, compliance, control inside your cluster API
- But also: existing Terraform, Azure managed services, team skills, budget
- The platform must be a flexible control plane, not a rigid single-tool mandate
- **Framing:** we'll look at four tools — each solving a different angle of this problem

## 5. Decision framework: which tool for which problem (~4 min)

| Tool | Best for | Azure native? | Abstraction level |
|------|----------|---------------|-------------------|
| **ASO** | Direct Azure resources as K8s CRDs | ✅ | Low — maps 1:1 to Azure APIs |
| **Crossplane** | Building your own platform API (XRDs) | Partial | High — you design the abstraction |
| **KRO** | Composing multiple K8s resources into one "app concept" CR | ✅ (with ASO) | Medium — compose, don't abstract |
| **Terranetes** | Running existing Terraform under Kubernetes control | ✅ | Medium — wraps what you have |

- GitOps (Argo CD) sits underneath all of these — it's the delivery layer, not a provisioning tool
- These are NOT mutually exclusive — real platforms combine them

## 6. Demo: ASO — Azure resources as Kubernetes CRDs (~5 min)
- ASO maintained by Microsoft — maps Azure ARM concepts directly to CRDs
- Apply YAML → Azure resource appears. Delete YAML → resource deleted.
- Great for Azure-first teams who want GitOps control
- **DEMO:** Create an Azure Storage Account or PostgreSQL via Kubernetes manifest
- Takeaway: lowest friction on-ramp for Azure-native teams

## 7. Demo: Crossplane — build your own platform API (~5 min)
- Crossplane extends the Kubernetes API with custom resource types (XRDs + Compositions)
- Platform team writes the Composition; developer only sees a simple CR
- Encode platform opinions: naming, network, backup, tagging
- Multi-cloud capable
- **DEMO:** Developer creates `AppDatabase` CR → Composition provisions Azure PostgreSQL with platform standards
- Takeaway: Crossplane is for when you want to own your abstraction layer

## 8. Demo: KRO — compose multi-resource app concepts (~5 min)
- KRO lets you define a ResourceGroup: a bundle of K8s resources as one CR
- Pairs naturally with ASO: one CR → namespace + RBAC + ASO database + secret
- Lower complexity than Crossplane XRDs for scenarios staying within Kubernetes/Azure
- **DEMO:** Single KRO ResourceGroup CR provisions namespace + managed identity + ASO database
- Takeaway: KRO is the glue for app-level self-service without a full IDP engine

## 9. Demo: Terranetes — Terraform under Kubernetes control (~5 min)
- Most orgs have years of Terraform modules — you don't throw them away
- Terranetes runs Terraform/OpenTofu inside Kubernetes as controller-managed jobs
- Policy gates: require approval before Terraform applies
- Git-native: state and config tracked like any Kubernetes resource
- **DEMO:** Terranetes `Configuration` CR → existing Terraform module → Azure resources + policy approval
- Takeaway: meets teams where they are, brings infra under platform control

## 10. Sovereignty, AI, and platform design (~3 min)
- All four tools keep the control plane inside your Kubernetes API — you own the state and audit trail
- Compliance and data residency become easier when the platform API is the single entry point
- AI-driven development increases the velocity of infra requests — platforms need guardrails, not manual approval for everything
- AI also helps write Compositions, ResourceGroups, and ApplicationSets

## 11. The whole picture (~3 min)
- Architecture diagram: Git → Argo CD → Kubernetes API → ASO / Crossplane / KRO / Terranetes → Azure
- Developer touchpoints: simple CRs or golden-path UI
- Platform team touchpoints: Compositions, Policies, ApplicationSets
- Self-service, consistency, clear boundaries — delivered
- **Closing beat:** the platform team's job isn't to say no. It's to make yes safe.

---

## Demo issues (tracked separately)
- [#1 Demo: Argo CD](https://github.com/Geertvdc/platformengineering-talk/issues/1)
- [#2 Demo: ASO](https://github.com/Geertvdc/platformengineering-talk/issues/2)
- [#3 Demo: Crossplane](https://github.com/Geertvdc/platformengineering-talk/issues/3)
- [#4 Demo: KRO](https://github.com/Geertvdc/platformengineering-talk/issues/4)
- [#5 Demo: Terranetes](https://github.com/Geertvdc/platformengineering-talk/issues/5)
