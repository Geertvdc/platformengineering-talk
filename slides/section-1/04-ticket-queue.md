# Slide 04 — The Ticket Queue

**Type:** Pain points, 3-column  
**Design:** White, "THE TICKET QUEUE." large type, 3 columns: SLOW / INCONSISTENT / BOTTLENECK

---

## Key Message

The ticket-based model for infrastructure work is the most common coping mechanism — and it creates three fundamental problems: it's slow, the results are inconsistent, and the platform team becomes a bottleneck for everyone else.

---

## Talking Points

"So you file a ticket."

"And the ticket queue is where developer velocity goes to die."

"Let's talk about what the ticket queue actually costs you."

"**Slow.** A namespace request takes 2 days. A database takes a week. A new environment takes two weeks. In the meantime your developer is blocked. They context-switch to something else. The original task loses momentum. And this happens dozens of times across your organisation, every single week."

"**Inconsistent.** Every ticket is handled by whoever picks it up. One person sets up the namespace one way, another person sets it up differently. The database config varies by who ran the Terraform. The pipeline template is slightly different because someone used an older version. Now you have 40 microservices with 40 slightly different setups."

"**Bottleneck.** The platform team, the SRE team, the ops team — they become the single point of failure for everyone else moving forward. They can't keep up. Developers are frustrated. The platform team is burning out. Nobody wins."

"The ticket queue isn't a process problem. It's a design problem. You're asking humans to do what a platform should do."

---

## Notes

- The three columns are the rhetorical anchors — return to them clearly
- Slow → Inconsistent → Bottleneck builds in severity
- The final line is a key thesis: "asking humans to do what a platform should do"
- Transition: "And here's the thing — every team handles it differently."
