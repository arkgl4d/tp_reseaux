### A. STP protections + ⭐ Bonus : jouer avec BPDU Filter

bpduguard et filter activé sur l'ensemble des ports non uplink et tout les ports d'accès.

CF conf dossier confs_rzo_part3 : sw1 jusqu'a sw7

### 🌞 Mettre en place DHCP snooping dans l'infra

```bash
ip dhcp snooping trust sur les uplinks et port access du serveur dhcp
ip dhcp snooping sur sw5 et sw6
ip dhcp snooping vlan 20 sur sw6 et ip dhcp snooping vlan 10,20 sur sw5
no ip dhcp snooping information option sur sw5 et sw6 car le serveur droppait les paquets
```

```bash
sw5#show ip dhcp snooping binding 
MacAddress          IpAddress        Lease(sec)  Type           VLAN  Interface
------------------  ---------------  ----------  -------------  ----  --------------------
00:50:79:66:68:0A   10.3.10.10       2164074     dhcp-snooping   10    Ethernet0/2
00:50:79:66:68:0B   10.3.20.13       2403629     dhcp-snooping   20    Ethernet0/3
Total number of bindings: 2
```

CF conf dossier confs_rzo_part3 : sw5-sw6

### 🌞 Mettre en place du DAI

```bash
ip arp inspection trust sur les uplinks de sw5 et sw6
ip arp inspection vlan 10,20 sur sw5 et ip arp inspection vlan 20 sur sw6
ip arp inspection validate src-mac ip 
```

CF conf dossier confs_rzo_part3 : sw5-sw6

### 🌞 Le réseau 10.3.30.0/24... + ⭐ Bonus : Les IP réelles des routeurs comme 10.3.10.253/24...

```bash
access-list 110 permit ip 10.3.10.0 0.0.0.255 host 10.3.30.67
access-list 110 permit ip 10.3.20.0 0.0.0.255 host 10.3.30.67
access-list 110 deny   ip 10.3.10.0 0.0.0.255 10.3.30.0 0.0.0.255
access-list 110 deny   ip 10.3.20.0 0.0.0.255 10.3.30.0 0.0.0.255
access-list 110 deny   icmp 10.3.10.0 0.0.0.255 host 10.3.10.252 echo
access-list 110 deny   icmp 10.3.10.0 0.0.0.255 host 10.3.10.253 echo
access-list 110 deny   icmp 10.3.20.0 0.0.0.255 host 10.3.20.252 echo
access-list 110 deny   icmp 10.3.20.0 0.0.0.255 host 10.3.20.253 echo
access-list 110 deny   icmp 10.3.10.0 0.0.0.255 host 10.3.20.252 echo
access-list 110 deny   icmp 10.3.10.0 0.0.0.255 host 10.3.20.253 echo
access-list 110 deny   icmp 10.3.20.0 0.0.0.255 host 10.3.10.252 echo
access-list 110 deny   icmp 10.3.20.0 0.0.0.255 host 10.3.10.253 echo
access-list 110 permit ip any any
```

Sur R1 et R2 fa0/0.10 et fa0/0.20 en access-group 110 in

CF conf dossier confs_rzo_part3 : R1-R2

### ⭐ Bonus : jouer avec IP Source Guard

Ensemble des ports accès des sw5 et sw6 :

```bash
switchport port-security maximum 2
switchport port-security violation restrict
switchport port-security mac-address sticky
switchport port-security
ip verify source
```

CF conf dossier confs_rzo_part3 : sw5-sw6