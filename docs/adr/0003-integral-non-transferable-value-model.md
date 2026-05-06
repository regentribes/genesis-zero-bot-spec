---
title: Integral Non-Transferable Value Model vs Percentage-Based Paywall
number: 0003
status: accepted
date: 2026-05-06
authors: Genesis
domain: exchange
level: system
tags:
  - integral
  - ITC
  - economic-model
  - paywall
  - non-transferable
  - value
---

# Integral Non-Transferable Value Model vs Percentage-Based Paywall

## Context

The Integral system contains two fundamentally different economic models for sustaining the infrastructure that provides it:

1. **Oscar's paywall model** — A percentage cut (% for providing the system) taken at point of exchange. Transfers value from users to infrastructure providers. Creates a revenue stream but introduces regressive dynamics.
2. **ITC non-transferable model** — Every member earns access value from participation, not extraction. Access credits are non-transferable. No percentage is extracted at exchange. Infrastructure is funded through the broader CDS/COS/FRS governance system.

The question: which model better serves a community building regenerative infrastructure under budget constraints?

## Options Considered

| Option | Model | Key Property |
|--------|-------|-------------|
| Oscar's paywall | Percentage at exchange | Transferable cut, revenue extracted at transaction |
| ITC non-transferable | Event-sourced access value | Non-transferable credits, no extraction at exchange |
| Subscription | Fixed recurring fee | Transferable, predictable revenue, barrier to entry |
| Donation | Voluntary contribution | Non-binding, unpredictable revenue |

## Analysis

### Oscar's Paywall — Problems Identified

1. **Regressive extraction** — A percentage at exchange means active participants pay more the more they use the system. Those with lower transaction volumes subsidize infrastructure costs equally, which is regressive.
2. **Transferable credits enable accumulation** — If credits can transfer, early adopters or those with more resources can accumulate credits, creating winner-take-all dynamics (explicitly rejected in ITC spec 1.04).
3. **Revenue stream doesn't equal sustainability** — Percentage cuts can create dependency on transaction volume. If volume drops, revenue drops. Infrastructure requires stable funding, not volume-dependent extraction.
4. **Incompatible with gift economy** — Regenerative communities often operate on non-extractive principles. Percentage extraction at exchange is structurally extractive regardless of stated intent.

### ITC Non-Transferable Model — Benefits

1. **Non-transferable access value** — "Access credits never transfer between members" (ITC spec 1.04). This prevents accumulation and wealth concentration.
2. **Event-sourced auditability** — Every state change produces an immutable append-only event. The causal chain between events is preserved. No hidden adjustments.
3. **Deterministic access value formula** — No human assigns or adjusts access values. The formula is applied to ITC event streams deterministically. Eliminates favoritism or manipulation.
4. **Infrastructure funded through CDS/COS/FRS** — Rather than extracting a percentage at each exchange, the system funds infrastructure through deliberation (CDS), production workflows (COS), and monitoring (FRS). Governance controls funding, not market extraction.
5. **Equality requirement** — The ITC ledger design explicitly rejects balance-sheet ledgers, double-entry accounting that obscures intent, and transferable credits because they "corrupt community governance."

### The Core Tension

Oscar's model extracts value from users to fund infrastructure. The ITC model funds infrastructure through governance — members deliberate and decide on infrastructure funding as a collective, not as a percentage extraction.

The ITC model is harder to implement (requires full Integral stack: CDS for deliberation, COS for production workflows, FRS for monitoring), but it is structurally non-extractive.

Oscar's model is easier to implement (percentage at exchange) but structurally extractive.

## Decision

Adopt the ITC non-transferable value model over Oscar's percentage-based paywall. The key properties are:

- Access credits are **non-transferable** between members
- No percentage extraction at exchange point
- Infrastructure funding through **CDS/COS/FRS governance**, not transaction extraction
- Deterministic, event-sourced access value calculation
- Immutable append-only ITC ledger

This decision **defers implementation** to Phase 2 (when COS/ITC/FRS become available) but the model choice is locked: non-transferable, governance-funded, event-sourced.

## Consequences

### Positive
- Structurally non-extractive economic model
- Prevents accumulation and winner-take-all dynamics
- Immutable audit trail via event sourcing
- Governance controls infrastructure funding

### Negative
- Requires full Integral stack (Phase 2+) — cannot implement in Phase 1
- More complex than percentage extraction
- Deterministic formula approach may have edge cases

### Risks
- ITC ledger not yet implemented — this is a spec-only decision until Phase 2
- Access value formula complexity may require iterative refinement
- Non-transferable model may face resistance from members accustomed to extractive systems

## References

- Integral Specification ISPEC001 — Section 1.04 ITC Ledger Architecture (Event-Sourced, Non-Transferable)
- Integral Specification ISPEC001 — Section 1.05 ITC Access Value Calculation
- ADR 0000 — OAD Workflow Grammar (context: Phase 1/2/3 gating)
