---
layout: post
title: Fixing data corruption in a PostgreSQL database running in kubernetes as a non-root container
category: Tech
tags: ['k8s', 'postgresql', 'data corruption']
author: pgmac
---

I am running the Dependency Track application in my homelab microk8s cluster. One day I started seeing error messages on INSERT's like this:
`ERROR:  invalid page in block 3693 of relation base/16384/16531`

Take note of the final number (16531 in my case), this is the file inode causing a problem. You'll need this later.

## Bitname PostgreSQL background

But first - a little background on postgresql in the bitnami container:

1. superuser account is `postgres`
2. Doesn't have a password
3. Configured to use md5 to protect passwords
4. Can't login
5. What to do?

## Finding out what's wrong

This is how I resolved my problem.

First we need to reconfigure the PostgreSQL server to allow unauthenticated connections.

### Unauth'd postgresql connections 
 
WARNING: This will open up your PostgreSQL database for all. Please be careful.

This is a bit heavy handed, but it's simple and it works.

Even though the pod is running as a non-root user AND I was connected to the pod as the running user (UID 1001) AND the `pg_hba.conf` file was owned by `root` with `664` permissions, I was still able to update the file with the following `sed` command. Perhaps I'm missing something, but I didn't expect that to work - yet it did. I'm content that it worked, but I'm not happy (and more than a little confused/worried) that it worked.

1. Connect to the pod

```kubectl --namespace <namespace> exec -ti <pgsql pod> -- /bin/bash```

{:start="2"}
2. Update the `pg_hba.conf` file to trust all connections

```sed -i 's/md5/trust/g' /opt/bitnami/postgresql/conf/pg_hba.conf```

{:start="3"}
3. Now reload postgresql to apply the changes

```pg_ctl reload```

Now you can connect locally 

```psql -U <username> <database>```

---

### Querying which objects are corrupted

Connect to the database using a local connection from within the PostgreSQL pod

```psql -U postgres postgres```

1. Now to find out which objects are affected (you don't need to do this, but it is good to know)

```
SELECT c.oid, n.nspname AS schema, c.relname,
  CASE c.relkind
  WHEN 'r' THEN 'table'
  WHEN 'i' THEN 'index'
  WHEN 't' THEN 'TOAST table'
  WHEN 'm' THEN 'materialized view'
  WHEN 'S' THEN 'sequence'
  ELSE 'other'
  END AS type
FROM pg_class AS c
JOIN pg_namespace AS n ON c.relnamespace = n.oid
WHERE c.relfilenode = <file inode id from error message>;
```

---

## Fixing the problem

Right, now we know where the problem is, we can start to repair things.

1. First - tell the database there's no damaged pages, so the repair work (and application) can continue

```set zero_damaged_pages to on;```

This allows you to actually repair (vacuum) the affected objects without throwing the same error again
 
{:start="2"}
2. Second - vacuum. This does cleanup (as the name implies)

```vacuum full verbose analyse;```

{:start="3"}
3. Third - reindex things

```reindex database <your database>```

---

## Bringing it back to normal

Finally, set your `pg_hba.conf` file to do md5 auth again

```sed -i 's/trust/md5/g' /opt/bitnami/postgresql/conf/pg_hba.conf```

```pg_ctl reload```

Everything _should_ be working just fine again. Assuming you don't have any other issues :/

---

### References

[PostgreSQL: Fixing or Mitigating this ERROR: invalid page in block 35217 of
 relation base/16421/3192429](https://www.postgresql.org/message-id/CAA3DN%3DX-ZT27Knq5BOAcdD1LsiZoBuTm6UVso%3Dn5g0LRUdHsOg%40mail.gmail.com)

[PostgreSQL Tutorial: Dealing with corrupted blocks - Redrock Postgres](https://www.rockdata.net/tutorial/troubleshooting-corrupted-blocks/)

[Modify the default administrator password](https://docs.bitnami.com/virtual-machine/infrastructure/postgresql/administration/change-reset-password/)
