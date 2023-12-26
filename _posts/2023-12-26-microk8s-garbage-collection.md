---
layout: post
title: Pruning microk8s containerd when k8s garbage collection fails
category: Technology
tags: [microk8s, containerd, prune, garbage collection]
author: pgmac
---
microk8s, well k8s as a whole tbf, seems to really struggle with garbage collection when the disk is (nearly) full.
Which seems odd to me. When you really need garbaga collection to work, it's failing on you. Why is that? Grinds my gears, it does.

Anyway, you might see node events like this:

```
  Type     Reason               Age                   From     Message
  ----     ------               ----                  ----     -------
  Warning  FreeDiskSpaceFailed  41m (x50 over 4h46m)  kubelet  (combined from similar events): Failed to garbage collect required amount of images. Attempted to free 14442242048 bytes, but only found 0 bytes eligible to free.
```

How do you solve a problem like garbage collection?
Well, it's not that easy.

The general consensus is "don't let it get that bad".
Yeah, thanks. Helpful.

"Just add more disk".
Yeah, that can work. But it is really just addressing the symptom and not the cause so much.
Also - this isn't an option for some. Especially me running this on tin in my homelab where my available storage is limited.

How about some manual garbage collection?
That has more merit. But, how to do it?

microk8s uses `containerd` under the hood for it's containerisation engine.
It even has it's own interface into it: `microk8s.ctr`

But, first - you need to connect to the microk8s node in question.

Having a look around `microk8s.ctr` on the problem node in there, I found:

`microk8s images list`
This will list out all of the images currently on a node.
This can, and probably will, give you a great number of entries. Espeically on a system that's been running for a while.

`microk8s images rm <image reference>`
This will remove the referenced image from containerd on the node.
But how to decide which image(s) you can remove? Yeah, I'm not digging through all of those images, either.

Instead, I was looking for something more like `docker prune`.
containerd does have something similar
`microk8s.ctr content prune references`

It's not exact, but it will clean up some strays for you.
This got me back about 5% disk space (on an 80GB file system).
That'll do for now.

Now - to schedule this on a regular period. But, that's a story for another night.

What I would dearly love to do is to figure out WHY the kubelet found 0 eligible bytes for garbage collection.
If I could do that, then address that problem, I'd be in a much happier place.

By all reports from my searching, this seems to be poorly logged right now, so investigating is difficult.
Garbage collection is a bit of a black art (not as bad as cache invalidation, of course).