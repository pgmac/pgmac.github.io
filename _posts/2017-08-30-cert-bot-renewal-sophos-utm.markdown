---
layout: post
title: Manual cert-bot renewals for certificates hosted on a Sophos UTM
category: Technology
tags: [cert-bot, letsencrypt, Sophos, UTM]
author: pgmac
---

# Renew your cert-bot certificate

I have a cert-bot certificate on my home licensed Sophos UTM. Yeah, yeah. I should upgrade to the Home XG. One of these days ... maybe. 
I also use the Remote Access feature (SSL VPN) to gain access to my stuff at home when I'm out and about. I don't have to leave my SSH, or other, ports wide open. It's just good practise. But, because it needs the user portal to get your certificates and configs for the OpenVPN SSL VPN, I can't use cert-bot's automatic renewal, as the required URL's aren't normally available. The reverse proxy configuration (Web Server Protection) doesn't seem to work with the User Portal also enabled. So, I have to go manual.

The basic steps for me go like this:

* Start the cert-bot manual process
* Disable the Sophos User Portal
* Start up a Web Server Protection config to send my requests to a backend server. This could the cert-bot temp web server. But not in my case. Because "reasons".
* Put the codes into the files (or it gets the hose) as cert-bot expects to browse them.
* Verify it all works
* Complete the cert-bot renewal
* Disable the Web Server Protection
* Re-enable the User Portal
* Convert the certificates into a PKCS#12 cert
* Upload to Sophos Certificate Manager
* Change your Sophos config to use the new PKCS#12 cert
* Good to go

## The more detailed steps look like this:

1. Start the cert-bot renewal in manual mode

   ```bash
   ./certbot-auto certonly --debug --force-renew -a manual -d your.domain.com -d your.other.domain.com -d one.more.domain.com
   CODE=<that big long string of characters as listed from the previous command>
   printf "%s" ${CODE} > /var/www/html/.well-known/acme-challenge/${CODE}
   ```

2. Go to your UTM portal

   <https://your.domain.com:4444/>{:target="_blank"}

3. Disable the User Portal
4. Start Web Server Protection config.
5. Create the config if needs be.

   I'm using an Apache server on my backend server. But, you could use the python based web server cert-bot uses to do the auto-renew, too. 
   This would mean a different order of doing things here, though. I might cover that later.

6. Ensure the required URLs work from an external source

   Mobile phones/tablets are good for that

7. Complete the cert-bot renewal

   Get all your certs updated

8. Disable the Web Server Protection

   Just disable, don't delete it. You'll need it again in 3 months

9. Re-enable the User Portal

   So you and your people can get the configs, etc you need.

10. Create the PKCS#12 cert

   Convert/combine all your certs in one PKCS#12 certificate to import into the Sophos UTM 
   You will need to give a password/passphrase when exporting. Remember this. It's important for the next step.

   ```bash
   openssl pkcs12 -export -out /tmp/certificate.pfx \
   -inkey /etc/letsencrypt/live/<domainname>/privkey.pem \
   -in /etc/letsencrypt/live/<domainname>/cert.pem \
   -certfile /etc/letsencrypt/live/<domainname>/chain.pem
   ```

11. Upload and enable

   Upload the new PKCS#12 cert to your UTM Certificate Manager. Use the password/passphrase from the previous step to import the PKCS#12 cert.
   Select the new PKCS#12 cert in the UTM Web Portal configuration.
   This will ask you to logout and reload.
   You should be all good to go now.
