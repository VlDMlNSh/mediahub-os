# MediaHub Network Infrastructure — System Passport Extension v1

Date: 2026-09-30
Status: normative system-passport description; architecture implementation remains a subsequent stage

## 1. Purpose

This document records the user's expanded description of the MediaHub network infrastructure as a durable system-passport requirement.

It is intentionally broader than a final implementation design. It defines the intended capabilities and boundaries that the later network reference architecture must satisfy.

## 2. Core network model

Every MediaHub machine is expected to have wired Internet connectivity available through Ethernet/RJ45.

The MediaHub network infrastructure uses this wired connection as the normal upstream/backhaul path for local wireless networking. A MediaHub node may therefore provide wireless access-point functionality while retaining wired Ethernet as its upstream connection.

When multiple MediaHub devices are present in one local installation, the devices participate in providing an integrated, seamless Wi-Fi coverage system.

The target experience is one local wireless environment rather than a collection of unrelated Wi-Fi networks.

## 3. MediaHub as a wireless-network participant

MediaHub nodes participate in extending wireless coverage together with compatible external access points.

The system passport explicitly includes interoperability with:
- Ubiquiti;
- Keenetic;
- other compatible access-point equipment selected in future qualification.

The architectural objective is to remove unnecessary dependence on dedicated physical controller/server hardware where equivalent controller functionality can safely be hosted by MediaHub.

This does NOT yet prescribe a particular vendor controller implementation. Vendor-specific control-plane compatibility, roaming behavior, provisioning, firmware support, and failure semantics must be qualified before being declared production-compatible.

The canonical product language is:
**расширение бесшовного беспроводного покрытия**.

## 4. Wired backhaul

The normal MediaHub wireless backhaul model is:

Internet/WAN
    |
Ethernet/RJ45
    |
MediaHub
    |
Wi-Fi access service
    |
local wireless clients

With multiple MediaHub nodes:

Internet/LAN backhaul
    |
+---+------------------+
|                      |
MediaHub A          MediaHub B
|                      |
Wi-Fi                 Wi-Fi

The detailed L2/L3 topology, addressing, roaming protocol, channel management, VLAN design, and failure behavior remain to be specified in the Network Infrastructure Reference Architecture.

## 5. Seamless Wi-Fi

The intended user experience includes seamless movement of wireless clients across the available MediaHub/external access points.

The final implementation must distinguish:
- wireless coverage;
- common SSID/network identity;
- client roaming;
- fast roaming;
- coordinated channel management;
- wired backhaul;
- actual wireless mesh, if used.

These are not assumed to be the same mechanism.

A feature may be described as supported only after its actual interoperability and roaming behavior are qualified.

## 6. Personal paid VPN for user Wi-Fi

MediaHub provides the user with the ability to use a personal paid VPN service.

When the user enables this feature, the designated Wi-Fi traffic is routed through the configured VPN tunnel.

The intended model is:

Wi-Fi client
    |
MediaHub network gateway
    |
VPN tunnel
    |
VPN provider
    |
Internet

The final architecture must support at least:
- explicit enable/disable;
- defined traffic scope;
- VPN tunnel lifecycle;
- DNS handling;
- route selection;
- tunnel failure behavior;
- direct-Internet fallback policy selected by the user/system policy;
- per-network or per-client policy where supported;
- status visibility in MediaHub applications.

The implementation may use an existing VPN protocol/service or a MediaHub-owned VPN implementation. No particular VPN technology is selected by this passport document.

MediaHub must not make a general VPN assumption merely because a VPN client exists. The routing policy must be explicit.

## 7. Local permanent online system

The MediaHub installation is a permanently connected local system.

The network infrastructure provides continuous connectivity for MediaHub-managed services, subject to normal network, power, and service availability.

The local system includes, as applicable:
- smart-home systems;
- energy/network energy systems;
- video surveillance;
- intercom;
- security systems;
- fire-safety systems;
- leak sensors;
- temperature sensors;
- humidity sensors;
- climate-control systems;
- lighting;
- gates and access equipment;
- other supported sensors and actuators;
- MediaHub media library.

## 8. Unified local control and data access

The MediaHub network is intended to provide a common local integration environment in which supported smart-home systems can interact with MediaHub services.

The MediaHub media library remains a first-class local service.

Supported local systems may have continuous access to the MediaHub media library where the relevant service contract and authorization permit it.

This does not mean that every device automatically receives unrestricted access to every MediaHub service.

Access must remain capability- and policy-controlled.

## 9. Mobile application connectivity

The user's MediaHub mobile application maintains persistent online connectivity with the user's MediaHub system, subject to connectivity and service availability.

The application is intended to provide monitoring and control of the supported MediaHub environment, including:
- smart-home systems;
- energy systems;
- surveillance;
- intercom;
- security;
- fire-safety systems;
- sensors;
- climate;
- lighting;
- gates;
- MediaHub media services.

The exact remote-access transport is not selected here. The later network architecture must define secure remote access, authentication, session management, reconnect behavior, notification delivery, and offline/failure semantics.

## 10. iPad wall-panel application

The MediaHub iPad application is a distinct application class from the user's general mobile application.

Its role is the minimum entry point into the local MediaHub system and includes use of an iPad as a wall-mounted control panel.

The iPad application is a paid MediaHub application.

It provides access to supported MediaHub smart-home and local-system functions according to the same authorization and local-service boundaries as other clients.

The iPad wall panel is not the developer application and must not be treated as part of the developer environment.

## 11. Application classes

The system passport distinguishes at least three application environments:

### 11.1 User mobile MediaHub application
User-facing mobile application for continuous monitoring and control.

### 11.2 MediaHub iPad wall-panel application
Paid, local-system-oriented application class intended for an iPad wall panel and minimal entry into the local MediaHub environment.

### 11.3 Developer mobile application
A separate developer environment/application class.

The developer application is explicitly outside the scope of this network-passport section and will be specified separately.

## 12. Security boundary

The network infrastructure must preserve a strict distinction between:
- user control;
- local MediaHub services;
- smart-home devices;
- MediaHub media storage;
- Internet access;
- personal VPN;
- developer infrastructure;
- CPRG protected registration;
- compute contribution.

Wireless access does not by itself authorize access to all MediaHub resources.

Likewise, access to the MediaHub control application does not imply unrestricted network access.

## 13. MediaHub and external Wi-Fi equipment

Ubiquiti and Keenetic are target interoperability classes, not an assumption that their entire physical infrastructure must be retained.

Where MediaHub can safely host the required logical controller/gateway functionality, dedicated controller hardware may be unnecessary.

However, the physical AP/radio itself remains a hardware function unless a qualified alternative exists.

The later reference architecture must therefore distinguish:
- controller functions;
- gateway/router functions;
- AP/radio functions;
- switching;
- backhaul;
- management;
- roaming coordination.

## 14. Local-network priority

The local MediaHub network is primarily a user-facing local system.

Normal local media, smart-home, sensor, surveillance, control, and automation traffic should remain local whenever the required service can be provided locally.

External access should not convert the local MediaHub installation into a permanently cloud-dependent system.

## 15. Relationship to existing MediaHub architecture

This passport extension is consistent with the previously established architecture:

- Local MediaHub Cluster remains the user-facing local cluster.
- Cloud Development Cluster remains a separate developer/company environment.
- Development Mesh is not the user's normal Media Mesh.
- Compute Contribution is a separate authorization domain.
- CPRG remains a protected registration-only capability.
- User data remains local by default.
- Developer infrastructure must not gain access merely because network connectivity exists.
- AI remains outside the state-authority role.

## 16. Explicit non-goals of this passport section

This document does not yet select:
- a Wi-Fi chipset;
- an AP firmware;
- a roaming protocol;
- Ubiquiti controller software;
- Keenetic controller software;
- a VPN provider;
- a VPN protocol;
- a remote-access provider;
- an IP addressing plan;
- VLAN/VRF topology;
- firewall implementation;
- DNS implementation;
- DHCP implementation;
- service-discovery implementation;
- physical switch topology;
- Wi-Fi channel plan;
- production deployment procedure.

Those belong to the subsequent Network Infrastructure Reference Architecture.

## 17. Required next-stage architecture questions

The next network-design stage must resolve:

1. How MediaHub nodes become Wi-Fi APs using their available hardware.
2. How wired Ethernet backhaul is separated from ordinary Internet egress.
3. How multiple MediaHub nodes coordinate one seamless Wi-Fi environment.
4. Which Ubiquiti/Keenetic interoperability features are supported.
5. Which controller functions can safely be hosted inside MediaHub.
6. Whether MediaHub is a gateway, AP, controller, or a combination depending on deployment mode.
7. How client traffic is segmented.
8. How personal VPN routing is selected and isolated.
9. What happens when the VPN fails.
10. How local smart-home systems are segmented from guest/client traffic.
11. How MediaHub media services are exposed to authorized local devices.
12. How mobile applications reach the local system remotely and securely.
13. How the iPad wall panel is provisioned and authenticated.
14. How local operation continues during WAN failure.
15. How developer infrastructure is prevented from entering the user network.
16. How Compute Contribution remains separately authorized.
17. How CPRG remains outside the normal data plane.
18. How discovery, DNS, addressing, IPv4/IPv6, firewalling, and service identity are implemented.
19. How Wi-Fi/AP failure and MediaHub-node failure affect coverage.
20. How the final network is qualified before deployment.

## 18. Passport principle

MediaHub is intended to be more than a server connected to a home network.

A MediaHub node participates in the local network itself and may provide:
- wired Internet/backhaul;
- wireless access;
- seamless coverage extension;
- local service integration;
- smart-home control;
- media-library services;
- secure user application access;
- optional personal VPN routing.

The exact implementation must preserve the separation between these functions and must not allow convenience in one network role to silently expand authority in another.
