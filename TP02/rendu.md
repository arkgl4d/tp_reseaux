# TP02

## Part II : Security

🌞 Ajouter des ACL sur le routeur

```bash
r1(config)#access-list 10 deny 10.2.30.0 0.0.0.255

r1(config)#access-list 10 permit ip any any

interface FastEthernet1/0.10
 encapsulation dot1Q 10
 ip address 10.2.10.254 255.255.255.0
 ip access-group 10 out
 ip nat inside
end

interface FastEthernet1/0.20
 encapsulation dot1Q 20
 ip address 10.2.20.254 255.255.255.0
 ip access-group 10 out
 ip nat inside
end
```

## 5. Try to attack

Le switch drop les trames car la machine attaquante n'est pas dans la base d'hote autorisées : 

```bash
*Mar 14 23:18:06.623: %SW_DAI-4-DHCP_SNOOPING_DENY: 1 Invalid ARPs (Res) on Et0/3, vlan 10.([bc24.11ef.3eff/10.2.10.254/0050.7966.6809/10.2.10.1/23:18:06 UTC Fri Mar 14 2025])
access1#
*Mar 14 23:18:08.635: %SW_DAI-4-DHCP_SNOOPING_DENY: 1 Invalid ARPs (Res) on Et0/3, vlan 10.([bc24.11ef.3eff/10.2.10.254/0050.7966.6809/10.2.10.1/23:18:08 UTC Fri Mar 14 2025])
access1#
*Mar 14 23:18:10.639: %SW_DAI-4-DHCP_SNOOPING_DENY: 1 Invalid ARPs (Res) on Et0/3, vlan 10.([bc24.11ef.3eff/10.2.10.254/0050.7966.6809/10.2.10.1/23:18:10 UTC Fri Mar 14 2025])
access1#
*Mar 14 23:18:12.639: %SW_DAI-4-DHCP_SNOOPING_DENY: 1 Invalid ARPs (Res) on Et0/3, vlan 10.([bc24.11ef.3eff/10.2.10.254/0050.7966.6809/10.2.10.1/23:18:12 UTC Fri Mar 14 2025])
access1#
*Mar 14 23:18:14.643: %SW_DAI-4-DHCP_SNOOPING_DENY: 1 Invalid ARPs (Res) on Et0/3, vlan 10.([bc24.11ef.3eff/10.2.10.254/0050.7966.6809/10.2.10.1/23:18:14 UTC Fri Mar 14 2025])
access1#
*Mar 14 23:18:16.648: %SW_DAI-4-DHCP_SNOOPING_DENY: 1 Invalid ARPs (Res) on Et0/3, vlan 10.([bc24.11ef.3eff/10.2.10.254/0050.7966.6809/10.2.10.1/23:18:16 UTC Fri Mar 14 2025])
access1#
*Mar 14 23:18:18.652: %SW_DAI-4-DHCP_SNOOPING_DENY: 1 Invalid ARPs (Res) on Et0/3, vlan 10.([bc24.11ef.3eff/10.2.10.254/0050.7966.6809/10.2.10.1/23:18:18 UTC Fri Mar 14 2025])
access1#
*Mar 14 23:18:20.660: %SW_DAI-4-DHCP_SNOOPING_DENY: 1 Invalid ARPs (Res) on Et0/3, vlan 10.([bc24.11ef.3eff/10.2.10.254/0050.7966.6809/10.2.10.1/23:18:20 UTC Fri Mar 14 2025])
access1#
*Mar 14 23:18:22.664: %SW_DAI-4-DHCP_SNOOPING_DENY: 1 Invalid ARPs (Res) on Et0/3, vlan 10.([bc24.11ef.3eff/10.2.10.254/0050.7966.6809/10.2.10.1/23:18:22 UTC Fri Mar 14 2025])
access1#
*Mar 14 23:18:24.672: %SW_DAI-4-DHCP_SNOOPING_DENY: 1 Invalid ARPs (Res) on Et0/3, vlan 10.([bc24.11ef.3eff/10.2.10.254/0050.7966.6809/10.2.10.1/23:18:24 UTC Fri Mar 14 2025])
access1#
*Mar 14 23:18:26.676: %SW_DAI-4-DHCP_SNOOPING_DENY: 1 Invalid ARPs (Res) on Et0/3, vlan 10.([bc24.11ef.3eff/10.2.10.254/0050.7966.6809/10.2.10.1/23:18:26 UTC Fri Mar 14 2025])
access1#
...
```