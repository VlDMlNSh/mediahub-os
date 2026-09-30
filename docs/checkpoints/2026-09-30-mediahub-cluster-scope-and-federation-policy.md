# MediaHub Cluster Scope and Federation Policy — clarification

Date: 2026-09-30

## Canonical clarification

MediaHub has two fundamentally different cluster domains. They must not be treated as equivalent resource pools.

### 1. Local MediaHub Cluster — user environment

The local cluster is assembled inside the user's local network and exists primarily to extend the user's MediaHub capabilities.

Its purpose includes, according to the system passport and product architecture:
- extending user-configurable capabilities and settings;
- extending available local compute/AI/storage capacity;
- extending seamless wireless/network coverage and related local infrastructure capabilities;
- keeping ordinary user media and local workloads close to the user and local data.

The local cluster is therefore a user-facing resource fabric. Its resources belong to the user's local MediaHub environment and are coordinated as one local cluster.

Normal local traffic uses the local network directly. A management VPN is not required for ordinary media, storage, compute, or wireless-extension traffic.

### 2. Cloud Development Cluster — MediaHub company environment

The external/cloud cluster is not a general-purpose extension of the user's local cluster.

Its primary and default purpose is:
- MediaHub product development;
- CI/CD and engineering automation;
- developer compute;
- engineering storage and artifacts;
- internal development services;
- other company MediaHub operational needs.

The Cloud Development Cluster is a closed development environment by default. It is not exposed as a general user resource pool.

### 3. Controlled user escalation into cloud

A MediaHub user may invoke the Cloud Development Cluster only as a bounded, exceptional execution path when the local AI assistant cannot reasonably satisfy a request locally.

Two explicit escalation conditions are recognized:
1. local AI capacity is insufficient for the request;
2. local processing would take sufficiently long that a cloud execution path is warranted.

Such use is request-scoped and temporary. It does not turn the user's MediaHub into a permanent member of the Cloud Development Cluster.

The normal decision order is:

User request
  -> Local MediaHub AI / local compute
  -> if sufficient: complete locally
  -> if insufficient or excessively slow: explicit cloud escalation
  -> Cloud Development Cluster executes the bounded task
  -> result returns to the user's MediaHub
  -> cloud access for that request ends

### 4. Default isolation rule

Unless a specific user request is admitted through the cloud-escalation policy, the Cloud Development Cluster is closed to end users.

In particular, the following are NOT implied by federation:
- permanent user membership in the cloud cluster;
- permanent full-tunnel VPN from a user's network to the cloud;
- unrestricted access to company development resources;
- unrestricted access to engineering storage;
- unrestricted access to developer compute;
- exposure of internal development services;
- treating cloud capacity as ordinary local MediaHub capacity.

### 5. Federation is policy, not a flat network

The term Federation/Sync Layer describes controlled interaction between two distinct administrative and functional domains.

It does not mean that all nodes become one flat cluster.

The federation layer must provide:
- cluster identity and capability advertisement;
- admission control;
- request-scoped cloud execution authorization;
- job metadata exchange;
- selective result transfer;
- resumable and integrity-checked data transfer where data must cross domains;
- audit/evidence of each cloud escalation;
- failure isolation between local and cloud environments.

### 6. Data locality

Local user data remains local by default.

A cloud escalation must transfer only the minimum input required to process the admitted request, and only when policy permits it.

Results should return to the local MediaHub without requiring persistent synchronization of the user's full media library or local storage fabric into the cloud.

Large local datasets should normally be processed locally when feasible. If cloud execution is selected, the transfer must be explicit, bounded, resumable, integrity-checked, and attributable to the originating job.

### 7. Job classes

The scheduler must distinguish at least:

- LOCAL_ONLY — must execute inside the local MediaHub Cluster.
- LOCAL_PREFERRED — execute locally when feasible; cloud escalation allowed only under the defined admission policy.
- CLOUD_DEVELOPMENT_ONLY — internal company/developer work; never exposed as a user workload.
- CLOUD_ESCALATED_USER — a single user request admitted because local execution is insufficient or excessively slow.

CLOUD_ESCALATED_USER is an execution class, not a membership class.

### 8. Security boundaries

The Cloud Development Cluster must remain administratively separate from user-local resources.

Required invariants:
- user workloads receive least-privilege access;
- each cloud escalation has an explicit job identity and scope;
- cloud execution cannot implicitly enumerate or access the local cluster;
- internal development services remain inaccessible unless explicitly required by the admitted job;
- provider credentials remain exclusively in GitHub Secrets;
- credentials are never copied into node metadata or persisted on user/local nodes;
- Development Mesh access does not grant Media Data Plane access;
- API egress remains separately policy-controlled;
- VPN is connectivity infrastructure, not a mechanism for bypassing provider/regional restrictions.

### 9. Network model

Local cluster:
- direct LAN/P2P data plane;
- local wireless/network extension as defined by the system passport;
- local compute and storage paths remain local.

Cloud development cluster:
- private development network;
- encrypted management/discovery connectivity;
- direct node-to-node paths where available;
- relay fallback only where required.

Local-to-cloud:
- no permanent full-tunnel extension;
- request-scoped federation gateway/API;
- selective data transfer;
- explicit admission and audit.

### 10. Correct architectural model

MEDIAHUB FEDERATION

  LOCAL MEDIAHUB CLUSTER
    - user settings/capability extension
    - local AI/compute expansion
    - local storage/media
    - seamless wireless/network coverage extension
    - local resource coordination

          | controlled federation
          | request-scoped escalation only
          v

  CLOUD DEVELOPMENT CLUSTER
    - MediaHub development
    - CI/CD
    - developer compute
    - engineering storage/artifacts
    - company operational needs
    - closed by default to users

The cloud cluster is therefore a company development environment with a narrowly defined user escalation interface, not a second general-purpose user cluster.

## Implementation consequence

The next federation PoC must test the admission boundary before testing data synchronization.

Required PoC order:
1. cluster identity and trust;
2. user-vs-company workload classification;
3. local-only execution;
4. denied cloud request by default;
5. admitted CLOUD_ESCALATED_USER request;
6. bounded input transfer;
7. cloud execution;
8. bounded result return;
9. automatic end of request-scoped access;
10. failure/retry without granting persistent cloud membership;
11. audit/evidence verification.

No production deployment is authorized by this checkpoint.
GOLD #176 remains untouched.
Immutable R4 baseline remains untouched.
Provider credentials remain in GitHub Secrets.
