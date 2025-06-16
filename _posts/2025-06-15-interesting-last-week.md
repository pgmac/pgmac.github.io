---
layout: last-week
title: Some things I found interesting from 2025-06-08 to 2025-06-15
category: Last-Week
tags: ['cicd', 'monitoring', 'dependencies', 'python', 'ai', 'google', 'llm', 'mobile', 'ide', 'python', 'dependencies', 'python', 'coding assistant', 'llm', 'solar system', 'space', 'email', 'phishing', 'security', 'cloudflare', 'incident', 'history', 'internet', 'authentication', 'networking', 'security', 'cyber', 'phishing', 'security', 'networking', 'zero trust', 'open source', 'security', 'ubuntu', 'aws', 'k8s', 'management', 'host your own', 'open source', 'photography', 'software', 'monitoring', 'power', 'monitoring', 'power', 'monitoring', 'power', 'ai', 'llm', 'text-to-speech', 'ai', 'llm', 'observability', 'linux', 'ubuntu', 'development', 'personal', 'apple', 'macos', 'virtualisation', 'management', 'proxmox', 'virtualisation', 'mobile', 'music', 'cyber', 'security', 'google', 'knowledge', 'llm', 'management']
author: pgmac
---

Internet Discoveries between  8 and 15 June

- CI/CD Observability with OpenTelemetry - A Step by Step Guide | SigNoz
- Auto activating a python virtualenv · GitHub
- I tried Google's secret open source app and glimpsed the power of offline AI
- Setup | Ruff
- Running scripts | uv
- Remote GitHub MCP Server is now in public preview - GitHub Changelog
- www.spaceweatherlive.com
- Google Online Security Blog: On Fire Drills and Phishing Tests
- Cloudflare service outage June 12, 2025
- A history of the Internet, part 2: The high-tech gold rush begins - Ars Technica
- Frequent reauth doesn't make you more secure
- Scammers impersonating the ASD's ACSC | Cyber.gov.au
- NIST Offers 19 Ways to Build Zero Trust Architectures | NIST
- Ubuntu 25.10 Replaces sudo With a Rust-Based Equivalent - The New Stack
- AWS Launches EKS Dashboard to Tackle Multi-Cloud Kubernetes Complexity - InfoQ
- immich.app
- www.evolutionaustralia.com.au
- GitHub - jomjol/AI-on-the-edge-device: Easy to use device for connecting "old" measuring units (water, power, gas, ...) to the digital world
- IoTaWatt™ Open WiFi Electric Power Monitor
- GitHub - resemble-ai/chatterbox: SoTA open-source TTS
- It's The End Of Observability As We Know It (And I Feel Fine) | Honeycomb
- Canonical Confirms Ubuntu 25.10 Will Drop Support For GNOME On X.Org - Phoronix
- Getting Past Procastination - IEEE Spectrum
- GitHub - apple/containerization: Containerization is a Swift package for running Linux containers on macOS.
- 5 Proxmox scripts I run on every new installation
- USB-C was a missed opportunity and it’s too late to fix the mess
- abcnews.go.com
- Designing Blue Team playbooks with Wazuh for proactive incident response
- I started using NotebookLM with Obsidian and it’s been a game-changer

## Interesting details

<a name="CI/CD Observability with OpenTelemetry - A Step by Step Guide | SigNoz">[CI/CD Observability with OpenTelemetry - A Step by Step Guide | SigNoz](https://signoz.io/blog/cicd-observability-with-opentelemetry/)</a> - In the fast-paced world of CI/CD, understanding the performance and behaviour of your pipelines is crucial. In this guide, we'll walk through setting up OpenTelemetry for GitHub Actions, with practical examples and configuration snippets.

<a name="Auto activating a python virtualenv · GitHub">[Auto activating a python virtualenv · GitHub](https://gist.github.com/pgmac/0bc0da3df511ca58993ec5416950a04d)</a> - Auto activating a python virtualenv. GitHub Gist: instantly share code, notes, and snippets.

> I thought I was doing an 'ok' thing here, but never felt comfortable with the solution. Here's the solution I came with AND a link in the comments with a much better to manage dependencies for scripts. NB: the new solution is also in my links.

<a name="I tried Google's secret open source app and glimpsed the power of offline AI">[I tried Google's secret open source app and glimpsed the power of offline AI](https://www.androidauthority.com/google-ai-edge-gallery-3565904/)</a> - Available only on GitHub, Google AI Edge Gallery is the company's new AI app. But what does it do, and how does it compare to Gemini?

<a name="Setup | Ruff">[Setup | Ruff](https://docs.astral.sh/ruff/editors/setup/#zed)</a> - An extremely fast Python linter and code formatter, written in Rust.

> ruff is quick - like proper quick.
> I hear stories of people making it a pre-commit, it's _that_ quick.

<a name="Running scripts | uv">[Running scripts | uv](https://docs.astral.sh/uv/guides/scripts/#using-a-shebang-to-create-an-executable-file)</a> - A guide to using uv to run Python scripts, including support for inline dependency metadata, reproducible scripts, and more.

> I thought about doing virtualenv auto-activate - but that seemed counter-intuitive.
> Using uv to control dependencies and execute scripts is a much happier place.

<a name="Remote GitHub MCP Server is now in public preview - GitHub Changelog">[Remote GitHub MCP Server is now in public preview - GitHub Changelog](https://github.blog/changelog/2025-06-12-remote-github-mcp-server-is-now-available-in-public-preview/)</a> - Connect AI agents to GitHub tools and context with OAuth, one-click setup, and automatic updates with GitHub’s hosted server.

<a name="www.spaceweatherlive.com">[www.spaceweatherlive.com](https://www.spaceweatherlive.com/en/solar-activity/solar-flares.html)</a> - None

<a name="Google Online Security Blog: On Fire Drills and Phishing Tests">[Google Online Security Blog: On Fire Drills and Phishing Tests](https://security.googleblog.com/2024/05/on-fire-drills-and-phishing-tests.html)</a> - None

<a name="Cloudflare service outage June 12, 2025">[Cloudflare service outage June 12, 2025](https://blog.cloudflare.com/cloudflare-service-outage-june-12-2025/)</a> - Multiple Cloudflare services, including Workers KV, Access, WARP and the Cloudflare dashboard, experienced an outage for up to 2 hours and 22 minutes on June 12, 2025.

<a name="A history of the Internet, part 2: The high-tech gold rush begins - Ars Technica">[A history of the Internet, part 2: The high-tech gold rush begins - Ars Technica](https://arstechnica.com/gadgets/2025/06/a-history-of-the-internet-part-2-the-high-tech-gold-rush-begins/)</a> - The Web Era arrives, the browser wars flare, and a bubble bursts.

<a name="Frequent reauth doesn't make you more secure">[Frequent reauth doesn't make you more secure](https://tailscale.com/blog/frequent-reath-security)</a> - Securely connect to anything on the internet with Tailscale. Built on WireGuard®️, Tailscale enables you to make finely configurable connections, secured end-to-end according to zero trust principles, between any resources on any infrastructure.

<a name="Scammers impersonating the ASD's ACSC | Cyber.gov.au">[Scammers impersonating the ASD's ACSC | Cyber.gov.au](https://www.cyber.gov.au/about-us/view-all-content/alerts-and-advisories/email-scammers-impersonating-asds-acsc)</a> - Scammers are impersonating the ASD's ACSC sending out phishing emails to the public with the email content suggesting to download a malicious antivirus program.

<a name="NIST Offers 19 Ways to Build Zero Trust Architectures | NIST">[NIST Offers 19 Ways to Build Zero Trust Architectures | NIST](https://www.nist.gov/news-events/news/2025/06/nist-offers-19-ways-build-zero-trust-architectures)</a> - The examples use off-the-shelf commercial technologies, giving organizations valuable starting points

<a name="Ubuntu 25.10 Replaces sudo With a Rust-Based Equivalent - The New Stack">[Ubuntu 25.10 Replaces sudo With a Rust-Based Equivalent - The New Stack](https://thenewstack.io/ubuntu-25-10-replaces-sudo-with-a-rust-based-equivalent/)</a> - The new sudo-rs is meant to be a near drop-in replacement for sudo, but some of the less secure aspects of sudo will not be supported.

> Rusty sudo

<a name="AWS Launches EKS Dashboard to Tackle Multi-Cloud Kubernetes Complexity - InfoQ">[AWS Launches EKS Dashboard to Tackle Multi-Cloud Kubernetes Complexity - InfoQ](https://www.infoq.com/news/2025/06/aws-eks-dashboard-kubernetes/)</a> - Introducing the Amazon EKS Dashboard: a centralized management tool delivering unified visibility across multiple Kubernetes clusters in AWS. Simplifying operational oversight, it offers insights on r

<a name="immich.app">[immich.app](https://immich.app/)</a> - None

<a name="www.evolutionaustralia.com.au">[www.evolutionaustralia.com.au](https://www.evolutionaustralia.com.au/product-page/myenergi-ct-clamp)</a> - None

<a name="GitHub - jomjol/AI-on-the-edge-device: Easy to use device for connecting "old" measuring units (water, power, gas, ...) to the digital world">[GitHub - jomjol/AI-on-the-edge-device: Easy to use device for connecting "old" measuring units (water, power, gas, ...) to the digital world](https://github.com/jomjol/AI-on-the-edge-device)</a> - Easy to use device for connecting "old" measuring units (water, power, gas, ...) to the digital world - jomjol/AI-on-the-edge-device

<a name="IoTaWatt™ Open WiFi Electric Power Monitor">[IoTaWatt™ Open WiFi Electric Power Monitor](https://iotawatt.com/)</a> - Electric Power Monitor. Residential and Commercial. Single, split and three-phase. Any voltage.  Local data storage and analysis and also upload to your cloud service. Economical. Ships worldwide, in use in dozens of countries on four continents.

<a name="GitHub - resemble-ai/chatterbox: SoTA open-source TTS">[GitHub - resemble-ai/chatterbox: SoTA open-source TTS](https://github.com/resemble-ai/chatterbox)</a> - SoTA open-source TTS. Contribute to resemble-ai/chatterbox development by creating an account on GitHub.

<a name="It's The End Of Observability As We Know It (And I Feel Fine) | Honeycomb">[It's The End Of Observability As We Know It (And I Feel Fine) | Honeycomb](https://www.honeycomb.io/blog/its-the-end-of-observability-as-we-know-it-and-i-feel-fine)</a> - The history of observability tools over the past decade has been about a pretty simple concept, but LLMs bring the death of that paradigm.

<a name="Canonical Confirms Ubuntu 25.10 Will Drop Support For GNOME On X.Org - Phoronix">[Canonical Confirms Ubuntu 25.10 Will Drop Support For GNOME On X.Org - Phoronix](https://www.phoronix.com/news/Ubuntu-25.10-No-GNOME-X.Org)</a> - In aligning with upstream GNOME 49 expected to ship with X11 support disabled by default, Canonical announced today that the upcoming Ubuntu 25.10 release will also ship without support for running the GNOME desktop on X11.

<a name="Getting Past Procastination - IEEE Spectrum">[Getting Past Procastination - IEEE Spectrum](https://spectrum.ieee.org/getting-past-procastination)</a> - Create systems that allow you to be consistently productive

> Meh - I'll fix that sitting mistake in the url and title later.
> Procastination -> Procrastination

<a name="GitHub - apple/containerization: Containerization is a Swift package for running Linux containers on macOS.">[GitHub - apple/containerization: Containerization is a Swift package for running Linux containers on macOS.](https://github.com/apple/containerization)</a> - Containerization is a Swift package for running Linux containers on macOS. - apple/containerization

<a name="5 Proxmox scripts I run on every new installation">[5 Proxmox scripts I run on every new installation](https://www.xda-developers.com/proxmox-scripts-run-new-installation/)</a> - These scripts can streamline your installation.

<a name="USB-C was a missed opportunity and it’s too late to fix the mess">[USB-C was a missed opportunity and it’s too late to fix the mess](https://www.androidauthority.com/usb-c-cant-be-fixed-3560127/)</a> - USB-C aimed to unify charging and data, but years later, compatibility problems and complex specs make it a headache for consumers worldwide.

<a name="abcnews.go.com">[abcnews.go.com](https://abcnews.go.com/US/sly-stone-pioneering-leader-funk-band-sly-family/story?id=122666345)</a> - None

<a name="Designing Blue Team playbooks with Wazuh for proactive incident response">[Designing Blue Team playbooks with Wazuh for proactive incident response](https://www.bleepingcomputer.com/news/security/designing-blue-team-playbooks-with-wazuh-for-proactive-incident-response/)</a> - Blue Team playbooks are essential—but tools like Wazuh take them to the next level. From credential dumping to web shells and brute-force attacks, see how Wazuh strengthens real-time detection and automated response.

<a name="I started using NotebookLM with Obsidian and it’s been a game-changer">[I started using NotebookLM with Obsidian and it’s been a game-changer](https://www.xda-developers.com/using-notebooklm-with-obsidian/)</a> - My secret combo for peak productivity


---

All this was saved to my [Link Ace](https://links.pgmac.net.au/) over the week