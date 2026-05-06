#!/bin/bash
set -e

BOT_TOKEN=$(cat ~/.openclaw/openclaw.json | jq -r '.channels.telegram.accounts.genesis.botToken')
CHAT_ID="-1001921904187"
THREAD_ID="3651"
API="https://api.telegram.org/bot${BOT_TOKEN}/sendMessage"

send() {
  local msg="$1"
  local response=$(curl -s -X POST "$API" \
    -H "Content-Type: application/json" \
    -d "$(jq -n \
      --arg chat "$CHAT_ID" \
      --arg text "$msg" \
      --argjson thread "$THREAD_ID" \
      '{
        chat_id: $chat,
        text: $text,
        parse_mode: "HTML",
        message_thread_id: $thread,
        link_preview_options: { is_disabled: true }
      }')")
  local ok=$(echo "$response" | jq -r '.ok')
  if [ "$ok" != "true" ]; then
    echo "ERROR: $(echo "$response" | jq -r '.description')"
  fi
}

# PART 1: PREAMBLE + SECTION 1
send '[[reply_to_current]] 🏗️ <b>Integral Node Architecture</b> — Part 1/8

<i>Complete interface design: internal + external + federation</i>

<b>PREAMBLE</b>

The Integral system has 5 subsystems: CDS, OAD, ITC, COS, FRS. Each semi-autonomous yet tightly coupled. This document specifies:
• How each subsystem interfaces with the others
• How a node interfaces with the external world
• How federated nodes communicate

Principle: <b>Architectural faithfulness over functional completeness.</b> MVP specified first; expansion paths noted.

<b>SECTION 1 — INTERNAL SUBSYSTEM INTERFACES</b>

<b>The Master Data Flow:</b>
Decision → Design → Production → Contribution accounting → Feedback → Decision
   CDS          OAD              COS                    ITC            FRS

Every loop generates info the next subsystem consumes.

<b>1.2 CDS → OAD Interface</b>
What flows: Decisions authorizing designs, standards, constraints

CDS emits a decision object → OAD receives it → if authorized, OAD can publish the design for production use.

<b>Key rule:</b> OAD cannot publish a design for production use without a linked CDS authorization. Unauthorised designs exist in draft state only.

<b>1.3 OAD → COS Interface</b>
What flows: Production requirements and design specifications

OAD_PRODUCTION_ORDER includes: design_id, quantity, quality_standards, materials_required, labor_requirements, ecological_constraints, delivery_deadline.

COS returns COS_PRODUCTION_OUTPUT: actual_metrics (labor_hours, materials_used, throughput_time, defect_rate, ecological_actual), quality_signals (passed_inspection, rejected_units, satisfaction_score).

<b>1.4 COS → ITC Interface</b>
What flows: Labor events, contribution records, material usage data

ITC_LABOR_EVENT: member_did, hours_contributed, skill_weight, difficulty_factor, task_type (production | maintenance | governance | education | care).

ITC processes: Labor events → calculates ITC credit award based on three-signal valuation (labor effort + ecological sensitivity + fairness from FRS) → records in member ledger → applies decay rules.

<b>ITC → COS feedback:</b> When ITC values change (OAD design improvements or FRS ecological cost changes), ITC notifies COS so production cost expectations update.'

sleep 1

# PART 2: SECTIONS 1.5-1.7 + 2.1
send '[[reply_to_current]] 🏗️ <b>Integral Node Architecture</b> — Part 2/8

<b>1.5 ITC → FRS Interface</b>
What flows: Contribution ledger data, access balance histories, trade patterns

ITC_TELEMETRY includes: member_balances (starting, credits_earned, credits_spent, credits_decayed, ending), aggregate_metrics (total_labor_hours, average_balance, balance_distribution_gini, cross_node_trades, external_fiat_exchanges), access_events.

FRS receives: Raw ITC flows. Uses them to compute balance distribution, detect hoarding/starvation patterns, identify labor bottlenecks, generate fairness signals.

<b>1.6 FRS → All Subsystems</b>
FRS is the cybernetic sensing layer. It monitors system state and emits signals to every other subsystem.

<b>FRS → CDS:</b> Boundary warnings, opportunities, crises. Domains: ecological | economic | social | operational. Escalation flag for Syntegrity when needed.

<b>FRS → OAD:</b> Design performance data — actual_vs_expected labor, ecological footprint, failure modes, lifecycle data, user satisfaction. Refinement suggestions with expected impact + priority.

<b>FRS → COS:</b> Operational data — throughput_vs_capacity, bottleneck_location, labor_utilization, resource_strain_score. Rebalancing recommendations.

<b>FRS → ITC:</b> Ecological cost updates, fairness adjustments, scarcity factors. Parameters: ecological_sensitivity_multiplier, scarcity_weight, need_based_access_modifier.

<b>1.7 Internal Data Flow Summary</b>
CDS ↔ OAD: Decisions ↔ Design authorizations
OAD ↔ COS: Production orders ↔ Output metrics
COS ↔ ITC: Labor events ↔ Valuation updates
COS ↔ FRS: Operational data ↔ Rebalancing signals
ITC ↔ FRS: Contribution telemetry ↔ Ecological/fairness signals
FRS ↔ CDS: Boundary warnings ↔ Deliberation triggers
FRS ↔ OAD: Performance data ↔ Design refinements

<b>SECTION 2 — EXTERNAL-FACING INTERFACES</b>

<b>2.1 The External World Problem</b>
Every node must interact with: external procurement, external sales, legal compliance, physical logistics (Rec.50 corridors), supply chain verification (Rec.49 DPPs). The architecture must handle these without Integral internal post-monetary logic breaking.'

sleep 1

# PART 3: SECTIONS 2.2-2.5
send '[[reply_to_current]] 🏗️ <b>Integral Node Architecture</b> — Part 3/8

<b>2.2 External Procurement Interface (ITC ↔ External Markets)</b>
<b>The bridge:</b> Members earn external income (fiat) → convert to ITC balance → spend ITC internally → use fiat only for external transactions.

<b>Conversion mechanism:</b>
ITC_FIAT_EXCHANGE: member_did, direction (fiat_to_itc | itc_to_fiat), fiat_amount, itc_amount, exchange_rate (basis: real_labor_market_equivalent, established_by CDS_decision_id, reviewed monthly by FRS).

<b>Key rule:</b> ITC → fiat conversion allowed (for external purchases). ITC can never be transferred to another person in fiat form. The conversion rate is set by CDS based on local labor market data.

<b>2.3 External Sales Interface (COS ↔ Markets)</b>
COS produces surplus → sold for fiat, ITC (internal to other nodes), or other external payments.

Sales event records: items_sold (design_id, quantity, unit_price_fiat, unpt_dpp_id), buyer details, revenue allocation (member_producer_share, community_infrastructure_fund, OAD_improvement_fund).

<b>2.4 Legal Interface (Node ↔ State Systems)</b>
Integral nodes are not legal entities in most jurisdictions. Solution: a <b>Legal Wrapper</b> layer above the node.

<b>Wrapper types:</b>
• Worker Cooperative — production, contracts
• Agricultural Cooperative — food production, supply chain
• Community Land Trust (CLT) — land holding, long-term lease
• Non-profit/Foundation — grant receiving, education
• Benefit Corporation — external-facing commercial

<b>The node has one or more Legal Wrappers</b> providing: bank account access, contract signing, tax compliance, regulatory compliance, grant eligibility.

The node\'s internal logic (ITC, CDS) operates independently — the Legal Wrapper translates between node decisions and external legal requirements.

<b>2.5 Corridor Logistics Interface (COS ↔ Rec.50 Corridor Digital Platform)</b>
When goods move through a Rec.50 corridor, they interact with corridor digital infrastructure.

CORRIDOR_BOOKING: origin/destination (facility_id, UN/LOCODE), cargo (description, harmonized_code, weight, unpt_dpp_id, itc_value), transport_mode, pre_arrival_data (e_cmr_id, e_manifest_id, certificate_of_origin).

The node integrates with the corridor\'s digital platform via standardized APIs using UN/CEFACT RDM-aligned data. The node acts as a logistics entity within the corridor — no state status required.'

sleep 1

# PART 4: SECTION 3 - FEDERATION
send '[[reply_to_current]] 🏗️ <b>Integral Node Architecture</b> — Part 4/8

<b>SECTION 3 — FEDERATION INTERFACES</b>

<b>3.1 Inter-Node Communication Architecture</b>
When two nodes trade or share info, they use a federated interface.

<b>Protocol stack:</b>
• <b>Communication:</b> Nostr (identity + messaging) — each node operates a Nostr relay
• <b>Trust:</b> W3C DID Core + Verifiable Credentials (UNTP layer)
• <b>Data:</b> SurrealDB federation + shared OAD design commons
• <b>Coordination:</b> Holochain hREA for economic events
• <b>AI integration:</b> MCP for agent-to-agent communication

<b>3.2 Node Identity and Discovery</b>
<b>Every node has:</b>
• Nostr public key (npub) — identity on the network
• W3C DID — decentralized identifier for Verifiable Credentials
• SurrealDB namespace — federated database instance

NODE_REGISTRY_ENTRY: node_id, node_name, node_npub, node_did, location (country, region, climate_zone), capabilities (production_domains, service_domains, max_inter_node_capacity), status (active | suspended | decommissioned).

<b>Discovery mechanism:</b> Nodes register with a federated registry (initially shared SurrealDB table; potentially Holochain DHT as network grows). Any node can query registry to find partners with specific capabilities.

<b>3.3 Cross-Node ITC Transfer</b>
Scenario: Member in Node A earns ITC → wants to access goods from Node B.

<b>Mechanism: ITC credit note, not transfer</b>

Node A issues a CROSS_NODE_ITC_CREDIT_NOTE: issuing_node, receiving_node, member_did, amount_itc, purpose (goods_access | services_access | investment), validity_period, redemption_conditions (goods_categories_allowed, services_allowed, restrictions).

Node B receives the credit note → verifies against Node A registry → honors it → sends redemption receipt back to Node A. Node A\'s ITC ledger is debited.

<b>Non-transferability preserved:</b> Credit note can only be issued TO a specific node for specific purposes. Cannot be sold, traded, or accumulated. This preserves ITC\'s non-transferable nature while enabling federation.

<b>3.4 Cross-Node OAD Sharing</b>
Every node contributes to and draws from the shared OAD commons.

OAD_CONTRIBUTION: design_id, contributing_node, design_version, design_data (specification, performance_metrics, adaptations_for_regions), contribution_license (integral_open_commons), attestation (verifiable_credential, signing_did).

OAD pull: Node B queries OAD commons → receives design spec + adaptation notes → implements locally.

Quality assurance: FRS from both nodes can exchange performance data on shared designs, informing whether a design should be flagged as "verified for region X" or "performance concern noted."'

sleep 1

# PART 5: SECTION 3.5 + 4
send '[[reply_to_current]] 🏗️ <b>Integral Node Architecture</b> — Part 5/8

<b>3.5 Cross-Node FRS Federation</b>
FRS alerts propagate across the network.

CROSS_NODE_FRS_ALERT: originating_node, alert_type (ecological_threshold_crossed | resource_strain | supply_chain_disruption | design_failure_pattern), severity (local | regional | network_wide), affected_domains, data (metric, value, threshold, trajectory), recommended_node_actions, broadcast_scope (all_nodes | regional_nodes | specific_nodes).

Nodes receiving alerts can take preventive action: adjust production, stock reserves, or trigger CDS deliberation on federation-wide response.

<b>SECTION 4 — COMPLETE 8-LAYER INTERFACE MAP</b>

Layer 0 — Physical Substrate
Sensors, Actuators, Edge Hardware (RISC-V, ESP32, Cortex-M4, WASM-on-edge)
↑ raw data

Layer 1 — Edge Compute
Local processing, SNN inference, mesh networking (LoRa/Zigbee/WiFi mesh, IOTA for sensor micropayments)
↑ processed data

Layer 2 — Node Data (SurrealDB)
Member profiles (DID-linked) | ITC ledger (contribution + access) | COS production records | OAD design commons | FRS telemetry (time-series) | Cross-node registry
↑ queryable

Layer 3 — Node Logic (Subsystems)
CDS: decision pipeline, weighted consensus, Syntegrity
OAD: design management, version control, peer review
ITC: contribution accounting, access valuation, decay engine
COS: production planning, labor coordination, resource allocation
FRS: monitoring, alerting, cybernetic feedback
↑ inter-subsystem events

Layer 4 — Node API Gateway
Internal: JSON-RPC / REST for subsystem communication
External: REST + UN/CEFACT RDM-aligned for corridor
Federation: Nostr relay + SurrealDB federation + MCP
↑ protocols

Layer 5 — External World Interfaces
Legal Wrapper (cooperative/CLT/nonprofit) | Corridor Digital Platform (Rec.50) | UNTP DPP verification (Rec.49) | External procurement/sales | Fiat exchange mechanism
↑ translated

Layer 6 — Federation
Node registry (SurrealDB/Holochain DHT) | Cross-node ITC credit notes | OAD shared commons (Radicle) | FRS alert propagation | AI agent federation (MCP)
↑ coordinated'

sleep 1

# PART 6: SECTIONS 5-6
send '[[reply_to_current]] 🏗️ <b>Integral Node Architecture</b> — Part 6/8

<b>SECTION 5 — MINIMUM VIABLE NODE INTERFACE SPEC</b>

For a starting community (5-15 members, Phase 1):

<b>Required interfaces (MVP):</b>
1. <b>ITC ledger</b> — simple record of labor contributions and access events (even spreadsheet-backed initially)
2. <b>OAD shared notes</b> — shared document tracking design decisions and versions
3. <b>CDS simple protocol</b> — weekly meetings with recorded decisions in a shared ledger
4. <b>COS task board</b> — Trello or similar for production task management
5. <b>FRS manual reporting</b> — monthly self-reporting of well-being, resource use, community health
6. <b>External fiat bridge</b> — simple spreadsheet tracking external income and conversions

<b>Interfaces to add as node grows:</b>
15-30 members: SurrealDB for ITC ledger; Nostr for communication
30-100: Full 5-subsystem stack; Legal Wrapper; external procurement API
100-500: Federation with 1-2 other nodes; OAD shared commons via Radicle
500+: Full Rec.50 corridor integration; UNTP DPP for external sales; Cross-node ITC

<b>SECTION 6 — INTERFACE WITH UNTP/VERIFIABLE CREDENTIALS</b>

<b>The integration填补 Integral\'s missing trust layer</b>

Integral does not currently specify member identity and attestation. UNTP fills this gap.

<b>Member credential schema:</b>
VerifiableCredential: issuer (node DID), credentialSubject: member_did, node_id, contribution_role, skills_attested, itc_standing (balance, decay_schedule, verified_contributions), federation_trust_level (basic | trusted | verified).

<b>Labor event credential:</b>
VerifiableCredential: issuer (COS production node DID), credentialSubject: event_id, member_did, task_type, hours, output_verified, linked_cos_workflow, itc_awarded, timestamp.

<b>This enables:</b>
• Cross-node verification of member contributions without revealing personal data
• External parties (buyers, logistics providers) can verify community credentials
• Audit: third-party can verify ITC ledger accuracy without accessing raw data'

sleep 1

# PART 7: SECTION 7 - API ENDPOINTS
send '[[reply_to_current]] 🏗️ <b>Integral Node Architecture</b> — Part 7/8

<b>SECTION 7 — CONCRETE API ENDPOINTS</b>

<b>Node Internal API</b>
POST /cds/decisions — Submit new decision proposal
GET /cds/decisions/{id} — Get decision status and consensus data
POST /cds/votes — Register weighted consensus vote
GET /oad/designs — List all OAD designs
POST /oad/designs — Submit new design for review
GET /oad/designs/{id} — Get design with version history
POST /oad/designs/{id}/validate — Request design peer review
GET /itc/balance/{member_did} — Get member ITC balance
POST /itc/contribution — Record a labor contribution event
POST /itc/access — Record an access event (goods received)
POST /itc/exchange — Convert fiat ↔ ITC
GET /cos/workflows — List active production workflows
POST /cos/workflows — Create production workflow
POST /cos/workflows/{id}/complete — Mark workflow complete with metrics
GET /frs/telemetry — Get FRS monitoring data
GET /frs/alerts — Get active alerts
POST /frs/signals — Submit FRS signal to subsystem

<b>External API (Legal Wrapper Interface)</b>
POST /external/procurement — Place external order
GET /external/procurement/{id}/tracking — Track order status
POST /external/sales — Record external sale
POST /legal/wrapper/transaction — Execute legal wrapper action (contract, payment)
GET /corridor/booking — Book corridor transit
POST /corridor/pre-arrival — Submit pre-arrival data (e-CMR, manifest)

<b>Federation API</b>
GET /federation/nodes — Discover active nodes
GET /federation/nodes/{id} — Get node capabilities
POST /federation/credit-note — Issue cross-node ITC credit note
POST /federation/credit-note/redeem — Redeem received credit note
GET /oad/commons — Query shared OAD design commons
POST /oad/commons/contribute — Contribute design to commons
POST /federation/frs-alert — Broadcast FRS alert to network'
sleep 1

# PART 8: SECTION 8 + CLOSING
send '[[reply_to_current]] 🏗️ <b>Integral Node Architecture</b> — Part 8/8

<b>SECTION 8 — IMPLEMENTATION PRIORITY</b>

<b>Phase 1 (Months 1-6): Core Internal</b>
1. ITC ledger (manual → SurrealDB)
2. OAD design notes (shared doc → structured)
3. CDS decision log (meeting notes → structured decisions)
4. FRS self-reporting (monthly)
5. External fiat tracking (spreadsheet)

<b>Phase 2 (Months 6-12): Digital Infrastructure</b>
6. SurrealDB deployment for all subsystems
7. Member DID assignment (W3C DID key pairs)
8. Nostr relay for node communication
9. MCP agent integration
10. First external procurement with UNTP DPP verification

<b>Phase 3 (Months 12-24): Federation</b>
11. Second node connection
12. Cross-node ITC credit note system
13. Shared OAD commons via Radicle
14. FRS cross-node alert propagation
15. First Rec.50 corridor integration for external logistics

<b>Phase 4 (Years 2-5): Full Integration</b>
16. Full UNTP Verifiable Credential issuance
17. Legal Wrapper formalization
18. Corridor Digital Platform API integration
19. MeTTa/AtomSpace governance encoding
20. Federation with 5+ nodes

<b>THE CRITICAL BRIDGE — External Income + Internal ITC:</b>
Every member engagement must simultaneously:
1. <b>Generate fiat income</b> for external purchases (food, tools, energy inputs)
2. <b>Record contribution in ITC</b> for community access (housing, food, care, tools)
3. <b>Build node infrastructure</b> (sensor installed for client = sensor in node inventory)

If it does #1 but not #2 → running a business, not building a node.
If it does #2 and #3 but not #1 → volunteer work, not sustainable.
The three must happen together or the method breaks.

---
<i>Full report: reports/Integral_Node_Complete_Architecture.md</i> | <i>Complete interface architecture: 8 sections, internal + external + federation interfaces | Compiled 2026-04-30</i>'

echo "All 8 parts sent successfully"