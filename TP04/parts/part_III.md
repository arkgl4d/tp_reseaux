### 🌞 Activer le service SNMP

```bash
snmp-server community tp4 ro
snmp-server host 10.3.30.100 version 2c tp4
#Sur R1 et R2
```

### 🌞 Vérifier l'état du service SNMP

```bash
R1#show snmp community 

Community name: ILMI
Community Index: ILMI
Community SecurityName: ILMI
storage-type: read-only  active


Community name: tp4
Community Index: tp4
Community SecurityName: tp4
storage-type: nonvolatile        active
```

```bash
R2#show snmp community 

Community name: ILMI
Community Index: ILMI
Community SecurityName: ILMI
storage-type: read-only  active


Community name: tp4
Community Index: tp4
Community SecurityName: tp4
storage-type: nonvolatile        active
```

### 🌞 Sur votre bastion

```bash
sudo dnf install net-snmp net-snmp-utils
```

```bash
[admuser@node1 ~]$ snmpwalk -v2c -c tp4 10.3.30.254
SNMPv2-MIB::sysDescr.0 = STRING: Cisco IOS Software, 7200 Software (C7200-ADVENTERPRISEK9-M), Version 15.2(4)S6, RELEASE SOFTWARE (fc1)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2014 by Cisco Systems, Inc.
Compiled Fri 08-Aug-14 04:05 by prod_rel_team
SNMPv2-MIB::sysObjectID.0 = OID: SNMPv2-SMI::enterprises.9.1.222
DISMAN-EVENT-MIB::sysUpTimeInstance = Timeticks: (1637727) 4:32:57.27
SNMPv2-MIB::sysContact.0 = STRING: 
SNMPv2-MIB::sysName.0 = STRING: R2.ynov.com
SNMPv2-MIB::sysLocation.0 = STRING: 
SNMPv2-MIB::sysServices.0 = INTEGER: 78
SNMPv2-MIB::sysORLastChange.0 = Timeticks: (0) 0:00:00.00
IF-MIB::ifNumber.0 = INTEGER: 7
IF-MIB::ifIndex.1 = INTEGER: 1
IF-MIB::ifIndex.2 = INTEGER: 2
IF-MIB::ifIndex.3 = INTEGER: 3
IF-MIB::ifIndex.4 = INTEGER: 4
IF-MIB::ifIndex.5 = INTEGER: 5
IF-MIB::ifIndex.6 = INTEGER: 6
IF-MIB::ifIndex.7 = INTEGER: 7
IF-MIB::ifDescr.1 = STRING: FastEthernet0/0
...
```

### 🌞 Sur votre bastion

```bash
snmpwalk -v2c -c tp4 10.3.30.254 IF-MIB::ifDescr
IF-MIB::ifDescr.1 = STRING: FastEthernet0/0
IF-MIB::ifDescr.2 = STRING: FastEthernet1/0
IF-MIB::ifDescr.3 = STRING: FastEthernet2/0
IF-MIB::ifDescr.4 = STRING: Null0
IF-MIB::ifDescr.5 = STRING: FastEthernet0/0.10
IF-MIB::ifDescr.6 = STRING: FastEthernet0/0.20
IF-MIB::ifDescr.7 = STRING: FastEthernet0/0.30
```

```bash
snmpwalk -v2c -c tp4 10.3.30.254 CISCO-REMOTE-ACCESS-MONITOR-MIB::*
``` 


### 🌞 Installer Netdata sur votre bastion

```bash
[admuser@node1 ~]$ sudo systemctl enable --now netdata
[admuser@node1 ~]$ sudo systemctl status netdata
● netdata.service - Netdata, X-Ray Vision for your infrastructure!
     Loaded: loaded (/usr/lib/systemd/system/netdata.service; enabled; preset: enabled)
     Active: active (running) since Fri 2025-03-28 15:38:44 CET; 15s ago
    Process: 5416 ExecStartPre=/bin/mkdir -p /var/cache/netdata (code=exited, status=0/SUCCESS)
    Process: 5418 ExecStartPre=/bin/chown -R netdata /var/cache/netdata (code=exited, status=0/SUCCESS)
   Main PID: 5420 (netdata)
      Tasks: 99 (limit: 23147)
     Memory: 120.5M
        CPU: 3.016s
     CGroup: /system.slice/netdata.service
             ├─5420 /usr/sbin/netdata -P /run/netdata/netdata.pid -D
             ├─5423 "spawn-plugins    " "  " "                        " "  "
             ├─5684 /usr/libexec/netdata/plugins.d/apps.plugin 1
             ├─5686 /usr/libexec/netdata/plugins.d/debugfs.plugin 1
             ├─5716 bash /usr/libexec/netdata/plugins.d/tc-qos-helper.sh 1
             ├─5723 /usr/libexec/netdata/plugins.d/network-viewer.plugin 1
             ├─5729 /usr/libexec/netdata/plugins.d/go.d.plugin 1
             ├─5731 /usr/libexec/netdata/plugins.d/ebpf.plugin 1
             ├─5733 "spawn-setns                                         " " "
             └─5740 /usr/libexec/netdata/plugins.d/systemd-journal.plugin 1
```



### 🌞 Visitez l'interface web de Netdata

```bash
[admuser@node1 netdata]$ curl http://172.16.0.50:19999
<!doctype html><html lang="en" dir="ltr"><head><meta charset="utf-8"/><title>Netdata</title><script>const CONFIG = {
      cache: {
        agentInfo: false,
        cloudToken: true,
        agentToken: true,
      }
    }

    // STATE MANAGEMENT ======================================================================== //
    const state = {
      loading: {
        spaces: false,
        rooms: false,
        claimingToken: false,
        claimingAgent: false
      },
      claim: {
        status: {},
        response: {},
        shouldClaim: false,
        step: 1,
        selectedSpaceIds: [],
        selectedRoomIds: [],
        privateKey: ""
      },
      cache: {
        spaces: undefined,
        rooms: {},
        claimingTokensPerSpace: {}
      }
    }

    const getSelectedRooms = state => {
      const spaceId = state.claim.selectedSpaceIds.length ? state.claim.selectedSpaceIds[0] : null;
      if (!spaceId) return [];
      if (state.claim.selectedRoomIds.length) {
        return state.cache?.rooms?.[spaceId]?.filter(({ id }) => state.claim.selectedRoomIds.includes(id)) || [];
      }
      return [];
    }

    const syncUI = () => {
      // Elements
      const splashMessage = document.getElementById("splashMessageContainer");
      const claiming = document.getElementById("claimingContentsContainer");
      const step1 = document.getElementById("connectionStep-1");
      const step2 = document.getElementById("connectionStep-2");
      const btnPrev = document.getElementById("btnConnectionStepPrev");
      const btnNext = document.getElementById("btnConnectionStepNext");
      const btnClaim = document.getElementById("btnClaim");
      const roomsSelector = document.getElementById("roomsSelector");
      const claimErrorMessage = document.getElementById("claimErrorMessage");

      // State
      const { spaces: spacesLoading, rooms: roomsLoading, claimingToken: claimingTokenLoading, claimingAgent: claimingAgentLoading } = state.loading;
      const { shouldClaim, step, selectedSpaceIds, selectedRoomIds, privateKey } = state.claim;
      const claimingTokenExists = state.claim.selectedSpaceIds.length ? !!state.cache.claimingTokensPerSpace[state.claim.selectedSpaceIds[0]] : false;

      splashMessage.style.display = !shouldClaim ? "initial" : "none";
      claiming.style.display = shouldClaim ? "initial" : "none";

      // Loading spaces
      if (step1) {
        const spacesLoader = step1.querySelector(".loader");
        if (spacesLoader) {
          spacesLoader.style.display = spacesLoading ? "initial" : "none";
        }
```

### 🌞 Ajouter la conf SNMP

```bash
[admuser@node1 ~]$ cat /etc/netdata/go.d/snmp.conf 
## All available configuration options, their descriptions and default values:
## https://github.com/netdata/netdata/tree/master/src/go/plugin/go.d/collector/snmp#readme

#jobs:
#  - name: switch
#    update_every: 10
#    hostname: "192.0.2.1"
#    community: public
#    options:
#      version: 2
#
jobs:
  - &anchor
    name: router
    update_every: 10
    hostname: "10.3.30.252"
    community: tp4
    options:
      version: 2
    charts:
      - id: "bandwidth_port1"
        title: "Switch Bandwidth for port 1"
        units: "kilobits/s"
        type: "area"
        family: "ports"
        dimensions:
          - name: "in"
            oid: "1.3.6.1.2.1.2.2.1.10.1"
            algorithm: "incremental"
            multiplier: 8
            divisor: 1000
          - name: "out"
            oid: "1.3.6.1.2.1.2.2.1.16.1"
            multiplier: -8
            divisor: 1000
  - <<: *anchor
    name: router2
    hostname: "10.3.30.253"
```