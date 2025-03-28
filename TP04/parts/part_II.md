### 🌞 Config réseau

```bash
DEVICE=ens19
NAME=LAN

ONBOOT=yes
#BOOTPROTO=dhcp

IPADDR=10.3.30.100
NETMASK=252.255.255.0
DNS1=1.1.1.1
GATEWAY=10.3.30.254
```
```bash
3: ens19: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether bc:24:11:ef:3e:ff brd ff:ff:ff:ff:ff:ff
    altname enp0s19
    inet 10.3.30.100/24 brd 10.3.30.255 scope global noprefixroute ens19
       valid_lft forever preferred_lft forever
    inet6 fe80::be24:11ff:feef:3eff/64 scope link 
       valid_lft forever preferred_lft forever
```

### 🌞 Serveur SSH

```bash
[admuser@node1 ~]$ systemctl status sshd
● sshd.service - OpenSSH server daemon
     Loaded: loaded (/usr/lib/systemd/system/sshd.service; enabled; preset: enabled)
     Active: active (running) since Thu 2025-03-27 12:46:45 CET; 1h 49min ago
       Docs: man:sshd(8)
             man:sshd_config(5)
   Main PID: 731 (sshd)
      Tasks: 1 (limit: 23148)
     Memory: 6.1M
        CPU: 162ms
     CGroup: /system.slice/sshd.service
             └─731 "sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups"
```

```bash
[admuser@node1 ~]$ ss | grep ssh
tcp   ESTAB  0      88                      172.16.0.50:ssh       10.0.0.7:56765
```

```bash
To                         Action      From
--                         ------      ----
SSH                        ALLOW       Anywhere                  
224.0.0.251 mDNS           ALLOW       Anywhere                         
22/tcp                     ALLOW       Anywhere                  
SSH (v6)                   ALLOW       Anywhere (v6)             
ff02::fb mDNS              ALLOW       Anywhere (v6)             
22/tcp (v6)                ALLOW       Anywhere (v6)             
```

### 🌞 Fichier SSH config

```bash
lucas@air-de-lucas .ssh % cat config  
Host bastion
  Hostname 172.16.0.50
  User admuser 
  IdentityFile /Users/lucas/.ssh/id_rsa
```

### 🌞 Proof !

```bash
lucas@air-de-lucas .ssh % ssh bastion -v
OpenSSH_9.7p1, LibreSSL 3.3.6
debug1: Reading configuration data /Users/lucas/.ssh/config
debug1: /Users/lucas/.ssh/config line 1: Applying options for bastion
debug1: Reading configuration data /etc/ssh/ssh_config
debug1: /etc/ssh/ssh_config line 21: include /etc/ssh/ssh_config.d/* matched no files
debug1: /etc/ssh/ssh_config line 54: Applying options for *
debug1: Authenticator provider $SSH_SK_PROVIDER did not resolve; disabling
debug1: Connecting to 172.16.0.50 [172.16.0.50] port 22.
debug1: Connection established.
debug1: identity file /Users/lucas/.ssh/id_rsa type -1
debug1: identity file /Users/lucas/.ssh/id_rsa-cert type -1
debug1: Local version string SSH-2.0-OpenSSH_9.7
debug1: Remote protocol version 2.0, remote software version OpenSSH_8.7
debug1: compat_banner: match: OpenSSH_8.7 pat OpenSSH* compat 0x04000000
debug1: Authenticating to 172.16.0.50:22 as 'admuser'
debug1: load_hostkeys: fopen /Users/lucas/.ssh/known_hosts2: No such file or directory
debug1: load_hostkeys: fopen /etc/ssh/ssh_known_hosts: No such file or directory
debug1: load_hostkeys: fopen /etc/ssh/ssh_known_hosts2: No such file or directory
debug1: SSH2_MSG_KEXINIT sent
debug1: SSH2_MSG_KEXINIT received
debug1: kex: algorithm: curve25519-sha256
debug1: kex: host key algorithm: ssh-ed25519
debug1: kex: server->client cipher: chacha20-poly1305@openssh.com MAC: <implicit> compression: none
debug1: kex: client->server cipher: chacha20-poly1305@openssh.com MAC: <implicit> compression: none
debug1: expecting SSH2_MSG_KEX_ECDH_REPLY
debug1: SSH2_MSG_KEX_ECDH_REPLY received
debug1: Server host key: ssh-ed25519 SHA256:0+sXnAjTOv+eKj+6nagcCXNd3fGTRH77Elo2qCgeiug
debug1: load_hostkeys: fopen /Users/lucas/.ssh/known_hosts2: No such file or directory
debug1: load_hostkeys: fopen /etc/ssh/ssh_known_hosts: No such file or directory
debug1: load_hostkeys: fopen /etc/ssh/ssh_known_hosts2: No such file or directory
debug1: Host '172.16.0.50' is known and matches the ED25519 host key.
debug1: Found key in /Users/lucas/.ssh/known_hosts:8
debug1: ssh_packet_send2_wrapped: resetting send seqnr 3
debug1: rekey out after 134217728 blocks
debug1: SSH2_MSG_NEWKEYS sent
debug1: expecting SSH2_MSG_NEWKEYS
debug1: ssh_packet_read_poll2: resetting read seqnr 3
debug1: SSH2_MSG_NEWKEYS received
debug1: rekey in after 134217728 blocks
debug1: SSH2_MSG_EXT_INFO received
debug1: kex_ext_info_client_parse: server-sig-algs=<ssh-ed25519,sk-ssh-ed25519@openssh.com,ssh-rsa,rsa-sha2-256,rsa-sha2-512,ssh-dss,ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,ecdsa-sha2-nistp521,sk-ecdsa-sha2-nistp256@openssh.com,webauthn-sk-ecdsa-sha2-nistp256@openssh.com>
debug1: SSH2_MSG_SERVICE_ACCEPT received
debug1: Authentications that can continue: publickey,gssapi-keyex,gssapi-with-mic,password
debug1: Next authentication method: publickey
debug1: get_agent_identities: bound agent to hostkey
debug1: get_agent_identities: ssh_fetch_identitylist: agent contains no identities
debug1: Will attempt key: /Users/lucas/.ssh/id_rsa  explicit
debug1: Trying private key: /Users/lucas/.ssh/id_rsa
Authenticated to 172.16.0.50 ([172.16.0.50]:22) using "publickey".
debug1: channel 0: new session [client-session] (inactive timeout: 0)
debug1: Requesting no-more-sessions@openssh.com
debug1: Entering interactive session.
debug1: pledge: filesystem
debug1: client_input_global_request: rtype hostkeys-00@openssh.com want_reply 0
debug1: client_input_hostkeys: searching /Users/lucas/.ssh/known_hosts for 172.16.0.50 / (none)
debug1: client_input_hostkeys: searching /Users/lucas/.ssh/known_hosts2 for 172.16.0.50 / (none)
debug1: client_input_hostkeys: hostkeys file /Users/lucas/.ssh/known_hosts2 does not exist
debug1: client_input_hostkeys: host key found matching a different name/address, skipping UserKnownHostsFile update
debug1: Remote: /home/admuser/.ssh/authorized_keys:2: key options: agent-forwarding port-forwarding pty user-rc x11-forwarding
debug1: Sending environment.
debug1: channel 0: setting env LANG = "en_FR.UTF-8"
debug1: pledge: fork
Last login: Thu Mar 27 15:03:09 2025 from 10.0.0.7
[admuser@node1 ~]$ 
```

### 🌞 Mettre à jour la clé publique déposées sur les routeurs

```bash
R1(config)#ip ssh pubkey-chain 
R1(conf-ssh-pubkey)#username admin
R1(conf-ssh-pubkey-user)#no key-hash 
R1(conf-ssh-pubkey-user)#key-string 
R1(conf-ssh-pubkey-data)#$BAAACAQDFZuh7daQ7w03saIv0+QIYpJaT9OniwpXa+O0cPDer  
R1(conf-ssh-pubkey-data)#$kaz/v5xL90U75fCWZ6YA9U3KuO925HoLCrtSn1mNdcJdE+rIP  
R1(conf-ssh-pubkey-data)#$xE6XZ95gPfRY6gxd7Byqi4IoicP3qm1sBIpxGwP2u+WF1idi/  
R1(conf-ssh-pubkey-data)#$OCClIWAYjvLb8vGAkgkjQC9S4j4wsIWwMdUtvWDlbrMcPJcr2  
R1(conf-ssh-pubkey-data)#$bxlOIhmHWuc0Wav3fj6n112655Hei9Czd+skjqPSesZTz+myQ  
R1(conf-ssh-pubkey-data)#$0aTwEexJ1Si7XzRrprBXNShEL/T15Vz4uyOzatSG4JOq4xdR1  
R1(conf-ssh-pubkey-data)#$AA+qqP6TQvSdps3v3EE4H9OVWHhsiQWrkfar6HBqpMELHOzM0  
R1(conf-ssh-pubkey-data)#$gYKQf0uvI683C/Z9cK+9AcUp98A4ochZ+J2pAXGegv7VtYU9D  
R1(conf-ssh-pubkey-data)#$2YFgQVxpJ1B/jn7cQp1QTUTXoIfmhSIXnMQ4Kb8yFJ9ZIE1YB  
R1(conf-ssh-pubkey-data)#mw== Generated By Termius
R1(conf-ssh-pubkey-data)#exit
#pareil sur R2
```

### 🌞 Se connecter aux routeurs avec un rebond sur le bastion

```bash
lucas@air-de-lucas .ssh % ssh -J bastion 10.3.30.253 \
  -o KexAlgorithms=+diffie-hellman-group1-sha1 \
  -o PubkeyAcceptedAlgorithms=+ssh-rsa \
  -o HostkeyAlgorithms=+ssh-rsa \
  -o Ciphers=+aes256-cbc -l admin -v 
OpenSSH_9.7p1, LibreSSL 3.3.6
debug1: Reading configuration data /Users/lucas/.ssh/config
debug1: Reading configuration data /etc/ssh/ssh_config
debug1: /etc/ssh/ssh_config line 21: include /etc/ssh/ssh_config.d/* matched no files
debug1: /etc/ssh/ssh_config line 54: Applying options for *
debug1: Setting implicit ProxyCommand from ProxyJump: ssh -v -W '[%h]:%p' bastion
debug1: Authenticator provider $SSH_SK_PROVIDER did not resolve; disabling
debug1: Executing proxy command: exec ssh -v -W '[10.3.30.253]:22' bastion
debug1: identity file /Users/lucas/.ssh/id_rsa type 0
debug1: identity file /Users/lucas/.ssh/id_rsa-cert type -1
debug1: identity file /Users/lucas/.ssh/id_ecdsa type -1
debug1: identity file /Users/lucas/.ssh/id_ecdsa-cert type -1
debug1: identity file /Users/lucas/.ssh/id_ecdsa_sk type -1
debug1: identity file /Users/lucas/.ssh/id_ecdsa_sk-cert type -1
debug1: identity file /Users/lucas/.ssh/id_ed25519 type -1
debug1: identity file /Users/lucas/.ssh/id_ed25519-cert type -1
debug1: identity file /Users/lucas/.ssh/id_ed25519_sk type -1
debug1: identity file /Users/lucas/.ssh/id_ed25519_sk-cert type -1
debug1: identity file /Users/lucas/.ssh/id_xmss type -1
debug1: identity file /Users/lucas/.ssh/id_xmss-cert type -1
debug1: identity file /Users/lucas/.ssh/id_dsa type -1
debug1: identity file /Users/lucas/.ssh/id_dsa-cert type -1
debug1: Local version string SSH-2.0-OpenSSH_9.7
OpenSSH_9.7p1, LibreSSL 3.3.6
debug1: Reading configuration data /Users/lucas/.ssh/config
debug1: /Users/lucas/.ssh/config line 1: Applying options for bastion
debug1: Reading configuration data /etc/ssh/ssh_config
debug1: /etc/ssh/ssh_config line 21: include /etc/ssh/ssh_config.d/* matched no files
debug1: /etc/ssh/ssh_config line 54: Applying options for *
debug1: Authenticator provider $SSH_SK_PROVIDER did not resolve; disabling
debug1: Connecting to 172.16.0.50 [172.16.0.50] port 22.
debug1: Connection established.
debug1: identity file /Users/lucas/.ssh/id_rsa type 0
debug1: identity file /Users/lucas/.ssh/id_rsa-cert type -1
debug1: Local version string SSH-2.0-OpenSSH_9.7
debug1: Remote protocol version 2.0, remote software version OpenSSH_8.7
debug1: compat_banner: match: OpenSSH_8.7 pat OpenSSH* compat 0x04000000
debug1: Authenticating to 172.16.0.50:22 as 'admuser'
debug1: load_hostkeys: fopen /Users/lucas/.ssh/known_hosts2: No such file or directory
debug1: load_hostkeys: fopen /etc/ssh/ssh_known_hosts: No such file or directory
debug1: load_hostkeys: fopen /etc/ssh/ssh_known_hosts2: No such file or directory
debug1: SSH2_MSG_KEXINIT sent
debug1: SSH2_MSG_KEXINIT received
debug1: kex: algorithm: curve25519-sha256
debug1: kex: host key algorithm: ssh-ed25519
debug1: kex: server->client cipher: chacha20-poly1305@openssh.com MAC: <implicit> compression: none
debug1: kex: client->server cipher: chacha20-poly1305@openssh.com MAC: <implicit> compression: none
debug1: expecting SSH2_MSG_KEX_ECDH_REPLY
debug1: SSH2_MSG_KEX_ECDH_REPLY received
debug1: Server host key: ssh-ed25519 SHA256:0+sXnAjTOv+eKj+6nagcCXNd3fGTRH77Elo2qCgeiug
debug1: load_hostkeys: fopen /Users/lucas/.ssh/known_hosts2: No such file or directory
debug1: load_hostkeys: fopen /etc/ssh/ssh_known_hosts: No such file or directory
debug1: load_hostkeys: fopen /etc/ssh/ssh_known_hosts2: No such file or directory
debug1: Host '172.16.0.50' is known and matches the ED25519 host key.
debug1: Found key in /Users/lucas/.ssh/known_hosts:8
debug1: ssh_packet_send2_wrapped: resetting send seqnr 3
debug1: rekey out after 134217728 blocks
debug1: SSH2_MSG_NEWKEYS sent
debug1: expecting SSH2_MSG_NEWKEYS
debug1: ssh_packet_read_poll2: resetting read seqnr 3
debug1: SSH2_MSG_NEWKEYS received
debug1: rekey in after 134217728 blocks
debug1: SSH2_MSG_EXT_INFO received
debug1: kex_ext_info_client_parse: server-sig-algs=<ssh-ed25519,sk-ssh-ed25519@openssh.com,ssh-rsa,rsa-sha2-256,rsa-sha2-512,ssh-dss,ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,ecdsa-sha2-nistp521,sk-ecdsa-sha2-nistp256@openssh.com,webauthn-sk-ecdsa-sha2-nistp256@openssh.com>
debug1: SSH2_MSG_SERVICE_ACCEPT received
debug1: Authentications that can continue: publickey,gssapi-keyex,gssapi-with-mic,password
debug1: Next authentication method: publickey
debug1: get_agent_identities: bound agent to hostkey
debug1: get_agent_identities: ssh_fetch_identitylist: agent contains no identities
debug1: Will attempt key: /Users/lucas/.ssh/id_rsa RSA SHA256:hn4tWxuho8ZfYo2PXvbk5FIIyFx2IV8T1WNZcsbZgj0 explicit
debug1: Offering public key: /Users/lucas/.ssh/id_rsa RSA SHA256:hn4tWxuho8ZfYo2PXvbk5FIIyFx2IV8T1WNZcsbZgj0 explicit
debug1: Server accepts key: /Users/lucas/.ssh/id_rsa RSA SHA256:hn4tWxuho8ZfYo2PXvbk5FIIyFx2IV8T1WNZcsbZgj0 explicit
Authenticated to 172.16.0.50 ([172.16.0.50]:22) using "publickey".
debug1: channel_connect_stdio_fwd: 10.3.30.253:22
debug1: channel 0: new stdio-forward [stdio-forward] (inactive timeout: 0)
debug1: Requesting no-more-sessions@openssh.com
debug1: Entering interactive session.
debug1: pledge: filesystem
debug1: client_input_global_request: rtype hostkeys-00@openssh.com want_reply 0
debug1: client_input_hostkeys: searching /Users/lucas/.ssh/known_hosts for 172.16.0.50 / (none)
debug1: client_input_hostkeys: searching /Users/lucas/.ssh/known_hosts2 for 172.16.0.50 / (none)
debug1: client_input_hostkeys: hostkeys file /Users/lucas/.ssh/known_hosts2 does not exist
debug1: client_input_hostkeys: host key found matching a different name/address, skipping UserKnownHostsFile update
debug1: pledge: fork
debug1: Remote: /home/admuser/.ssh/authorized_keys:6: key options: agent-forwarding port-forwarding pty user-rc x11-forwarding
debug1: Remote: /home/admuser/.ssh/authorized_keys:6: key options: agent-forwarding port-forwarding pty user-rc x11-forwarding
debug1: Remote protocol version 2.0, remote software version Cisco-1.25
debug1: compat_banner: match: Cisco-1.25 pat Cisco-1.* compat 0x60000000
debug1: Authenticating to 10.3.30.253:22 as 'admin'
debug1: load_hostkeys: fopen /Users/lucas/.ssh/known_hosts2: No such file or directory
debug1: load_hostkeys: fopen /etc/ssh/ssh_known_hosts: No such file or directory
debug1: load_hostkeys: fopen /etc/ssh/ssh_known_hosts2: No such file or directory
debug1: SSH2_MSG_KEXINIT sent
debug1: SSH2_MSG_KEXINIT received
debug1: kex: algorithm: diffie-hellman-group1-sha1
debug1: kex: host key algorithm: ssh-rsa
debug1: kex: server->client cipher: aes256-cbc MAC: hmac-sha1 compression: none
debug1: kex: client->server cipher: aes256-cbc MAC: hmac-sha1 compression: none
debug1: expecting SSH2_MSG_KEX_ECDH_REPLY
debug1: SSH2_MSG_KEX_ECDH_REPLY received
debug1: Server host key: ssh-rsa SHA256:EtbcvKpAQKPp/VO80E2AI3PCwdHz+vAAF8rK5nYoll8
debug1: load_hostkeys: fopen /Users/lucas/.ssh/known_hosts2: No such file or directory
debug1: load_hostkeys: fopen /etc/ssh/ssh_known_hosts: No such file or directory
debug1: load_hostkeys: fopen /etc/ssh/ssh_known_hosts2: No such file or directory
debug1: Host '10.3.30.253' is known and matches the RSA host key.
debug1: Found key in /Users/lucas/.ssh/known_hosts:11
debug1: rekey out after 4294967296 blocks
debug1: SSH2_MSG_NEWKEYS sent
debug1: expecting SSH2_MSG_NEWKEYS
debug1: SSH2_MSG_NEWKEYS received
debug1: rekey in after 4294967296 blocks
debug1: SSH2_MSG_SERVICE_ACCEPT received
debug1: Authentications that can continue: publickey,keyboard-interactive,password
debug1: Next authentication method: publickey
debug1: get_agent_identities: bound agent to hostkey
debug1: get_agent_identities: ssh_fetch_identitylist: agent contains no identities
debug1: Will attempt key: /Users/lucas/.ssh/id_rsa RSA SHA256:hn4tWxuho8ZfYo2PXvbk5FIIyFx2IV8T1WNZcsbZgj0
debug1: Will attempt key: /Users/lucas/.ssh/id_ecdsa 
debug1: Will attempt key: /Users/lucas/.ssh/id_ecdsa_sk 
debug1: Will attempt key: /Users/lucas/.ssh/id_ed25519 
debug1: Will attempt key: /Users/lucas/.ssh/id_ed25519_sk 
debug1: Will attempt key: /Users/lucas/.ssh/id_xmss 
debug1: Will attempt key: /Users/lucas/.ssh/id_dsa 
debug1: Offering public key: /Users/lucas/.ssh/id_rsa RSA SHA256:hn4tWxuho8ZfYo2PXvbk5FIIyFx2IV8T1WNZcsbZgj0
debug1: Server accepts key: /Users/lucas/.ssh/id_rsa RSA SHA256:hn4tWxuho8ZfYo2PXvbk5FIIyFx2IV8T1WNZcsbZgj0
Authenticated to 10.3.30.253 (via proxy) using "publickey".
debug1: channel 0: new session [client-session] (inactive timeout: 0)
debug1: Entering interactive session.
debug1: pledge: filesystem
debug1: Sending environment.
debug1: channel 0: setting env LANG = "en_FR.UTF-8"
R2#
```
### 🌞 Modifier votre fichier SSH config

```bash
lucas@air-de-lucas .ssh % cat config 

Host bastion
  Hostname 172.16.0.50
  User admuser 
  IdentityFile /Users/lucas/.ssh/id_rsa

Host r1
  ProxyJump bastion
  HostName 10.3.30.252
  User admin
  IdentityFile /Users/lucas/.ssh/id_rsa
  KexAlgorithms +diffie-hellman-group1-sha1
  PubkeyAcceptedAlgorithms +ssh-rsa
  HostkeyAlgorithms +ssh-rsa
  Ciphers +aes256-cbc
  MACs hmac-sha1,hmac-md5

Host r2
  ProxyJump bastion   
  HostName 10.3.30.253
  User admin
  IdentityFile /Users/lucas/.ssh/id_rsa
  KexAlgorithms +diffie-hellman-group1-sha1
  PubkeyAcceptedAlgorithms +ssh-rsa
  HostkeyAlgorithms +ssh-rsa
  Ciphers +aes256-cbc
  MACs hmac-sha1,hmac-md5
```

### 🌞 Proof !

```bash
lucas@air-de-lucas .ssh % ssh r1 -v
OpenSSH_9.7p1, LibreSSL 3.3.6
debug1: Reading configuration data /Users/lucas/.ssh/config
debug1: /Users/lucas/.ssh/config line 7: Applying options for r1
debug1: Reading configuration data /etc/ssh/ssh_config
debug1: /etc/ssh/ssh_config line 21: include /etc/ssh/ssh_config.d/* matched no files
debug1: /etc/ssh/ssh_config line 54: Applying options for *
debug1: Setting implicit ProxyCommand from ProxyJump: ssh -v -W '[%h]:%p' bastion
debug1: Authenticator provider $SSH_SK_PROVIDER did not resolve; disabling
debug1: Executing proxy command: exec ssh -v -W '[10.3.30.252]:22' bastion
debug1: identity file /Users/lucas/.ssh/id_rsa type 0
debug1: identity file /Users/lucas/.ssh/id_rsa-cert type -1
debug1: Local version string SSH-2.0-OpenSSH_9.7
OpenSSH_9.7p1, LibreSSL 3.3.6
debug1: Reading configuration data /Users/lucas/.ssh/config
debug1: /Users/lucas/.ssh/config line 2: Applying options for bastion
debug1: Reading configuration data /etc/ssh/ssh_config
debug1: /etc/ssh/ssh_config line 21: include /etc/ssh/ssh_config.d/* matched no files
debug1: /etc/ssh/ssh_config line 54: Applying options for *
debug1: Authenticator provider $SSH_SK_PROVIDER did not resolve; disabling
debug1: Connecting to 172.16.0.50 [172.16.0.50] port 22.
debug1: Connection established.
debug1: identity file /Users/lucas/.ssh/id_rsa type 0
debug1: identity file /Users/lucas/.ssh/id_rsa-cert type -1
debug1: Local version string SSH-2.0-OpenSSH_9.7
debug1: Remote protocol version 2.0, remote software version OpenSSH_8.7
debug1: compat_banner: match: OpenSSH_8.7 pat OpenSSH* compat 0x04000000
debug1: Authenticating to 172.16.0.50:22 as 'admuser'
debug1: load_hostkeys: fopen /Users/lucas/.ssh/known_hosts2: No such file or directory
debug1: load_hostkeys: fopen /etc/ssh/ssh_known_hosts: No such file or directory
debug1: load_hostkeys: fopen /etc/ssh/ssh_known_hosts2: No such file or directory
debug1: SSH2_MSG_KEXINIT sent
debug1: SSH2_MSG_KEXINIT received
debug1: kex: algorithm: curve25519-sha256
debug1: kex: host key algorithm: ssh-ed25519
debug1: kex: server->client cipher: chacha20-poly1305@openssh.com MAC: <implicit> compression: none
debug1: kex: client->server cipher: chacha20-poly1305@openssh.com MAC: <implicit> compression: none
debug1: expecting SSH2_MSG_KEX_ECDH_REPLY
debug1: SSH2_MSG_KEX_ECDH_REPLY received
debug1: Server host key: ssh-ed25519 SHA256:0+sXnAjTOv+eKj+6nagcCXNd3fGTRH77Elo2qCgeiug
debug1: load_hostkeys: fopen /Users/lucas/.ssh/known_hosts2: No such file or directory
debug1: load_hostkeys: fopen /etc/ssh/ssh_known_hosts: No such file or directory
debug1: load_hostkeys: fopen /etc/ssh/ssh_known_hosts2: No such file or directory
debug1: Host '172.16.0.50' is known and matches the ED25519 host key.
debug1: Found key in /Users/lucas/.ssh/known_hosts:8
debug1: ssh_packet_send2_wrapped: resetting send seqnr 3
debug1: rekey out after 134217728 blocks
debug1: SSH2_MSG_NEWKEYS sent
debug1: expecting SSH2_MSG_NEWKEYS
debug1: ssh_packet_read_poll2: resetting read seqnr 3
debug1: SSH2_MSG_NEWKEYS received
debug1: rekey in after 134217728 blocks
debug1: SSH2_MSG_EXT_INFO received
debug1: kex_ext_info_client_parse: server-sig-algs=<ssh-ed25519,sk-ssh-ed25519@openssh.com,ssh-rsa,rsa-sha2-256,rsa-sha2-512,ssh-dss,ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,ecdsa-sha2-nistp521,sk-ecdsa-sha2-nistp256@openssh.com,webauthn-sk-ecdsa-sha2-nistp256@openssh.com>
debug1: SSH2_MSG_SERVICE_ACCEPT received
debug1: Authentications that can continue: publickey,gssapi-keyex,gssapi-with-mic,password
debug1: Next authentication method: publickey
debug1: get_agent_identities: bound agent to hostkey
debug1: get_agent_identities: ssh_fetch_identitylist: agent contains no identities
debug1: Will attempt key: /Users/lucas/.ssh/id_rsa RSA SHA256:hn4tWxuho8ZfYo2PXvbk5FIIyFx2IV8T1WNZcsbZgj0 explicit
debug1: Offering public key: /Users/lucas/.ssh/id_rsa RSA SHA256:hn4tWxuho8ZfYo2PXvbk5FIIyFx2IV8T1WNZcsbZgj0 explicit
debug1: Server accepts key: /Users/lucas/.ssh/id_rsa RSA SHA256:hn4tWxuho8ZfYo2PXvbk5FIIyFx2IV8T1WNZcsbZgj0 explicit
Authenticated to 172.16.0.50 ([172.16.0.50]:22) using "publickey".
debug1: channel_connect_stdio_fwd: 10.3.30.252:22
debug1: channel 0: new stdio-forward [stdio-forward] (inactive timeout: 0)
debug1: Requesting no-more-sessions@openssh.com
debug1: Entering interactive session.
debug1: pledge: filesystem
debug1: client_input_global_request: rtype hostkeys-00@openssh.com want_reply 0
debug1: client_input_hostkeys: searching /Users/lucas/.ssh/known_hosts for 172.16.0.50 / (none)
debug1: client_input_hostkeys: searching /Users/lucas/.ssh/known_hosts2 for 172.16.0.50 / (none)
debug1: client_input_hostkeys: hostkeys file /Users/lucas/.ssh/known_hosts2 does not exist
debug1: client_input_hostkeys: host key found matching a different name/address, skipping UserKnownHostsFile update
debug1: pledge: fork
debug1: Remote: /home/admuser/.ssh/authorized_keys:6: key options: agent-forwarding port-forwarding pty user-rc x11-forwarding
debug1: Remote: /home/admuser/.ssh/authorized_keys:6: key options: agent-forwarding port-forwarding pty user-rc x11-forwarding
debug1: Remote protocol version 2.0, remote software version Cisco-1.25
debug1: compat_banner: match: Cisco-1.25 pat Cisco-1.* compat 0x60000000
debug1: Authenticating to 10.3.30.252:22 as 'admin'
debug1: load_hostkeys: fopen /Users/lucas/.ssh/known_hosts2: No such file or directory
debug1: load_hostkeys: fopen /etc/ssh/ssh_known_hosts: No such file or directory
debug1: load_hostkeys: fopen /etc/ssh/ssh_known_hosts2: No such file or directory
debug1: SSH2_MSG_KEXINIT sent
debug1: SSH2_MSG_KEXINIT received
debug1: kex: algorithm: diffie-hellman-group1-sha1
debug1: kex: host key algorithm: ssh-rsa
debug1: kex: server->client cipher: aes256-cbc MAC: hmac-sha1 compression: none
debug1: kex: client->server cipher: aes256-cbc MAC: hmac-sha1 compression: none
debug1: expecting SSH2_MSG_KEX_ECDH_REPLY
debug1: SSH2_MSG_KEX_ECDH_REPLY received
debug1: Server host key: ssh-rsa SHA256:ZeoK7vUTiPMLiEOmt/yZLdOqYhtoi3UpNVWDnIxSiRU
debug1: load_hostkeys: fopen /Users/lucas/.ssh/known_hosts2: No such file or directory
debug1: load_hostkeys: fopen /etc/ssh/ssh_known_hosts: No such file or directory
debug1: load_hostkeys: fopen /etc/ssh/ssh_known_hosts2: No such file or directory
debug1: Host '10.3.30.252' is known and matches the RSA host key.
debug1: Found key in /Users/lucas/.ssh/known_hosts:10
debug1: rekey out after 4294967296 blocks
debug1: SSH2_MSG_NEWKEYS sent
debug1: expecting SSH2_MSG_NEWKEYS
debug1: SSH2_MSG_NEWKEYS received
debug1: rekey in after 4294967296 blocks
debug1: SSH2_MSG_SERVICE_ACCEPT received
debug1: Authentications that can continue: publickey,keyboard-interactive,password
debug1: Next authentication method: publickey
debug1: get_agent_identities: bound agent to hostkey
debug1: get_agent_identities: ssh_fetch_identitylist: agent contains no identities
debug1: Will attempt key: /Users/lucas/.ssh/id_rsa RSA SHA256:hn4tWxuho8ZfYo2PXvbk5FIIyFx2IV8T1WNZcsbZgj0 explicit
debug1: Offering public key: /Users/lucas/.ssh/id_rsa RSA SHA256:hn4tWxuho8ZfYo2PXvbk5FIIyFx2IV8T1WNZcsbZgj0 explicit
debug1: Server accepts key: /Users/lucas/.ssh/id_rsa RSA SHA256:hn4tWxuho8ZfYo2PXvbk5FIIyFx2IV8T1WNZcsbZgj0 explicit
Authenticated to 10.3.30.252 (via proxy) using "publickey".
debug1: channel 0: new session [client-session] (inactive timeout: 0)
debug1: Entering interactive session.
debug1: pledge: filesystem
debug1: Sending environment.
debug1: channel 0: setting env LANG = "en_FR.UTF-8"
R1#
```
