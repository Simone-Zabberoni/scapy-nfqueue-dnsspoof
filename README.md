# Simple DNS spoof with scapy and nfqueue

## Description

Intercept all dns queries, spoof the answer by requested domain.
It's just a simple poc to test scapy+nfqueue toghether

## Requirements

- python 2.7 (yes, I know)
- [Scapy](http://www.secdev.org/projects/scapy/)
- gcc compiler, netfilter headers etc...


## Setup

Install packages, on a Centos/RHEL machine:

```
yum install python-pip
yum install scapy
yum install gcc python-devel libnfnetlink-devel libnetfilter_queue-devel libnetfilter_conntrack-devel
```

Upgrade pip and install/compile the python module:

```
pip install --upgrade pip
pip install NetfilterQueue
```

## Run it

Activate the spoofer:

```
[root@spoofmachine ~]# python dnsSpoof.py
Intercepting nfqueue: 1
Spoofing www.youporn.com to 1.1.1.1
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
PING www.youporn.com (1.1.1.1) 56(84) bytes of data.

[root@spoofmachine ~]# ping www.google.com
PING www.google.com (216.58.205.132) 56(84) bytes of data.
```

The spoofer shows the summary of the packets (`pkt.summary()` scapy function):
```
Intercepted DNS request for www.youporn.com: IP / UDP / DNS Ans "youporn.com."
Spoofing DNS response to: IP / UDP / DNS Ans "1.1.1.1"
------------------------------------------
Intercepted DNS request for www.youporn.com: IP / UDP / DNS Ans
Spoofing DNS response to: IP / UDP / DNS Ans "1.1.1.1"
```

## References

- [Scapy project](http://www.secdev.org/projects/scapy/)
- [Scapy usage and examples](http://scapy.readthedocs.io/en/latest/usage.html)
- [Netfilter Queue](http://netfilter.org/projects/libnetfilter_queue/)
