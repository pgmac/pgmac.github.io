---
layout: last-week
title: Some things I found interesting from 2025-09-14 to 2025-09-21
category: Last-Week
tags: ['development', 'software', 'games', 'active direcotry', 'cyber', 'security', 'vulnerability']
author: pgmac
---

Internet Discoveries between 14 and 21 September

- blog.inf.ed.ac.uk
- Playing &quot;Minecraft&quot; without Minecraft (free minecraft-like/compatible game) - LenOwO
- One Token to rule them all - obtaining Global Admin in every Entra ID tenant via Actor tokens - dirkjanm.io

## Interesting details

<a name="blog.inf.ed.ac.uk"></a>[blog.inf.ed.ac.uk](https://blog.inf.ed.ac.uk/sapm/2014/03/14/we-could-write-nearly-perfect-software-but-we-choose-not-to/) - &nbsp;

<a name="Playing &quot;Minecraft&quot; without Minecraft (free minecraft-like/compatible game) - LenOwO"></a>[Playing &quot;Minecraft&quot; without Minecraft (free minecraft-like/compatible game) - LenOwO](https://lenowo.org/viewtopic.php?t=5) - Ever wanted to play the worlds second most popular videogame without actually playing it? Well, I will guide you through it! First of all, what do I mean by 'Pl

<a name="One Token to rule them all - obtaining Global Admin in every Entra ID tenant via Actor tokens - dirkjanm.io"></a>[One Token to rule them all - obtaining Global Admin in every Entra ID tenant via Actor tokens - dirkjanm.io](https://dirkjanm.io/obtaining-global-admin-in-every-entra-id-tenant-with-actor-tokens/) - While preparing for my Black Hat and DEF CON talks in July of this year, I found the most impactful Entra ID vulnerability that I will probably ever find. One that could have allowed me to compromise every Entra ID tenant in the world (except probably those in national cloud deployments). If you are an Entra ID admin reading this, yes that means complete access to your tenant. The vulnerability consisted of two components: undocumented impersonation tokens that Microsoft uses in their backend for service-to-service (S2S) communication, called “Actor tokens”, and a critical vulnerability in the (legacy) Azure AD Graph API that did not properly validate the originating tenant, allowing these tokens to be used for cross-tenant access.


---

All this was saved to my [Link Ace](https://links.pgmac.net.au/) over the week