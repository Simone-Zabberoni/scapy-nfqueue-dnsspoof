# Simple DNS spoof with scapy and nfqueue

## Description

Intercept all dns queries, spoof the answer by requested FQDN.

It's just a simple poc to test scapy+nfqueue toghether.

Usage:
```
dnsSpoof -q 1 -s www.youporn.com/1.2.3.4
```

## Requirements

- python 2.7 (yes, I know)
- [Scapy](http://www.secdev.org/projects/scapy/)
- gcc compiler, netfilter headers etc...

## Setup

Install packages, on a Centos/RHEL machine:

```
yum -y install python-pip scapy
yum -y install gcc python-devel libnfnetlink-devel libnetfilter_queue-devel libnetfilter_conntrack-devel
```

Install the required python modules:

```
pip install -r requirements.txt
```

## Run it

Activate the spoofer:

```
# ./dnsSpoof.py -q 1 -s www.youporn.com/1.2.3.4
Intercepting nfqueue: 1
Spoofing www.youporn.com to 1.2.3.4
------------------------------------------
```

**Nothing will happen right now**, we've just activated the spoofer and its binding to nfqueue 1

Let's redirect all dns responses (udp and source port 53) to dnsSpoof.py:

```
[root@spoofmachine ~]# iptables -A INPUT -p udp  --sport 53 -j NFQUEUE --queue-num 1
[root@spoofmachine ~]# iptables -L -nv
Chain INPUT (policy ACCEPT 9 packets, 680 bytes)
 pkts bytes target     prot opt in     out     source               destination
    0     0 NFQUEUE    udp  --  *      *       0.0.0.0/0            0.0.0.0/0            udp spt:53 NFQUEUE num 1
```

Spoofing in action, but only for the target domain

```
[root@spoofmachine ~]# ping www.youporn.com
PING www.youporn.com (1.2.3.4) 56(84) bytes of data.

[root@spoofmachine ~]# ping www.google.com
PING www.google.com (216.58.205.132) 56(84) bytes of data.
```

The spoofer shows the summary of the packets (`pkt.summary()` scapy function):

```
Intercepted DNS request for www.youporn.com: IP / UDP / DNS Ans "youporn.com."
Spoofing DNS response to: IP / UDP / DNS Ans "1.2.3.4"
------------------------------------------
Intercepted DNS request for www.youporn.com: IP / UDP / DNS Ans "youporn.com."
Spoofing DNS response to: IP / UDP / DNS Ans "1.2.3.4"
------------------------------------------
```

**Important**: if you deactivate the spoofer, your system will be unable to resolve anything until you deactivate the iptables rule as well!

## References

- [Scapy project](http://www.secdev.org/projects/scapy/)
- [Scapy usage and examples](http://scapy.readthedocs.io/en/latest/usage.html)
- [Netfilter Queue](http://netfilter.org/projects/libnetfilter_queue/)
