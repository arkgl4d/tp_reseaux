### 🌞 Serveur DHCP, si c'est un serveur dédié

```bash
[admuser@node1 ~]$ systemctl status dhcpd.service
● dhcpd.service - DHCPv4 Server Daemon
     Loaded: loaded (/usr/lib/systemd/system/dhcpd.service; enabled; preset: disabled)
     Active: active (running) since Mon 2025-03-24 22:47:44 CET; 19min ago
       Docs: man:dhcpd(8)
             man:dhcpd.conf(5)
   Main PID: 824 (dhcpd)
     Status: "Dispatching packets..."
      Tasks: 1 (limit: 23148)
     Memory: 7.2M
        CPU: 17ms
     CGroup: /system.slice/dhcpd.service
             └─824 /usr/sbin/dhcpd -f -cf /etc/dhcp/dhcpd.conf -user dhcpd -group dhcpd --no-pid
```

```bash
[admuser@node1 ~]$ sudo cat /etc/dhcp/dhcpd.conf
[sudo] password for admuser: 
#
# DHCP Server Configuration file.
#   see /usr/share/doc/dhcp-server/dhcpd.conf.example
#   see dhcpd.conf(5) man page
#

default-lease-time 2592000;
max-lease-time 3888000;
authoritative;
subnet 10.3.10.0 netmask 255.255.255.0 {
    interface ens19;
    range 10.3.10.10 10.3.10.200;
    option routers 10.3.10.254;
    option subnet-mask 255.255.255.0;
    option domain-name-servers 1.1.1.1;
}
subnet 10.3.20.0 netmask 255.255.255.0 {
    interface ens19;
    range 10.3.20.10 10.3.20.200;
    option routers 10.3.20.254;
    option subnet-mask 255.255.255.0;
    option domain-name-servers 1.1.1.1;
}
```

```bash
[admuser@node1 ~]$ sudo ufw status
Status: active

To                         Action      From
--                         ------      ----
SSH                        ALLOW       Anywhere                  
224.0.0.251 mDNS           ALLOW       Anywhere                  
67/udp                     ALLOW       Anywhere                  
22/tcp                     ALLOW       Anywhere                  
SSH (v6)                   ALLOW       Anywhere (v6)             
ff02::fb mDNS              ALLOW       Anywhere (v6)             
22/tcp (v6)                ALLOW       Anywhere (v6)             
67/udp (v6)                ALLOW       Anywhere (v6)             
```

### 🌞 Depuis pc4.tp3.my

```bash
VPCS> ip dhcp
DORA IP 10.3.10.10/24 GW 10.3.10.254

#CF tcpdump pc04-tp03.my-dhcp.pcap
```

```bash
VPCS> ping 10.3.30.11


84 bytes from 10.3.30.11 icmp_seq=1 ttl=63 time=32.556 ms
84 bytes from 10.3.30.11 icmp_seq=2 ttl=63 time=11.866 ms
84 bytes from 10.3.30.11 icmp_seq=3 ttl=63 time=9.010 ms
84 bytes from 10.3.30.11 icmp_seq=4 ttl=63 time=8.670 ms
84 bytes from 10.3.30.11 icmp_seq=5 ttl=63 time=9.257 ms

#CF tcpdump pc04-tp03.my-ping1.pcap
```

```bash
VPCS> ping ynov.com  
ynov.com resolved to 104.26.11.233

84 bytes from 104.26.11.233 icmp_seq=1 ttl=53 time=29.626 ms
84 bytes from 104.26.11.233 icmp_seq=2 ttl=53 time=28.003 ms
84 bytes from 104.26.11.233 icmp_seq=3 ttl=53 time=28.310 ms
84 bytes from 104.26.11.233 icmp_seq=4 ttl=53 time=28.354 ms
84 bytes from 104.26.11.233 icmp_seq=5 ttl=53 time=28.970 ms

#CF tcpdump pc04-tp03.my-ping2.pcap
```

### 🌞 Depuis pc2.tp3.my

```bash
VPCS> ip dhcp
DORA IP 10.3.20.10/24 GW 10.3.20.254

#CF tcpdump pc02-tp03.my-dhcp.pcap
```

```bash
VPCS> ping 10.3.30.11

84 bytes from 10.3.30.11 icmp_seq=1 ttl=63 time=26.359 ms
84 bytes from 10.3.30.11 icmp_seq=2 ttl=63 time=7.476 ms
84 bytes from 10.3.30.11 icmp_seq=3 ttl=63 time=8.564 ms
84 bytes from 10.3.30.11 icmp_seq=4 ttl=63 time=8.356 ms
84 bytes from 10.3.30.11 icmp_seq=5 ttl=63 time=7.840 ms

#CF tcpdump pc02-tp03.my-ping1.pcap
```

```bash
VPCS> ping ynov.com
ynov.com resolved to 104.26.10.233

84 bytes from 104.26.10.233 icmp_seq=1 ttl=53 time=29.328 ms
84 bytes from 104.26.10.233 icmp_seq=2 ttl=53 time=27.956 ms
84 bytes from 104.26.10.233 icmp_seq=3 ttl=53 time=28.261 ms
84 bytes from 104.26.10.233 icmp_seq=4 ttl=53 time=38.595 ms
84 bytes from 104.26.10.233 icmp_seq=5 ttl=53 time=28.330 ms

##CF tcpdump pc02-tp03.my-ping2.pcap
```

### 🌞 Vérifier, à l'aide de commandes dédiées

```bash
sw1#show etherchannel 1 summary 
Flags:  D - down        P - bundled in port-channel
        I - stand-alone s - suspended
        H - Hot-standby (LACP only)
        R - Layer3      S - Layer2
        U - in use      N - not in use, no aggregation
        f - failed to allocate aggregator

        M - not in use, minimum links not met
        m - not in use, port not aggregated due to minimum links not met
        u - unsuitable for bundling
        w - waiting to be aggregated
        d - default port

        A - formed by Auto LAG


Number of channel-groups in use: 1
Number of aggregators:           1

Group  Port-channel  Protocol    Ports
------+-------------+-----------+-----------------------------------------------
1      Po1(SU)         LACP      Et0/0(P)    Et0/1(P)    
```


### 🌞 Couper le routeur prioritaire

```bash
R1#show standby brief 
                     P indicates configured to preempt.
                     |
Interface   Grp  Pri P State   Active          Standby         Virtual IP
Fa0/0.10    10   100 P Active  local           10.3.10.253     10.3.10.254
Fa0/0.20    20   100 P Active  local           10.3.20.253     10.3.20.254
Fa0/0.30    30   100 P Standby 10.3.30.253     local           10.3.30.254
```

```bash
R2#show standby brief 
                     P indicates configured to preempt.
                     |
Interface   Grp  Pri P State   Active          Standby         Virtual IP
Fa0/0.10    10   90  P Standby 10.3.10.252     local           10.3.10.254
Fa0/0.20    20   90  P Standby 10.3.20.252     local           10.3.20.254
Fa0/0.30    30   110 P Active  local           10.3.30.252     10.3.30.254
```

CF ping_hsrp.pcap

### 🌞 Couper un switch crucial dans la topo STP

```bash
#core

sw1#show spanning-tree vlan ? 
  WORD  vlan range, example: 1,3-5,7,9-11

sw1#show spanning-tree vlan 10,20,30

VLAN0010
  Spanning tree enabled protocol ieee
  Root ID    Priority    32778
             Address     aabb.cc00.3000
             This bridge is the root
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

  Bridge ID  Priority    32778  (priority 32768 sys-id-ext 10)
             Address     aabb.cc00.3000
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
             Aging Time  300 sec

Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- --------------------------------
Et0/2               Desg FWD 100       128.3    P2p 
Et0/3               Desg FWD 100       128.4    P2p 
Et1/0               Desg FWD 100       128.5    P2p 
Po1                 Desg FWD 56        128.65   P2p 


VLAN0020
  Spanning tree enabled protocol ieee
  Root ID    Priority    32788
             Address     aabb.cc00.3000
             This bridge is the root
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

  Bridge ID  Priority    32788  (priority 32768 sys-id-ext 20)
             Address     aabb.cc00.3000
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
             Aging Time  300 sec

Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- --------------------------------
Et0/2               Desg FWD 100       128.3    P2p 
Et0/3               Desg FWD 100       128.4    P2p 
Et1/0               Desg FWD 100       128.5    P2p 
Po1                 Desg FWD 56        128.65   P2p 


VLAN0030
  Spanning tree enabled protocol ieee
  Root ID    Priority    32798
             Address     aabb.cc00.3000
             This bridge is the root
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

  Bridge ID  Priority    32798  (priority 32768 sys-id-ext 30)
             Address     aabb.cc00.3000
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
             Aging Time  300 sec

Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- --------------------------------
Et0/2               Desg FWD 100       128.3    P2p 
Et0/3               Desg FWD 100       128.4    P2p 
Et1/0               Desg FWD 100       128.5    P2p 
Po1                 Desg FWD 56        128.65   P2p 
```

```bash
#distrib

sw3#show spanning-tree vlan 10,20,30

VLAN0010
  Spanning tree enabled protocol ieee
  Root ID    Priority    32778
             Address     aabb.cc00.3000
             Cost        100
             Port        4 (Ethernet0/3)
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

  Bridge ID  Priority    32778  (priority 32768 sys-id-ext 10)
             Address     aabb.cc00.5000
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
             Aging Time  300 sec

Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- --------------------------------
Et0/0               Desg FWD 100       128.1    P2p 
Et0/3               Root FWD 100       128.4    P2p 
Et1/0               Altn BLK 100       128.5    P2p 


VLAN0020
  Spanning tree enabled protocol ieee
  Root ID    Priority    32788
             Address     aabb.cc00.3000
             Cost        100
             Port        4 (Ethernet0/3)
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

  Bridge ID  Priority    32788  (priority 32768 sys-id-ext 20)
             Address     aabb.cc00.5000
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
             Aging Time  300 sec

Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- --------------------------------
Et0/0               Desg FWD 100       128.1    P2p 
Et0/2               Desg FWD 100       128.3    P2p 
Et0/3               Root FWD 100       128.4    P2p 
Et1/0               Altn BLK 100       128.5    P2p 


VLAN0030
  Spanning tree enabled protocol ieee
  Root ID    Priority    32798
             Address     aabb.cc00.3000
             Cost        100
             Port        4 (Ethernet0/3)
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

  Bridge ID  Priority    32798  (priority 32768 sys-id-ext 30)
             Address     aabb.cc00.5000
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
             Aging Time  300 sec

Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- --------------------------------
Et0/1               Desg FWD 100       128.2    P2p 
Et0/3               Root FWD 100       128.4    P2p 
Et1/0               Altn BLK 100       128.5    P2p 
```

```bash
#access

sw5#show spanning-tree vlan 10,20,30

VLAN0010
  Spanning tree enabled protocol ieee
  Root ID    Priority    32778
             Address     aabb.cc00.3000
             Cost        200
             Port        1 (Ethernet0/0)
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

  Bridge ID  Priority    32778  (priority 32768 sys-id-ext 10)
             Address     aabb.cc00.7000
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
             Aging Time  300 sec

Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- --------------------------------
Et0/0               Root FWD 100       128.1    P2p 
Et0/1               Altn BLK 100       128.2    P2p 
Et0/2               Desg FWD 100       128.3    P2p 


VLAN0020
  Spanning tree enabled protocol ieee
  Root ID    Priority    32788
             Address     aabb.cc00.3000
             Cost        200
             Port        1 (Ethernet0/0)
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

  Bridge ID  Priority    32788  (priority 32768 sys-id-ext 20)
             Address     aabb.cc00.7000
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
             Aging Time  300 sec

Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- --------------------------------
Et0/0               Root FWD 100       128.1    P2p 
Et0/1               Altn BLK 100       128.2    P2p 
Et0/3               Desg FWD 100       128.4    P2p 
```

CF stp.pcap