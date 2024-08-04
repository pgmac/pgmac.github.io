---
layout: last-week
title: Some things I found interesting from 2024-07-28 to 2024-08-04
category: Last-Week
tags: ['certificates', 'security', 'security', '4g', '5g', 'bill', 'internet', 'nbnco', 'certificates', 'devsecops', 'github', 'security', 'ai', 'security', 'testing', 'git', 'releases', 'authentication', 'open source', 'saml', 'sso', 'macos', 'security', 'identity', 'security', 'github', 'secu', 'ai', 'image', 'open source', 'text', 'games', 'networks', 'proxy', 'security', 'ai', 'identity', 'security', 'ai', 'image', 'open source']
author: pgmac
---

Internet Discoveries between 28 July and  4 August
- All I Know About Certificates -- Certificate Authority
- Cyber ransom payments will need to be disclosed by businesses under new laws
- ACCC shifts support for broadband tax on 4G and 5G fixed wireless
- DigiCert Revocation Incident (CNAME-Based Domain Validation)
- Introducing Artifact Attestations–now in public beta
- NIST releases open-source platform for AI safety testing
- Highlights from Git 2.46
- ssoready/ssoready
- Our audit of Homebrew
- Free Shadow IT Scanner
- Artifact Attestations is generally available
- Announcing Flux: The Next Leap in Text-to-Image Models
- IPv4 Turf War
- OpenAI’s Sam Altman is becoming one of the most powerful people on Earth. We should be very afraid
- Implementing Identity Continuity With the NIST Cybersecurity Framework
- black-forest-labs/flux-dev – Run with an API on Replicate

## Interesting details

<a name="All I Know About Certificates -- Certificate Authority">[All I Know About Certificates -- Certificate Authority](https://www.pixelstech.net/article/1722045726-All-I-Know-About-Certificates----Certificate-Authority)</a> - One of the crucial steps in the TLS handshake is for the server to prove its identity to the client. While there is plenty of content explaining the principles of the handshake, there's less information about certificates, which are a critical component of TLS/SSL.

<a name="Cyber ransom payments will need to be disclosed by businesses under new laws">[Cyber ransom payments will need to be disclosed by businesses under new laws](https://www.abc.net.au/news/2024-07-30/cyber-ransom-payments-new-laws-before-parliament/104113038)</a> - The Cyber Security Act would force businesses to disclose when they pay ransom to a hacker, and prevent the information from being passed on to regulators. The proposal is designed to lift the lid on a flourishing practice of secret payments, which in turn fuel further ransomware attacks.

<a name="ACCC shifts support for broadband tax on 4G and 5G fixed wireless">[ACCC shifts support for broadband tax on 4G and 5G fixed wireless](https://www.itnews.com.au/news/accc-shifts-support-for-broadband-tax-on-4g-and-5g-fixed-wireless-610215)</a> - The ACCC has made a case for the ‘broadband tax’ on NBN-equivalent services to be expanded to 4G and 5G fixed wireless, after years of resistance to lobbying by NBN Co.

<a name="DigiCert Revocation Incident (CNAME-Based Domain Validation)">[DigiCert Revocation Incident (CNAME-Based Domain Validation)](https://www.digicert.com/support/certificate-revocation-incident)</a> - Browsers require Certificate Authorities to verify each domain included in a TLS certificate request before issuing a certificate. One of the allowed methods of DCV is called “Method 7” or “DNS-based verification”.

<a name="Introducing Artifact Attestations–now in public beta">[Introducing Artifact Attestations–now in public beta](https://github.blog/news-insights/product-news/introducing-artifact-attestations-now-in-public-beta/)</a> - June 25, 2024 update: Artifact Attestations is now generally available! Get started today. There’s an increasing need across enterprises and the open source ecosystem to have a verifiable way to link software artifacts back to their source code and build instructions.

<a name="NIST releases open-source platform for AI safety testing">[NIST releases open-source platform for AI safety testing](https://www.scmagazine.com/news/nist-releases-open-source-platform-for-ai-safety-testing)</a> - The National Institute of Standards and Technology (NIST) released a new open-source software tool for testing the resilience of machine learning (ML) models to various types of attacks.

<a name="Highlights from Git 2.46">[Highlights from Git 2.46](https://github.blog/open-source/git/highlights-from-git-2-46/)</a> - The open source Git project just released Git 2.46 with features and bug fixes from over 96 contributors, 31 of them new. We last caught up with you on the latest in Git back when 2.45 was released.

<a name="ssoready/ssoready">[ssoready/ssoready](https://github.com/ssoready/ssoready)</a> - We're building dev tools for implementing Enterprise SSO. You can use SSOReady to add SAML support to your product this afternoon, for free, forever. You can think of us as an open source alternative to products like Auth0 or WorkOS. For full documentation, check out https://ssoready.com/docs.

<a name="Our audit of Homebrew">[Our audit of Homebrew](https://blog.trailofbits.com/2024/07/30/our-audit-of-homebrew/)</a> - This is a joint post with the Homebrew maintainers; read their announcement here! Last summer, we performed an audit of Homebrew.

<a name="Free Shadow IT Scanner">[Free Shadow IT Scanner](https://www.accessowl.io/scan)</a> - An identity governance and administration tool.

<a name="Artifact Attestations is generally available">[Artifact Attestations is generally available](https://github.blog/changelog/2024-06-25-artifact-attestations-is-generally-available/)</a> - We’re thrilled to announce the general availability of GitHub Artifact Attestations! Artifact Attestations allow you to guarantee the integrity of artifacts built inside GitHub Actions by creating and verifying signed attestations.

<a name="Announcing Flux: The Next Leap in Text-to-Image Models">[Announcing Flux: The Next Leap in Text-to-Image Models](https://blog.fal.ai/flux-the-largest-open-sourced-text2img-model-now-available-on-fal/)</a> - We are excited to introduce Flux, the largest SOTA open source text-to-image model to date, brought to you by Black Forest Labs—the original team behind Stable Diffusion.

<a name="IPv4 Turf War">[IPv4 Turf War](http://ipv4.games/)</a> - Claim The Land At Your IP (What is this?) Top Players Loading top players... All /8 Address Blocks Loading...

<a name="OpenAI’s Sam Altman is becoming one of the most powerful people on Earth. We should be very afraid">[OpenAI’s Sam Altman is becoming one of the most powerful people on Earth. We should be very afraid](https://www.theguardian.com/technology/article/2024/aug/03/open-ai-sam-altman-chatgpt-gary-marcus-taming-silicon-valley)</a> - On 16 May 2023, Sam Altman, OpenAI’s charming, softly spoken, eternally optimistic billionaire CEO, and I stood in front of the US Senate judiciary subcommittee meeting on AI oversight. We were in Washington DC, and it was at the height of AI mania. Altman, then 38, was the poster boy for it all.

<a name="Implementing Identity Continuity With the NIST Cybersecurity Framework">[Implementing Identity Continuity With the NIST Cybersecurity Framework](https://www.darkreading.com/cybersecurity-operations/implementing-identity-continuity-with-nist-cybersecurity-framework)</a> - Eric has made a career out of simplifying and securing enterprise identity management. He founded, scaled, and successfully exited both Securant/ClearTrust (Web Access Management) and Symplified, (the first IDaaS company).

<a name="black-forest-labs/flux-dev – Run with an API on Replicate">[black-forest-labs/flux-dev – Run with an API on Replicate](https://replicate.com/black-forest-labs/flux-dev)</a> - FLUX.1 [dev] is a 12 billion parameter rectified flow transformer capable of generating images from text descriptions. For more information, please read our blog post. We provide a reference implementation of FLUX.1 [dev], as well as sampling code, in a dedicated github repository.

All this was saved to my [GetPocket](https://getpocket.com/) over the week