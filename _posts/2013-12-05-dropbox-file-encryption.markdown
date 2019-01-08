---
layout: post
title: Finally a workable solution to encrypt and secure Dropbox contents
category: Technology
author: pgmac
---
Finally a workable solution to encrypt and secure Dropbox contents

EncFS...a userspace filesystem encryption system that has clients available on [Windows](http://members.ferrara.linux.it/freddy77/encfs.html){:target="_blank"} and your favourite [Linux](https://wiki.archlinux.org/index.php/EncFS){:target="_blank"}.

EncFS encrypts encrypts each file separately unlike TrueCrypt which uses an encrypted filesystem.  This means that DropBox will sync each file as it is operated on unlike containers which will only sync when the container is closed.
