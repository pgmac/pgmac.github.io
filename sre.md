---
layout: page
title: Site Reliability Engineering
permalink: /sre/
---

Site Reliability Engineering is the discipline I've spent a significant chunk of my career in, and it's one that refuses to sit still. This section is my attempt to document where it came from, what it has been, where it is now, and where I think it's heading.

---

## Before SRE: The Era of Ops and Heroes

Before SRE had a name, there were sysadmins and operations teams — the people who kept the lights on after the developers went home. The work was largely reactive: something breaks, someone pages a person, that person fixes it. The divide between "those who build" and "those who run" was wide and often adversarial. Development teams threw software over the wall, and ops caught it (or didn't). Reliability was not engineered; it was hoped for, and when things went wrong, the answer was usually more humans on call, more heroism, and more tribal knowledge locked in the heads of whoever had been there longest.

This model scaled poorly. As systems grew more complex and the internet became load-bearing infrastructure for entire economies, the hero model became a liability. Outages got more expensive, on-call rotations got more brutal, and "we'll fix it when it breaks" stopped being an acceptable answer. The industry needed something better.

---

## How SRE Started: Google's Answer to Scale

Site Reliability Engineering as a formal discipline was born at Google in the early 2000s, largely through the work of Ben Treynor Sloss. The core insight was deceptively simple: if you want software to be reliable, treat reliability as a software problem. Hire software engineers to do operations work, give them the tools and mandate to automate everything that can be automated, and define reliability targets that are precise enough to be engineered against.

Google published this thinking openly in their [SRE Book](https://sre.google/sre-book/table-of-contents/) (freely available online), which became the closest thing the industry has to a founding document. The SRE Book introduced concepts that are now standard vocabulary: Service Level Objectives (SLOs), error budgets, toil reduction, and the idea that operations is an engineering discipline rather than a support function.

Crucially, SRE pushed back on the idea that incidents are primarily caused by individual human error. The field borrowed from aviation safety and systems theory: complex systems fail in complex ways, and blaming the person who happened to be at the keyboard when things went sideways doesn't prevent the next failure. John Allspaw's [The Infinite Hows](https://www.kitchensoap.com/2014/11/14/the-infinite-hows-or-the-dangers-of-the-five-whys/) is a landmark piece on this shift in thinking — why asking "how?" in a postmortem produces more useful learning than asking "why?" ever does.

---

## The Middle Years: SRE Grows Up and Spreads Out

Through the 2010s, SRE moved beyond Google and into the broader industry. The practices adapted — not every organisation could or should copy Google's exact model, but the underlying principles were transferable. DevOps emerged in parallel as a cultural movement with overlapping concerns: breaking down silos, automating pipelines, measuring what matters. The two were never quite the same thing, but they fertilised each other.

This period saw the maturing of the SLO/SLI/SLA framework, the mainstreaming of blameless postmortems, the rise of observability as a first-class concern (not just monitoring), and the growth of the on-call discipline. Error budgets became a shared language between product and reliability — a way to quantify the cost of risk and make tradeoffs legible. Chaos engineering emerged, formalised most visibly by Netflix's [Chaos Monkey](https://netflix.github.io/chaosmonkey/) work, as a way to build confidence in system resilience by deliberately introducing failure.

Incident management also got more rigorous. Industry practitioners pushed hard on learning from incidents rather than just closing them — the ideas in John Allspaw's work on blameless culture, and organisations like the [Learning from Incidents](https://www.learningfromincidents.io/) community, built a genuine body of practice around how to run postmortems that actually improve systems.

---

## Where SRE Is Now: Maturity, AI, and the Expanding Scope

SRE in 2026 is a mature discipline, but one that's being reshaped by two forces: AI-assisted operations and the expanding definition of what "reliability" even means.

On the AI front, the picture is nuanced. The [2026 SRE Report from Catchpoint](https://resources.catchpoint.com/hubfs/Website%20Assets%20-%20Briefs%2c%20EBooks%2c%20etc/The%20SRE%20Report%202026%20Catchpoint.pdf) paints a picture of an industry that is adopting AI tooling heavily — for anomaly detection, alert triage, and automated remediation — but is doing so with eyes open to the new failure modes that come with it. AI systems introduce their own reliability concerns: model drift, opaque failure modes, dependency on external APIs, and the challenge of knowing when to trust an automated recommendation versus when human judgment is required.

On the expanding scope front, SRE is increasingly being asked to take ownership of things that were previously considered someone else's problem: security posture, cost efficiency, developer experience, and the reliability of AI inference pipelines themselves. Swizec Teller's piece [The Future of Software Engineering is SRE](https://swizec.com/blog/the-future-of-software-engineering-is-sre/) articulates this well — as code generation gets cheaper, the hard problems shift squarely into the operational domain. Anyone can ship a demo; keeping it running reliably at scale is where the engineering challenge lives.

Google's adoption of [System Theoretic Process Analysis (STPA)](https://sre.google/stpa/teaching/) for outage prevention signals another maturation: moving from reactive postmortems to proactive hazard analysis. STPA treats safety as a control problem, modelling systems as control-feedback loops and looking for unsafe states before they occur — not just attributing blame after they do.

---

## Where SRE Is Heading: My Take

A few threads I'm watching closely.

**The abstraction of toil will raise the floor — and the ceiling.** AI-assisted on-call, automated remediation, and intelligent alerting will eliminate a lot of the repetitive grunt work that has always been part of SRE. That's genuinely good. But it will also raise expectations: if the easy stuff is handled automatically, humans will be asked to deal with increasingly novel, complex, and ambiguous situations. The cognitive demand on the on-call engineer won't go away; it will shift.

**Reliability engineering will merge with AI engineering.** As organisations run more AI workloads in production, the SRE discipline will need to develop new primitives for AI-specific reliability: latency SLOs for inference, handling model version drift, managing GPU resource contention, and understanding failure modes that don't look like traditional software failures. The SRE who can reason about both distributed systems and ML infrastructure is going to be very valuable.

**The "how" of incidents will keep mattering more than the "why".** The shift from root-cause-hunting to systemic learning that Allspaw wrote about in 2014 is still not universal. The industry will continue moving in that direction, and organisations that treat incidents as learning opportunities — rather than blame assignments — will build more resilient systems and more sustainable teams.

**Platform engineering and SRE will converge further.** The internal developer platform as a reliability primitive is already happening. SREs increasingly own the paved roads that other engineers drive on, and the reliability of the platform is inseparable from the reliability of the products built on it.

---

## Posts in This Section

{% for post in site.categories.sre %}
- [{{ post.title }}]({{ post.url }}) — <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%Y-%m-%d" }}</time>
{% endfor %}

---

*This page is a living document. I'll update it as the field evolves and as my thinking does.*
