### 🌞 Créer un utilisateur

```bash
ip domain-name ynov.com
username admin privilege 15 secret 5 $1$duIS$X7OJLZwk79ebuze3bZ0bl0
enable secret 5 $1$duIS$X7OJLZwk79ebuze3bZ0bl0
crypto key generate rsa general-keys modulus 2048

ip ssh pubkey-chain
  username admin
  key-string
  #copier la clé publique générée par la commande fold sur la machine linux
```

### 🌞 Activer le serveur SSH

```bash
ip ssh version 2
ip ssh time-out 60
ip ssh authentication-retries 3

line vty 0 4
login local
transport input ssh
```

### 🌞 Prouvez que la connexion est fonctionnelle

```bash
[admuser@node1 ~]$ ssh -oKexAlgorithms=+diffie-hellman-group1-sha1 -oPubkeyAcceptedAlgorithms=+ssh-rsa -oHostkeyAlgorithms=+ssh-rsa -oCiphers=+aes256-cbc -i .ssh/id_rsa admin@10.3.30.252 -v
OpenSSH_8.7p1, OpenSSL 3.2.2 4 Jun 2024
debug1: Reading configuration data /etc/ssh/ssh_config
debug1: Reading configuration data /etc/ssh/ssh_config.d/50-redhat.conf
debug1: Reading configuration data /etc/crypto-policies/back-ends/openssh.config
debug1: configuration requests final Match pass
debug1: re-parsing configuration
debug1: Reading configuration data /etc/ssh/ssh_config
debug1: Reading configuration data /etc/ssh/ssh_config.d/50-redhat.conf
debug1: Reading configuration data /etc/crypto-policies/back-ends/openssh.config
debug1: Connecting to 10.3.30.252 [10.3.30.252] port 22.
debug1: Connection established.
debug1: identity file .ssh/id_rsa type 0
debug1: identity file .ssh/id_rsa-cert type -1
debug1: Local version string SSH-2.0-OpenSSH_8.7
debug1: Remote protocol version 2.0, remote software version Cisco-1.25
debug1: compat_banner: match: Cisco-1.25 pat Cisco-1.* compat 0x60000000
debug1: Authenticating to 10.3.30.252:22 as 'admin'
debug1: load_hostkeys: fopen /home/admuser/.ssh/known_hosts2: No such file or directory
debug1: load_hostkeys: fopen /etc/ssh/ssh_known_hosts: No such file or directory
debug1: load_hostkeys: fopen /etc/ssh/ssh_known_hosts2: No such file or directory
debug1: SSH2_MSG_KEXINIT sent
debug1: SSH2_MSG_KEXINIT received
debug1: kex: algorithm: diffie-hellman-group1-sha1
debug1: kex: host key algorithm: ssh-rsa
debug1: kex: server->client cipher: aes256-cbc MAC: hmac-sha1 compression: none
debug1: kex: client->server cipher: aes256-cbc MAC: hmac-sha1 compression: none
debug1: kex: diffie-hellman-group1-sha1 need=32 dh_need=32
debug1: kex: diffie-hellman-group1-sha1 need=32 dh_need=32
debug1: expecting SSH2_MSG_KEX_ECDH_REPLY
debug1: SSH2_MSG_KEX_ECDH_REPLY received
debug1: Server host key: ssh-rsa SHA256:ZeoK7vUTiPMLiEOmt/yZLdOqYhtoi3UpNVWDnIxSiRU
debug1: load_hostkeys: fopen /home/admuser/.ssh/known_hosts2: No such file or directory
debug1: load_hostkeys: fopen /etc/ssh/ssh_known_hosts: No such file or directory
debug1: load_hostkeys: fopen /etc/ssh/ssh_known_hosts2: No such file or directory
debug1: Host '10.3.30.252' is known and matches the RSA host key.
debug1: Found key in /home/admuser/.ssh/known_hosts:5
debug1: rekey out after 4294967296 blocks
debug1: SSH2_MSG_NEWKEYS sent
debug1: expecting SSH2_MSG_NEWKEYS
debug1: SSH2_MSG_NEWKEYS received
debug1: rekey in after 4294967296 blocks
debug1: Will attempt key: .ssh/id_rsa RSA SHA256:MeyWzh2UwdVrRLmeNk7EygjEvae8ZJqtmcRYW3mks6Q explicit
debug1: SSH2_MSG_SERVICE_ACCEPT received
debug1: Authentications that can continue: publickey,keyboard-interactive,password
debug1: Next authentication method: publickey
debug1: Offering public key: .ssh/id_rsa RSA SHA256:MeyWzh2UwdVrRLmeNk7EygjEvae8ZJqtmcRYW3mks6Q explicit
debug1: Server accepts key: .ssh/id_rsa RSA SHA256:MeyWzh2UwdVrRLmeNk7EygjEvae8ZJqtmcRYW3mks6Q explicit
Authenticated to 10.3.30.252 ([10.3.30.252]:22) using "publickey".
debug1: pkcs11_del_provider: called, provider_id = (null)
debug1: channel 0: new [client-session]
debug1: Entering interactive session.
debug1: pledge: filesystem full
R1#
```

```bash
R1#show ssh
Connection Version Mode Encryption  Hmac         State                 Username
0          2.0     IN   aes256-cbc  hmac-sha1    Session started       admin
0          2.0     OUT  aes256-cbc  hmac-sha1    Session started       admin
%No SSHv1 server connections running.
```
