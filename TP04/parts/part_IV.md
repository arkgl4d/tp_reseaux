### 🌞 Créer un utilisateur : fichier user.yml

```bash
- name: Ajouter un utilisateur sur les routeurs Cisco
  hosts: 
    - r1
    - r2
  gather_facts: no
  tasks:
    - name: Ajouter un utilisateur avec un mot de passe
      cisco.ios.ios_user:
        name: admin2
        configured_password: "aze+123"
        privilege: 15
        state: present
      become: yes
      become_method: enable
```

### 🌞 Lancer un serveur SNMP : fichier snmp.yml

```bash
- name: Configurer SNMP sur les routeurs
  hosts:
    - r1
    - r2
  gather_facts: no
  tasks:
    - name: Configurer la communauté SNMP en lecture seule
      cisco.ios.ios_config:
        lines:
          - snmp-server community super_commu ro

    - name: Configurer l'hôte SNMP pour envoyer les traps
      cisco.ios.ios_config:
        lines:
          - snmp-server host 10.3.30.100 version 2c super_commu
```

```bash
snmpwalk -v 2c -c super_commu 10.3.30.254 ifDescr
IF-MIB::ifDescr.1 = STRING: FastEthernet0/0
IF-MIB::ifDescr.2 = STRING: FastEthernet1/0
IF-MIB::ifDescr.3 = STRING: FastEthernet2/0
IF-MIB::ifDescr.4 = STRING: Null0
IF-MIB::ifDescr.5 = STRING: FastEthernet0/0.10
IF-MIB::ifDescr.6 = STRING: FastEthernet0/0.20
IF-MIB::ifDescr.7 = STRING: FastEthernet0/0.30
```