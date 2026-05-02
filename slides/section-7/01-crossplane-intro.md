# Slide 01 — Demo: Crossplane — Build Your Own Platform API

**Type:** Demo intro — what Crossplane is and the problem it solves  
**Design:** Dark slide, large "CROSSPLANE." heading, subtitle "YOU DESIGN THE API."

---

## Key Message

Crossplane lets the platform team define the API that developers use — without exposing any cloud-provider details. Developers create simple custom resources; Crossplane Compositions handle all the complexity behind the scenes. The platform team owns the abstraction.

---

## Talking Points

"ASO gives you direct control. Crossplane gives you *designed* control."

"Here's the difference. With ASO, a developer writes a Kubernetes manifest that looks like an Azure resource. They need to know what a storage account SKU is, what a resource group is, what location to pick. That's fine if they're Azure engineers."

"But what if you want to give developers a completely cloud-agnostic experience? What if you want to say: 'you don't need to know anything about Azure — you just say you need a database, and the platform figures out the rest'?"

"That's what Crossplane does. The platform team writes a Composition — a detailed template that encodes every platform opinion: naming conventions, networking setup, backup policies, tagging standards. All of it hidden from the developer."

"The developer sees only what you want them to see. They create an `AppDatabase` resource. One field: the name. Maybe a size. That's it. Crossplane does the rest."

"This is the IDP dream — a platform API that your developers can use without becoming infrastructure engineers."

---

## Transition

→ Next: Demo — developer creates AppDatabase, Crossplane provisions Azure PostgreSQL
