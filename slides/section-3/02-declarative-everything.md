# Slide 02 — Declarative Everything

**Type:** Concept — intent vs. imperative
**Design:** Light slide, two-line impact heading, watermark "INTENT"

---

## Key Message

Declarative means you describe the desired state and let controllers converge to it. Imperative means you write the steps to get there. At platform scale, only declarative survives.

---

## Talking Points

"There's a word that gets used so often in the cloud native world that it loses its meaning: declarative. Let me try to make it concrete."

"Imperative is: 'create this VM, then install this package, then write this config file, then restart this service, then check it's healthy.' You write the steps. If a step fails, you debug a runbook. If you run it twice, you might break things. If reality drifts from what you ran, you don't know unless you check."

"Declarative is different. You write down what should be true: 'there should be a database of this size, in this region, with this backup policy.' You hand that to a controller. The controller figures out the steps. It checks reality. It fixes drift. You never tell it *how* — only *what*."

"This sounds like a small distinction. It isn't. It changes the operational model completely. Your Git repo becomes the description of your system. Reviewing a pull request becomes reviewing the next state of production. Rolling back becomes reverting a commit."

"And the controller does the boring, error-prone work — over and over, in a loop, forever. That's where the reliability comes from."

"This is the principle that everything in cloud native is built on. Kubernetes resources, Argo CD applications, ASO Azure resources, Crossplane compositions — all of them are 'describe what you want, the controller converges.' Once you internalise that, the rest of the toolkit makes sense."

---

## Transition

→ Next: That toolkit — the CNCF ecosystem
