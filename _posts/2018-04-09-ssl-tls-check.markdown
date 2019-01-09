---
layout: post
title: Quick SSL/TLS certificate check
category: Technology
tags: [SSL, TLS, curl, Scripts]
author: pgmac
---
While doing a lot of SSL/TLS renewals, transfers, migrations, etc recently; I was looking for a really simple tool to help me verify the certificate being served was the absolute correct one. It needed to check the:

* Issuer
* Valid from dates
* Valid to dates
* Distinguished Name
* Subject Alternate Names

I used the openssl utility to help me do this. I put this into a quick bash script to round it out for me:

```bash
#!/bin/sh

HOSTNAME=""  
PORT=443

check_dates() {  
    echo "Checking $1"
    DATE=${1:-$(date)}
    THRESHOLD=${2:-30}
    DIFF=$(($(date -d "${DATE}" +%s) - $(date +%s)))
    if [ ${DIFF} -lt 0 ]
    then
        echo "Certificate has expired!"
    elif [ ${DIFF} -lt $((${DIFF} + $((${THRESHOLD} * 24 * 60 * 60)))) ]
    then
        echo "Certificate expires within ${THRESHOLD} days"
    fi
}

while getopts ":f:h:i:p:" opt  
do  
    case ${opt} in
        f|h)
            HOSTNAME=${OPTARG}
        ;;
        i)
            IPADDR=${OPTARG}
        ;;
        p)
            PORT=${OPTARG}
        ;;
        \?)
            echo "Invalid option: -${OPTARG}" >&2
            exit 1
        ;;
        :)
            echo "Option -${OPTARG} requires an argument." >&2
            exit 1
        ;;
    esac
done  
shift $((OPTIND-1))  
[ "$1" = "--" ] && shift
[ -z ${HOSTNAME} ] && echo "You must specify a host/file to check" && exit 1
[ -z ${IPADDR} ] && IPADDR=${HOSTNAME}

echo -n "\nIssuer:"  
if [ -f ${HOSTNAME} ]  
then  
    openssl x509 -in ${HOSTNAME} -noout -issuer | cut -d'=' -f2-
else  
    echo | openssl s_client -showcerts -servername ${HOSTNAME} -connect ${IPADDR}:${PORT} 2>/dev/null | openssl x509 -inform pem -noout -issuer  | cut -d'=' -f2-
fi

echo -n "Serial Number: "  
if [ -f ${HOSTNAME} ]  
then  
    openssl x509 -in ${HOSTNAME} -noout -text  | grep -A 1 "Serial Number" | tail -1 | sed -e 's/\ //g'
else  
    echo | openssl s_client -showcerts -servername ${HOSTNAME} -connect ${IPADDR}:${PORT} 2>/dev/null | openssl x509 -inform pem -noout -text | grep -A 1 "Serial Number" | tail -1 | sed -e 's/\ //g'
fi

echo -n "Finger Print: "  
if [ -f ${HOSTNAME} ]  
then  
    openssl x509 -in ${HOSTNAME} -noout -fingerprint | cut -d'=' -f2
else  
    echo | openssl s_client -showcerts -servername ${HOSTNAME} -connect ${IPADDR}:${PORT} 2>/dev/null | openssl x509 -inform pem -noout -fingerprint | cut -d'=' -f2
fi

echo "\nValid dates\n-----------"  
if [ -f ${HOSTNAME} ]  
then  
    openssl x509 -in ${HOSTNAME} -noout -dates
else  
    echo | openssl s_client -showcerts -servername ${HOSTNAME} -connect ${IPADDR}:${PORT} 2>/dev/null | openssl x509 -inform pem -noout -dates
    #echo | openssl s_client -showcerts -servername ${HOSTNAME} -connect ${IPADDR}:${PORT} 2>/dev/null | openssl x509 -inform pem -noout -dates | grep notAfter | cut -d'=' -f2
fi

echo -n "\nCertificate subject:"  
if [ -f ${HOSTNAME} ]  
then  
    openssl x509 -in ${HOSTNAME} -noout -subject | cut -d'=' -f2-
else  
    echo | openssl s_client -showcerts -servername ${HOSTNAME} -connect ${IPADDR}:${PORT} 2>/dev/null | openssl x509 -inform pem -noout -subject | cut -d'=' -f2-
fi

echo "SAN's:"  
if [ -f ${HOSTNAME} ]  
then  
    openssl x509 -in ${HOSTNAME} -noout -text | grep "DNS:" | tr ',' "\n\t" | sed -e 's/\ //g'
else  
    echo | openssl s_client -showcerts -servername ${HOSTNAME} -connect ${IPADDR}:${PORT} 2>/dev/null | openssl x509 -inform pem -noout -text | grep "DNS:" | tr ',' "\n\t" | sed -e 's/\ //g'
fi  
```

While to worked, it relied on my doing the checks to ensure validity. It was good having the raw data there to verify, but I didn't want to be the verification engine. I wanted the tool to do that and let me know.

Enter curl.

```shell
curl -I -v https://${HOSTNAME}/
```

It still outputs all of the technical detail of the certificate, plus does the actual validation check.

If you have many servers behind a load balancer and you want to check a specific server (maybe you took it out of the load balancer first), you can use the  `--resolve` option to have curl resolve a name to a specific IP address:

```shell
curl -v --resolve myhost.name:443:a.b.c.d
```

Where:

|Value|Description|
|---:|---|
|**"myhost.name"**|is the DNS name of the site to check|
|**"443"**|is the port to connect to|
|**"a.b.c.d"**|is the IP address of the server you want to check.|

EG:

```shell
curl --resolve ${HOSTNAME}:443:${IPADDR} -I -v https://${HOSTNAME}/
```

I like curl. curl is good.
