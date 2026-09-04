# MH-04 Service Trust

Locality is not trust. A service is not trusted merely because it is on localhost, the same host/LAN, under the same deployment, or supervised by Runtime.

Service trust requires identity, authentication, bounded capability assignment and policy context.

T1 services remain constrained: they cannot self-grant capabilities, bypass P0-05, mutate State Authority directly, or promote caches/persistence to authority.

Runtime supervision does not itself confer domain authorization.