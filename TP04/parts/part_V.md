### 🌞 Sur le bastion, installer un serveur NTP

```bash
# Please consider joining the pool (https://www.pool.ntp.org/join.html).
server 0.fr.pool.ntp.org
server 1.fr.pool.ntp.org
server 2.fr.pool.ntp.org
server 3.fr.pool.ntp.org
```

```bash
# Allow NTP client access from local network.
allow 10.3.30.0/24
```

```bash
#On voit les serveurs du pool europe France
[admuser@node1 ~]$ chronyc sources -v

  .-- Source mode  '^' = server, '=' = peer, '#' = local clock.
 / .- Source state '*' = current best, '+' = combined, '-' = not combined,
| /             'x' = may be in error, '~' = too variable, '?' = unusable.
||                                                 .- xxxx [ yyyy ] +/- zzzz
||      Reachability register (octal) -.           |  xxxx = adjusted offset,
||      Log2(Polling interval) --.      |          |  yyyy = measured offset,
||                                \     |          |  zzzz = estimated error.
||                                 |    |           \
MS Name/IP address         Stratum Poll Reach LastRx Last sample               
===============================================================================
^? 27.ip-51-68-44.eu             3   6     1    47   +352us[ +352us] +/-   18ms
^? router-ix5.servme.network     3   6     1    48    -26ms[  -26ms] +/-  111ms
^? meshflow.net                  2   6     1    48   +574us[ +574us] +/-   18ms
^? ntp.univ-angers.fr            2   6     1    47   +828us[ +828us] +/-   46ms
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
19999                      ALLOW       Anywhere                  
123                        ALLOW       Anywhere                  
SSH (v6)                   ALLOW       Anywhere (v6)             
ff02::fb mDNS              ALLOW       Anywhere (v6)             
22/tcp (v6)                ALLOW       Anywhere (v6)             
67/udp (v6)                ALLOW       Anywhere (v6)             
19999 (v6)                 ALLOW       Anywhere (v6)             
123 (v6)                   ALLOW       Anywhere (v6)
```

### 🌞 Sur r1 et r2

```bash
- name: Configurer le client NTP sur r1 et r2
  hosts:
    - r1
    - r2
  gather_facts: no
  tasks:
    - name: Configurer bastion comme serveur NTP
      cisco.ios.ios_config:
        lines:
          - ntp server 10.3.30.100
        save_when: always
```

```bash
R1#show ntp status 
Clock is synchronized, stratum 4, reference is 10.3.30.100    
nominal freq is 250.0000 Hz, actual freq is 250.0000 Hz, precision is 2**18
ntp uptime is 5600 (1/100 of seconds), resolution is 4000
reference time is EB916D02.BC627B6A (18:46:26.735 UTC Fri Mar 28 2025)
clock offset is -1.0718 msec, root delay is 40.49 msec
root dispersion is 3943.01 msec, peer dispersion is 187.57 msec
loopfilter state is 'CTRL' (Normal Controlled Loop), drift is 0.000000000 s/s
system poll interval is 64, last update was 51 sec ago.
```

```bash
R1#show ntp associations 

  address         ref clock       st   when   poll reach  delay  offset   disp
*~10.3.30.100     51.195.104.188   3      8     64     3  1.627  -1.071 63.199
 * sys.peer, # selected, + candidate, - outlyer, x falseticker, ~ configured
```
