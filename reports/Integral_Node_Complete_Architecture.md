# INTEGRAL NODE — COMPLETE SOLUTION ARCHITECTURE
## Interface Design Between All Layers, Subsystems, and External Systems
**Compiled:** 2026-04-30 | **Based on:** Integral Whitepaper v0.1, DevGuide v0.1, Regen Tribe research | **Status:** Architecture specification

---

## PREAMBLE

The Integral system has five subsystems: CDS, OAD, ITC, COS, FRS. Each subsystem is semi-autonomous — responsible for a distinct domain — yet tightly coupled through shared information flows. This document specifies the complete interface architecture: how each subsystem interfaces with the others, how an Integral node interfaces with the external world, and how federated nodes communicate.

The architecture follows the principle from the DevGuide: **architectural faithfulness over functional completeness**. The minimum viable implementation is specified first; expansion paths are noted.

---

## SECTION 1 — INTERNAL SUBSYSTEM INTERFACES

### 1.1 The Five-Subsystem Data Flow Map

The master data flow follows this cybernetic cycle:

```
Decision → Design → Production → Contribution accounting → Feedback → Decision
   CDS          OAD              COS                    ITC            FRS
```

**Every loop generates information the next subsystem consumes.**

### 1.2 CDS → OAD Interface

**What flows:** Decisions authorizing designs, standards, and constraints

**Data contract:**
```json
{
  "type": "CDS_DECISION",
  "decision_id": "uuid",
  "timestamp": "ISO8601",
  "author": "member_did",
  "scope": "local | federated",
  "decision_type": "design_authorization | standard_set | constraint_def",
  "payload": {
    "design_id": "uuid | null",
    "standard_description": "string",
    "constraint_rules": ["rule1", "rule2"],
    "priority_class": "critical | normal | low",
    "effective_date": "ISO8601",
    "sunset_clause": "ISO8601 | null"
  },
  "consensus_data": {
    "participants": ["did1", "did2"],
    "weighted_support": 0.87,
    "objections_resolved": ["objection_id1"],
    "objections_pending": []
  }
}
```

**OAD receives:** Authorized design requests from CDS. Every design proposal that enters OAD must have a CDS decision_id linking it to the governance that authorized it.

**OAD returns:** Design completions, version updates, validation failures
```json
{
  "type": "OAD_DESIGN_UPDATE",
  "design_id": "uuid",
  "version": "int",
  "status": "draft | review | approved | archived",
  "author_did": "did",
  "design_data": {
    "blueprint": "multiformat_spec",
    "materials": ["material_spec"],
    "labor_hours_estimate": "float",
    "ecological_impact_estimate": "impact_obj",
    "safety_analysis": "safety_report"
  },
  "linked_decision_id": "uuid",
  "validation_signals": {
    "meets_standards": true,
    "safety_verified": true,
    "ecological_within_bounds": true
  }
}
```

**Key rule:** OAD cannot publish a design for production use without a linked CDS authorization. Unauthorised designs exist in draft state only.

### 1.3 OAD → COS Interface

**What flows:** Production requirements and design specifications

**Data contract:**
```json
{
  "type": "OAD_PRODUCTION_ORDER",
  "order_id": "uuid",
  "design_id": "uuid",
  "design_version": "int",
  "quantity": "int",
  "quality_standards": {
    "acceptance_criteria": ["criterion1"],
    "inspection_protocol": "protocol_id",
    "rejection_threshold": "float"
  },
  "materials_required": [
    {
      "material_id": "uuid",
      "quantity": "float",
      "unit": "string",
      "source_preference": "internal | external | either"
    }
  ],
  "labor_requirements": {
    "skill_categories": ["category1"],
    "estimated_hours": "float",
    "urgency": "standard | urgent | critical"
  },
  "ecological_constraints": {
    "max_carbon_kg": "float",
    "max_water_liters": "float",
    "waste_limits": "limits_obj"
  },
  "delivery_deadline": "ISO8601"
}
```

**COS receives:** What to produce, from which design, with what constraints.

**COS returns:** Production outcomes and actual metrics
```json
{
  "type": "COS_PRODUCTION_OUTPUT",
  "order_id": "uuid",
  "status": "completed | partial | failed",
  "actual_metrics": {
    "labor_hours": "float",
    "materials_used": [{"material_id": "uuid", "qty": "float", "waste_pct": "float"}],
    "tooling_wear_hours": "float",
    "throughput_time_hours": "float",
    "defect_rate": "float",
    "ecological_actual": {
      "carbon_kg": "float",
      "water_liters": "float",
      "waste_kg": "float"
    }
  },
  "quality_signals": {
    "passed_inspection": true,
    "rejected_units": "int",
    "consumer_satisfaction_score": "float | null"
  },
  "production_node_id": "string",
  "timestamp": "ISO8601"
}
```

### 1.4 COS → ITC Interface

**What flows:** Labor events, contribution records, material usage data

**Data contract:**
```json
{
  "type": "ITC_LABOR_EVENT",
  "event_id": "uuid",
  "member_did": "did",
  "timestamp": "ISO8601",
  "task_type": "production | maintenance | governance | education | care",
  "context": {
    "order_id": "uuid | null",
    "design_id": "uuid | null",
    "cos_workflow_id": "uuid | null"
  },
  "labor_data": {
    "hours_contributed": "float",
    "skill_weight": "float",
    "difficulty_factor": "float",
    "urgency_multiplier": "float",
    "seasonal_factor": "float",
    "individual_adjustment": "float"
  },
  "output_claim": {
    "task_description": "string",
    "outcome_verified": false,
    "verification_method": "pending | peer_review | output_confirmation"
  },
  "source_node": "string",
  "federation_context": "local | incoming_cross_node | outgoing_cross_node"
}
```

**ITC processes:** Labor events → calculates ITC credit award based on three-signal valuation (labor effort + ecological sensitivity + fairness adjustments from FRS) → records in member ledger → applies decay rules.

**ITC → COS feedback:** When ITC values for a production process change (due to design improvements in OAD or ecological cost changes from FRS), ITC notifies COS so production cost expectations update.

```json
{
  "type": "ITC_VALUATION_UPDATE",
  "design_id": "uuid",
  "reason": "design_improvement | ecological_cost_change | fairness_adjustment",
  "old_itc_value": "float",
  "new_itc_value": "float",
  "affected_members": ["did1", "did2"],
  "effective_date": "ISO8601",
  "因果链": "string (explains why)"
}
```

### 1.5 ITC → FRS Interface

**What flows:** Contribution ledger data, access balance histories, trade patterns

**Data contract:**
```json
{
  "type": "ITC_TELEMETRY",
  "period": {
    "start": "ISO8601",
    "end": "ISO8601"
  },
  "member_balances": [
    {
      "member_did": "did",
      "starting_balance": "float",
      "credits_earned": "float",
      "credits_spent": "float",
      "credits_decayed": "float",
      "ending_balance": "float",
      "net_flow": "float"
    }
  ],
  "aggregate_metrics": {
    "total_labor_hours": "float",
    "average_balance": "float",
    "balance_distribution_gini": "float",
    "decay_rate_applied": "float",
    "cross_node_trades": "int",
    "external_fiat_exchanges": "int"
  },
  "access_events": [
    {
      "member_did": "did",
      "good_or_service": "string",
      "itc_spent": "float",
      "timestamp": "ISO8601"
    }
  ]
}
```

**FRS receives:** Raw ITC flows. Uses them to compute balance distribution, detect hoarding or starvation patterns, identify labor bottlenecks, and generate fairness signals.

**FRS → ITC:** Ecological and fairness signals that adjust how ITC values are calculated.

### 1.6 FRS → All Subsystems

FRS is the cybernetic sensing layer. It monitors system state and emits signals to every other subsystem.

**FRS → CDS:**
```json
{
  "type": "FRS_CDS_SIGNAL",
  "signal_category": "boundary_warning | opportunity | crisis",
  "priority": "low | medium | high | critical",
  "domain": "ecological | economic | social | operational",
  "findings": {
    "metric_name": "string",
    "current_value": "float",
    "threshold": "float",
    "trajectory": "improving | stable | degrading | critical",
    "affected_nodes": ["member_did_list | area_id"]
  },
  "recommended_action": "string",
  "escalate_to_syntegrity": false
}
```

**FRS → OAD:**
```json
{
  "type": "FRS_OAD_SIGNAL",
  "design_id": "uuid",
  "performance_data": {
    "actual_vs_expected_labor": "float",
    "actual_vs_expected_ecological": "impact_obj",
    "failure_modes": ["mode1"],
    "lifecycle_data": "lifecycle_obj",
    "user_satisfaction": "float"
  },
  "refinement_suggestions": [
    {
      "improvement": "string",
      "expected_impact": "float",
      "priority": "high | medium | low"
    }
  ]
}
```

**FRS → COS:**
```json
{
  "type": "FRS_COS_SIGNAL",
  "workflow_id": "uuid",
  "operational_data": {
    "throughput_vs_capacity": "float",
    "bottleneck_location": "string",
    "labor_utilization": "float",
    "resource_strain_score": "float"
  },
  "rebalancing_recommendations": [
    {
      "action": "string",
      "expected_improvement": "float",
      "urgency": "high | medium | low"
    }
  ]
}
```

**FRS → ITC:**
```json
{
  "type": "FRS_ITC_SIGNAL",
  "signal_type": "ecological_cost_update | fairness_adjustment | scarcity_factor",
  "parameters": {
    "ecological_sensitivity_multiplier": "float",
    "scarcity_weight": "float",
    "need_based_access_modifier": "float"
  },
  "affected_designs": ["design_id_list"],
  "reason": "string",
  "evidence": "string"
}
```

### 1.7 Summary: Internal Data Flows

```
CDS ←→ OAD: Decisions ↔ Design authorizations
OAD ←→ COS: Production orders ↔ Output metrics
COS ←→ ITC: Labor events ↔ Valuation updates
COS ←→ FRS: Operational data ↔ Rebalancing signals
ITC ←→ FRS: Contribution telemetry ↔ Ecological/fairness signals
FRS ←→ CDS: Boundary warnings ↔ Deliberation triggers
FRS ←→ OAD: Performance data ↔ Design refinements
```

---

## SECTION 2 — EXTERNAL-FACING INTERFACES

### 2.1 The External World Problem

Integral nodes exist within a world of nation-states, monetary economies, logistics corridors, and supply chain infrastructure. Every node must interact with this external world for:
- **External procurement** — acquiring materials, tools, energy inputs
- **External sales** — selling surplus goods and services
- **Legal compliance** — taxes, contracts, property rights, regulatory requirements
- **Physical logistics** — moving goods through Rec.50 corridor infrastructure
- **Supply chain verification** — Rec.49 DPPs proving provenance of purchased materials

The architecture must handle these without Integral's internal post-monetary logic breaking.

### 2.2 External Procurement Interface (ITC ↔ External Markets)

**The bridge:** Members earn external income (fiat currency) → convert to ITC balance → spend ITC internally → use fiat only for external transactions.

**Conversion mechanism:**
```json
{
  "type": "ITC_FIAT_EXCHANGE",
  "event_id": "uuid",
  "member_did": "did",
  "direction": "fiat_to_itc | itc_to_fiat",
  "fiat_amount": "float",
  "fiat_currency": "USD | EUR | CRC | etc",
  "itc_amount": "float",
  "exchange_rate": {
    "basis": "real_labor_market_equivalent",
    "rate": "float",
    "established_by": "CDS_decision_id",
    "review_frequency": "monthly"
  },
  "external_purpose": {
    "procurement_item": "string",
    "vendor": "string",
    "itc_access_right": "bool"
  },
  "timestamp": "ISO8601"
}
```

**Key rule:** ITC → fiat conversion is allowed (for external purchases). Fiat → ITC conversion is tracked but ITC can never be transferred to another person in fiat form. The conversion rate is set by CDS based on local labor market data, reviewed monthly by FRS.

**External procurement DPI (Digital Procurement Interface):**
```json
{
  "type": "EXTERNAL_PROCUREMENT_ORDER",
  "order_id": "uuid",
  "source": {
    "vendor_id": "string",
    "vendor_did": "did | null",
    "location": "country_code",
    "has_unpt_dpp": true
  },
  "items": [
    {
      "material_name": "string",
      "quantity": "float",
      "unit": "string",
      "estimated_cost_fiat": "float",
      "unpt_dpp_id": "uuid | null"
    }
  ],
  "logistics": {
    "corridor_id": "string | null",
    "incoterms": "string",
    "expected_lead_time_days": "int"
  },
  "funding": {
    "source": "member_fiat | community_fiat | itc_conversion",
    "amount": "float"
  }
}
```

### 2.3 External Sales Interface (COS ↔ Markets)

**The bridge:** COS produces surplus → sold for fiat or for ITC (internal to other nodes) or for other external payments.

**Sales event:**
```json
{
  "type": "EXTERNAL_SALE",
  "sale_id": "uuid",
  "cos_order_id": "uuid",
  "items_sold": [
    {
      "design_id": "uuid",
      "quantity": "float",
      "unit_price_fiat": "float",
      "unpt_dpp_id": "uuid"
    }
  ],
  "buyer": {
    "type": "individual | business | government | other_node",
    "location": "country_code",
    "payment_method": "fiat | itc_cross_node"
  },
  "revenue": {
    "fiat_amount": "float",
    "fiat_currency": "string",
    "itc_amount": "float",
    "allocation": {
      "member_producer_share": "float",
      "community_infrastructure_fund": "float",
      "OAD_improvement_fund": "float"
    }
  },
  "logistics": {
    "corridor_id": "string | null",
    "tracking_id": "string"
  }
}
```

**Revenue allocation:** When goods are sold externally, fiat revenue is split: portion goes to the producing members (via their external account), portion stays in the community fund for infrastructure, portion feeds OAD improvement.

### 2.4 Legal Interface (Node ↔ State Systems)

**The challenge:** Integral nodes are not legal entities in most jurisdictions. They cannot sign contracts, hold bank accounts, or appear in court — but they must interact with the legal world constantly.

**Solution architecture:** A **Legal Wrapper** layer above the node.

**Legal Wrapper types:**

| Wrapper | Use case | Jurisdiction |
|---------|----------|-------------|
| **Worker Cooperative** | Production, employment, contracts | US, EU, Latin America |
| **Agricultural Cooperative** | Food production, sales, supply chain | Universal |
| **Community Land Trust (CLT)** | Land holding, long-term lease | US, EU increasingly |
| **Non-profit / Foundation** | Grant receiving, educational activities | Universal |
| **Benefit Corporation** | External-facing commercial activities | US, EU |
| **Mutual Aid Society** | Internal support, care economy | Universal |

**The node has one or more Legal Wrappers** that provide:
- Bank account access (fiat transactions)
- Contract signing authority (external agreements)
- Tax compliance (sales tax, income reporting)
- Regulatory compliance (safety standards, food handling, building codes)
- Grant eligibility

**The node's internal logic (ITC, CDS) operates independently** — the Legal Wrapper just translates between node decisions and external legal requirements.

**Interface contract:**
```json
{
  "type": "LEGAL_WRAPPER_TRANSACTION",
  "wrapper_id": "uuid",
  "wrapper_type": "worker_coop | agricultural_coop | clt | nonprofit | benefit_corp",
  "node_decision_ref": "CDS_decision_id",
  "action": {
    "type": "contract_sign | bank_transfer | tax_filing | regulatory_compliance | grant_application",
    "details": "json",
    "external_counterparty": "string | null",
    "fiat_amount": "float | null",
    "legal_entity_name": "string"
  },
  "node_internal_effect": {
    "itc_impact": "none | debit_member | credit_community",
    "cos_workflow_trigger": "string | null"
  },
  "compliance_flags": {
    "jurisdiction": "string",
    "regulatory_requirements_met": true,
    "documentationarchived": true
  }
}
```

### 2.5 Corridor Logistics Interface (COS ↔ Rec.50 Corridor Digital Platform)

When goods move through a Rec.50 corridor, they interact with the corridor's digital infrastructure.

**Entry interface:**
```json
{
  "type": "CORRIDOR_BOOKING",
  "booking_id": "uuid",
  "origin": {
    "facility_id": "string",
    "location_code": "UN/LOCODE",
    "facility_type": "production_site | warehouse | dry_port"
  },
  "destination": {
    "facility_id": "string",
    "location_code": "UN/LOCODE",
    "facility_type": "port | warehouse | buyer_facility"
  },
  "cargo": [
    {
      "description": "string",
      "harmonized_code": "string",
      "gross_weight_kg": "float",
      "volume_m3": "float",
      "unpt_dpp_id": "uuid",
      "itc_value": "float",
      "goods_type": "food | timber | manufactured | other"
    }
  ],
  "transport_mode": "road | rail | river | sea",
  "corridor_id": "string",
  "pre_arrival_data": {
    "e_cmr_id": "uuid | null",
    "e_manifest_id": "uuid | null",
    "certificate_of_origin": "bool",
    "insurance_certificate": "bool"
  },
  "corridor_platform_api": "url"
}
```

**The node integrates with the corridor's digital platform** via standardized APIs using UN/CEFACT RDM-aligned data. The node does NOT need to be a "country" — it acts as a logistics entity, like a freight forwarder, within the corridor.

---

## SECTION 3 — FEDERATION INTERFACES

### 3.1 Inter-Node Communication Architecture

When two Integral nodes trade or share information, they use a federated interface.

**Protocol stack:**
- **Communication:** Nostr (identity + messaging) — each node operates a Nostr relay
- **Trust:** W3C DID Core + Verifiable Credentials (UNTP layer)
- **Data:** SurrealDB federation + shared OAD design commons
- **Coordination:** Holochain hREA for economic events
- **AI integration:** MCP for agent-to-agent communication

### 3.2 Node Identity and Discovery

**Every node has:**
- A Nostr public key (npub) — identity on the network
- A W3C DID — decentralized identifier for Verifiable Credentials
- A SurrealDB namespace — federated database instance

**Node registry:**
```json
{
  "type": "NODE_REGISTRY_ENTRY",
  "node_id": "uuid",
  "node_name": "string",
  "node_npub": "npub1...",
  "node_did": "did:key:...",
  "location": {
    "country": "string",
    "region": "string",
    "climate_zone": "string"
  },
  "capabilities": {
    "production_domains": ["food", "timber", "energy", "built_env"],
    "service_domains": ["education", "care", "technical"],
    "max_inter_node_capacity": "int_members"
  },
  "status": "active | suspended | decommissioned",
  "surrealdb_endpoint": "ws://...",
  "last_heartbeat": "ISO8601"
}
```

**Discovery mechanism:** Nodes register with a federated registry (initially a shared SurrealDB table; potentially a Holochain DHT as the network grows). Any node can query the registry to find partners with specific capabilities.

### 3.3 Cross-Node ITC Transfer

**Scenario:** Member in Node A earns ITC → wants to access goods produced by Node B.

**Mechanism: ITC credit note, not transfer**

Node A issues a **cross-node credit note** denominated in ITC:
```json
{
  "type": "CROSS_NODE_ITC_CREDIT_NOTE",
  "credit_note_id": "uuid",
  "issuing_node": "node_A_id",
  "receiving_node": "node_B_id",
  "member_did": "did",
  "amount_itc": "float",
  "purpose": "goods_access | services_access | investment",
  "validity_period": {
    "issued": "ISO8601",
    "expires": "ISO8601"
  },
  "redemption_conditions": {
    "goods_categories_allowed": ["food", "timber"],
    "services_allowed": ["education"],
    "restrictions": ["no_cash_withdrawal"]
  },
  "signatures": {
    "member": "member_sig",
    "issuing_node": "node_A_sig"
  }
}
```

Node B receives the credit note → verifies it against Node A's registry → honors it by delivering goods/services → sends a **redemption receipt** back to Node A.

Node A's ITC ledger is debited. Node B's production records are updated.

**Non-transferability preserved:** The credit note can only be issued TO a specific node for specific purposes. It cannot be sold, traded, or accumulated. This preserves ITC's non-transferable nature while enabling federation.

### 3.4 Cross-Node OAD Sharing

**Every node contributes to and draws from the shared OAD commons.**

**Design contribution event:**
```json
{
  "type": "OAD_CONTRIBUTION",
  "design_id": "uuid",
  "contributing_node": "node_id",
  "contributing_member_did": "did",
  "design_version": "int",
  "design_data": {
    "specification": "multiformat",
    "performance_metrics": {...},
    "adaptations_for_regions": ["region_list"]
  },
  "contribution_license": "integral_open_commons",
  "attestation": {
    "verifiable_credential": "vc_json",
    "signing_did": "did:key:..."
  }
}
```

**Design pull event:** Node B queries the OAD commons for a design matching its needs → receives the design specification + adaptation notes → implements locally.

**Quality assurance:** FRS from both nodes can exchange performance data on shared designs, informing whether a design should be flagged as "verified for region X" or "performance concern noted."

### 3.5 Cross-Node FRS Federation

**FRS alerts propagate across the network:**

```json
{
  "type": "CROSS_NODE_FRS_ALERT",
  "alert_id": "uuid",
  "originating_node": "node_id",
  "alert_type": "ecological_threshold_crossed | resource_strain | supply_chain_disruption | design_failure_pattern",
  "severity": "local | regional | network_wide",
  "affected_domains": ["food", "water", "energy"],
  "data": {
    "metric": "string",
    "value": "float",
    "threshold": "float",
    "trajectory": "string"
  },
  "recommended_node_actions": ["action_list"],
  "broadcast_scope": "all_nodes | regional_nodes | specific_nodes"
}
```

Nodes receiving alerts can take preventive action: adjust production, stock reserves, or trigger CDS deliberation on federation-wide response.

---

## SECTION 4 — COMPLETE INTERFACE LAYER MAP

### Layer 0: Physical Substrate
```
Sensors, Actuators, Edge Hardware
(RISC-V, ESP32, Cortex-M4, WASM-on-edge)
```
↓ raw data

### Layer 1: Edge Compute
```
Local processing, SNN inference, mesh networking
(LoRa/Zigbee/WiFi mesh, IOTA for sensor micropayments)
```
↑ processed data

### Layer 2: Node Data (SurrealDB)
```
Member profiles (DID-linked)
ITC ledger (contribution + access)
COS production records
OAD design commons
FRS telemetry (time-series)
Cross-node registry
```
↑ queryable

### Layer 3: Node Logic (Subsystems)
```
CDS: decision pipeline, weighted consensus, Syntegrity
OAD: design management, version control, peer review
ITC: contribution accounting, access valuation, decay engine
COS: production planning, labor coordination, resource allocation
FRS: monitoring, alerting, cybernetic feedback
```
↑ inter-subsystem events

### Layer 4: Node API Gateway
```
Internal: JSON-RPC / REST for subsystem communication
External: REST + UN/CEFACT RDM-aligned for corridor
Federation: Nostr relay + SurrealDB federation + MCP
```
↑ protocols

### Layer 5: External World Interfaces
```
Legal Wrapper (cooperative/CLT/nonprofit)
Corridor Digital Platform (Rec.50)
UNTP DPP verification (Rec.49)
External procurement/sales
Fiat exchange mechanism
```
↑ translated

### Layer 6: Federation
```
Node registry (SurrealDB/Holochain DHT)
Cross-node ITC credit notes
OAD shared commons (Radicle)
FRS alert propagation
AI agent federation (MCP)
```
↑ coordinated

---

## SECTION 5 — MINIMUM VIABLE NODE INTERFACE SPEC

For a starting community (5-15 members, Phase 1):

### Required interfaces (MVP):
1. **ITC ledger** — simple record of labor contributions and access events (even spreadsheet-backed initially)
2. **OAD shared notes** — shared document (Google Docs, Notion) tracking design decisions and versions
3. **CDS simple protocol** — weekly meetings with recorded decisions in a shared ledger
4. **COS task board** — Trello or similar for production task management
5. **FRS manual reporting** — monthly self-reporting of well-being, resource use, community health
6. **External fiat bridge** — simple spreadsheet tracking external income and conversions

### Interfaces to add as node grows:
| Node size | Add interfaces |
|-----------|----------------|
| 15-30 members | SurrealDB for ITC ledger; Nostr for communication |
| 30-100 | Full 5-subsystem stack; Legal Wrapper; external procurement API |
| 100-500 | Federation with 1-2 other nodes; OAD shared commons via Radicle |
| 500+ | Full Rec.50 corridor integration; UNTP DPP for external sales; Cross-node ITC |

---

## SECTION 6 — INTERFACE WITH UNTP/VERIFIABLE CREDENTIALS

### The integration填补 Integral's missing trust layer

**Integral does not currently specify how member identity and attestation work. UNTP fills this gap.**

**Member credential schema:**
```json
{
  "type": "VerifiableCredential",
  "issuer": "did:key:node_authority",
  "credentialSubject": {
    "member_did": "did:key:member",
    "node_id": "uuid",
    "contribution_role": "string",
    "skills_attested": ["string"],
    "itc_standing": {
      "balance": "float",
      "decay_schedule": "string",
      "verified_contributions": "int"
    },
    "federation_trust_level": "basic | trusted | verified"
  },
  "proof": {
    "type": "Ed25519Signature2020",
    "created": "ISO8601",
    "verificationMethod": "did:key:node_authority#key1",
    "proofPurpose": "assertionMethod"
  }
}
```

**Labor event credential:**
```json
{
  "type": "VerifiableCredential",
  "issuer": "did:key:cos_production_node",
  "credentialSubject": {
    "event_id": "uuid",
    "member_did": "did:key:member",
    "task_type": "string",
    "hours": "float",
    "output_verified": "boolean",
    "linked_cos_workflow": "uuid",
    "itc_awarded": "float",
    "timestamp": "ISO8601"
  },
  "proof": {...}
}
```

**This enables:**
- Cross-node verification of member contributions without revealing personal data
- External parties (buyers, logistics providers) can verify community credentials
- ICO/audit: third-party can verify ITC ledger accuracy without accessing raw data

---

## SECTION 7 — CONCRETE API ENDPOINTS

### Node Internal API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/cds/decisions` | Submit a new decision proposal |
| GET | `/cds/decisions/{id}` | Get decision status and consensus data |
| POST | `/cds/votes` | Register weighted consensus vote |
| GET | `/oad/designs` | List all OAD designs |
| POST | `/oad/designs` | Submit new design for review |
| GET | `/oad/designs/{id}` | Get design with version history |
| POST | `/oad/designs/{id}/validate` | Request design peer review |
| GET | `/itc/balance/{member_did}` | Get member ITC balance |
| POST | `/itc/contribution` | Record a labor contribution event |
| POST | `/itc/access` | Record an access event (goods received) |
| POST | `/itc/exchange` | Convert fiat ↔ ITC |
| GET | `/cos/workflows` | List active production workflows |
| POST | `/cos/workflows` | Create production workflow |
| POST | `/cos/workflows/{id}/complete` | Mark workflow complete with metrics |
| GET | `/frs/telemetry` | Get FRS monitoring data |
| GET | `/frs/alerts` | Get active alerts |
| POST | `/frs/signals` | Submit FRS signal to subsystem |

### External API (Legal Wrapper Interface)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/external/procurement` | Place external order |
| GET | `/external/procurement/{id}/tracking` | Track order status |
| POST | `/external/sales` | Record external sale |
| POST | `/legal/wrapper/transaction` | Execute legal wrapper action (contract, payment) |
| GET | `/corridor/booking` | Book corridor transit |
| POST | `/corridor/pre-arrival` | Submit pre-arrival data (e-CMR, manifest) |

### Federation API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/federation/nodes` | Discover active nodes |
| GET | `/federation/nodes/{id}` | Get node capabilities |
| POST | `/federation/credit-note` | Issue cross-node ITC credit note |
| POST | `/federation/credit-note/redeem` | Redeem received credit note |
| GET | `/oad/commons` | Query shared OAD design commons |
| POST | `/oad/commons/contribute` | Contribute design to commons |
| POST | `/federation/frs-alert` | Broadcast FRS alert to network |

---

## SECTION 8 — IMPLEMENTATION PRIORITY

### Phase 1 (Months 1-6): Core Internal
1. ITC ledger (manual → SurrealDB)
2. OAD design notes (shared doc → structured)
3. CDS decision log (meeting notes → structured decisions)
4. FRS self-reporting (monthly)
5. External fiat tracking (spreadsheet)

### Phase 2 (Months 6-12): Digital Infrastructure
6. SurrealDB deployment for all subsystems
7. Member DID assignment (W3C DID key pairs)
8. Nostr relay for node communication
9. MCP agent integration
10. First external procurement with UNTP DPP verification

### Phase 3 (Months 12-24): Federation
11. Second node connection
12. Cross-node ITC credit note system
13. Shared OAD commons via Radicle
14. FRS cross-node alert propagation
15. First Rec.50 corridor integration for external logistics

### Phase 4 (Years 2-5): Full Integration
16. Full UNTP Verifiable Credential issuance
17. Legal Wrapper formalization
18. Corridor Digital Platform API integration
19. MeTTa/AtomSpace governance encoding
20. Federation with 5+ nodes

---

*Architecture compiled 2026-04-30 based on Integral Whitepaper v0.1, DevGuide v0.1, UN ECE Rec.49+50, UNTP specs, and Regen Tribe research. All interfaces are specified as JSON data contracts suitable for software implementation.*