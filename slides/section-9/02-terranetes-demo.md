# Slide 02 — Demo: Terranetes in Action

**Type:** Live demo — Configuration CR + policy approval + Terraform apply  
**Design:** Dark slide, terminal aesthetic, Configuration YAML + policy approval flow

---

## Key Message

The Configuration CR is the developer-facing surface. The policy gate is the platform team's control point. Terraform runs in the background — the developer never needs to run `terraform apply` directly, and the platform team can require approval before any apply happens.

---

## Demo Script

**Setup:** AKS cluster with Terranetes controller installed, Azure credentials configured, policy set to require approval for first-time applies.

**What to show:**
1. Show the `Configuration` CR — points to a Terraform module in Git, with variable values
2. Apply it: `kubectl apply -f demos/terranetes/storage-config.yaml`
3. Show the policy gate kicking in — resource is in `Pending` state waiting for approval
4. Approve it: `kubectl annotate configuration storage-config "terranetes.appvia.io/policy"=approve`
5. Watch the Terraform job run — show the pod spinning up, logs running
6. Show the resulting Azure resource and the Kubernetes status/outputs

**Key commands:**
```bash
kubectl apply -f demos/terranetes/storage-config.yaml
kubectl get configuration -w
kubectl describe configuration storage-config
kubectl annotate configuration storage-config "terranetes.appvia.io/policy"=approve
kubectl logs -l terraform.appvia.io/configuration=storage-config
```

---

## Talking Points

"Here's the Configuration CR. It says: use this Terraform module from this Git repo, with these variables. That's it."

"Apply it. Notice it doesn't run immediately — it's waiting for policy approval. This is configurable; you can auto-approve trusted modules, require approval for anything touching production, or gate on specific resource types."

"I approve it. Now watch the job spin up — this is literally running Terraform inside a Kubernetes pod. Standard Terraform, standard provider, standard module."

"A few moments later — the Azure resource exists. And in Kubernetes, I can see the status, the outputs, and any secrets that were injected."

"The Terraform team didn't have to change anything. Their module is unchanged. They just got a Kubernetes control plane wrapped around it."

---

## Transition

→ Next: Terranetes takeaway
