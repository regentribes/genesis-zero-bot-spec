# ISPEC-001: Member Bootstrap Specification — REV 1.0

**Document ID:** ISPEC-001  
**Revision:** 1.0  
**Status:** COMPLETE — 5 sections, 40 addenda, ready for implementation review  
**Source:** Topic 1958, Regen Tribe Collective Network  
**Date:** 2026-05-06  
**Authors:** Vitali, with community deliberation  

---

## CONTEXT

Every new member of the Integral Collective must undergo a defined bootstrap sequence to ensure a consistent, verifiable, and secure onboarding process. This specification defines that sequence and its governing principles.

---

## SECTION 1: DECISION

Every new member boots through a defined bootstrap sequence:

1. **Install** — Client binary installed on member node
2. **Verify** — Factory signature verified against known-good attestation
3. **Credential** — UNTP credentials established through CDS deliberation
4. **Connect** — Member node connects to local fleet
5. **Activate** — ITC ledger participation activated

All five steps must complete successfully before full community participation is granted.

---

## SECTION 2: RATIONALE

### Consistency
A defined bootstrap prevents inconsistent member states. Some members bootstrap correctly and participate fully. Others bootstrap partially and fall into degraded states that are hard to diagnose. The bootstrap sequence guarantees that every member who completes it has an identical baseline configuration.

### CDS Oversight
The sequence ensures the **Collective Deliberation System (CDS)** knows about every member before they participate in governance. No member can participate in governance votes or deliberation without being registered in the CDS first.

### Trust Architecture
The factory signature verification step ensures that only attested software participates. UNTP credentials provide cryptographically verifiable identity that is tied to community trust rather than external authorities.

---

## SECTION 3: REJECTED ALTERNATIVES

| Alternative | Problem |
|-------------|---------|
| Ad hoc bootstrap | Produces inconsistent member states requiring manual remediation |
| Managed bootstrap services | Creates single points of failure |
| Self-service without CDS deliberation | Allows bad actors to join without community oversight |

---

## SECTION 4: SPECIFICATION CONSEQUENCES

### Executable Sequence
The bootstrap sequence is a **single shell script or executable** that runs end-to-end. No manual intervention required for the happy path.

### ITC Ledger Logging
Every step logs to the **Integrity Trust Computation (ITC) ledger**. This provides an immutable audit trail of every bootstrap in the system.

### Failure Blocking
Failed steps block progression and publish ITC events. A failed step means the member does not complete bootstrap and does not gain access to any subsystem.

### FRS Monitoring
The **Fleet Registry System (FRS)** monitors bootstrap completion rates across all nodes. Anomalies trigger automatic alerts.

### CDS Deliberation Trigger
The **CDS deliberates on bootstrap failures** that occur above a defined threshold rate. If the fleet-wide failure rate exceeds threshold, the CDS enters a governance session to assess whether this represents an attack, a bug, or a configuration drift.

---

## SECTION 5: SUBSYSTEM INTEGRATION MAP

| Subsystem | Role in Bootstrap |
|-----------|-------------------|
| ITC Ledger | Immutable logging of all bootstrap steps |
| CDS | Deliberation on UNTP credential issuance; registry of all members |
| FRS | Monitors completion rates; triggers alerts |
| UNTP | Verifiable credentials tied to community trust model |
| Factory Attestation | Cryptographic verification of software provenance |
| Local Fleet | Peer-to-peer connectivity for newly joined nodes |

---

## ADDENDA (40)

*(Full addenda list maintained in implementation repository)*

- ADD-001: Bootstrap script must be reproducible from source
- ADD-002: Factory signature usesEd25519 or equivalent
- ADD-003: UNTP credential issuance requires quorum in CDS
- ADD-004: ITC events are signed by the bootstrapping node
- ADD-005: Fleet connectivity uses libp2p with gossipsub
- ... (35 additional addenda in implementation spec)

---

**END OF ISPEC-001 REV 1.0**