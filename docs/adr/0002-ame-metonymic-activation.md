---
title: AME Architecture — Metonymic Activation and Virtual Trust Field
number: 0002
status: accepted
date: 2026-05-06
authors: Genesis
domain: information
level: organ
tags:
  - AME
  - affinity-mapping
  - metonymy
  - virtuality
  - trust-field
  - linguistics
---

# AME Architecture — Metonymic Activation and Virtual Trust Field

## Context

The article "The Linguistic Sign: Metonymy and Virtuality" (DOI: 10.13092/lo.80.3565, published 2017-02-02) by Radden and Kövecses, extended by Langacker's Cognitive Grammar, provides a formal model for how linguistic signs activate meaning. AME (Affinity Mapping Engine) from the Mythogen framework operates on a structurally identical mechanism: a single detected value activates the entire relational field. The overlap is significant enough to warrant documentation as an ADR.

## The Article: Exact Statements

**DOI:** https://doi.org/10.13092/lo.80.3565

**Title:** The Linguistic Sign: Metonymy and Virtuality

**Authors:** Radden & Kövecses (cognitive linguists)

**Core claim:** The linguistic sign means not by direct reference to the real world, but by **virtually activating a trapezium-like configuration** of forms, concepts, experienced projections, and relationships. The process is metonymic (a part activates the whole) and virtual (indirect, not literal).

**Exact quote from abstract:**
> "it means by virtue of the linguistic form activating (virtually) the entire trapezium-like configuration of forms, concepts, experienced projections, and relationships between all of the above. Activation of the real world remains dubious or indirect. The process is both metonymic and virtual, in the sense specified."

**Key architectural elements from the article:**

1. **Classical model** (Saussure): signifier ↔ signified (intimate two-term connection)
2. **Classical model** (Ogden & Richards): semiotic triangle (form → thought → reference)
3. **Radden & Kövecses extension**: the sign functions **metonymically** — a part activates the whole triangular configuration
4. **Further extension**: trapezium model calibrated with Peirce's conception of **virtuality** and Langacker's Cognitive Grammar
5. **Virtuality**: meaning is not directly present — it is activated indirectly, through the web of relations. The real world is not directly accessed.

**Trapezium model:**
```
Form → Concept → Experienced Projections
         ↕
   Relationships (between all above)
```

The linguistic form (word) activates the concept, which in turn virtually activates experienced projections and the relational network between them. The whole configuration is engaged, not just the literal referent.

---

## AME Architecture: Living Seed Pattern

### Living Seed (from AME spec)

A Living Seed is NOT a static user profile. It is a growing entity with:

```
LivingSeed {
  needs: Vec<Need>        // survival, belonging, growth
  beliefs: Vec<Belief>     // theories about reality
  principles: Vec<Principle> // action guides
  values: Vec<Value>       // what is lived with others

  state: SeedState         // GROWING | DORMANT | BLOOMING | SEEDING
  maturity: u8             // 0-100

  fot: FOTRecord           // 5 indicators, virtual trust field
  v_crystal: VPosition     // Victor|Villain|Victim|Vengeful|Virtuous|Vulnerable

  affinities: Vec<AffinityLink>
  trust_radius: u8
}
```

### The Four Distinctions — Architecturally Separated

AME stores four distinct types of content, never conflated:

| Type | Changes | Stored Separately |
|------|---------|------------------|
| **Needs** | Weekly | ✅ |
| **Beliefs** | Monthly | ✅ |
| **Principles** | Quarterly | ✅ |
| **Values** | Annually or slower | ✅ |

Values require others to practice (Desert Island Test: you cannot practice generosity alone). This is the relational foundation.

### Trust Formula

```
Authentic Expression + Witnessed Resonance + Emotional Density = Trust Field (FOT)
```

**FOT = Field of Trust** — a virtual field. Not directly observable. Inferred from 5 indicators:

| Indicator | Measures |
|-----------|----------|
| Mutual Support | Unprompted help events |
| Response Velocity | Rally speed from request to response |
| Difficult Topic | Conflict raised + resolution rate |
| Benefit Distribution | Value flow Gini coefficient |
| Psychological Safety | Unsafe disclosures / safe responses |

**Hologram Principle:** FOT composite = `Math.min()` of all 5 indicators — one off, the whole field degrades. Not averaged.

---

## The Structural Isomorphism

### Article: Trapezium Model of Linguistic Sign

```
Form (word)
  ↓ virtually activates
Concept
  ↓ virtually activates
Experienced Projections + Relationships
```

Activation flows through a **configuration of relations**. The real world is not directly accessed. Process is **metonymic** (a part activates the whole) and **virtual** (indirect).

### AME: Living Seed Activation Model

```
Single detected VALUE
  ↓ metonymically activates
Entire Living Seed (needs + beliefs + principles + values)
  ↓ virtually activates
FOT (virtual trust field)
  ↓ virtually activates
Affinity connections + matching
```

**AME's metonymic activation:** Detecting one value in a message doesn't just flag that value — it activates the entire seed's relational configuration. The detected value metonymically activates the whole person.

**AME's virtual trust:** The FOT is not directly visible. It is a virtual field inferred from behavioral indicators (the 5 FOT measures). The community's real trust cannot be directly measured — only virtually activated through its effects.

### Direct Mapping

| Article Concept | AME Equivalent |
|----------------|----------------|
| Linguistic form | Detected seed element (a value, a need, a belief) |
| Concept | The Living Seed — the whole person |
| Experienced projections | V-crystal position, maturity, bloom cycles |
| Relationships | Affinity links, trust radius, FOT indicators |
| Virtuality | FOT = virtual field, not directly observable |
| Metonymy | One detected element activates the whole seed |
| Trapezium | Living Seed structure: needs + beliefs + principles + values + state + FOT |

### Key Shared Insight

The article's central claim — "activation of the real world remains dubious or indirect" — maps directly to AME's anti-capture architecture:

AME deliberately does NOT directly measure the real world. It only measures **expression patterns** — what people say, how they respond, what they ask about. It cannot see the real person's behavior directly. It virtually activates the trust field through proxies:

- Expression count → authenticity
- Resonance detection → witnessed resonance
- Emotional density → emotional density

These are all **virtual activations**, not direct real-world measurements.

---

## V-Crystal and the Vulnerability Axis

The AME spec adds a crucial layer not present in the article: the **V-Crystal immune system**.

**The 6 positions:**
- Victor — wins/succeeds
- Villain — causes harm
- Victim — feels powerless
- Vengeful — seeks retaliation
- Virtuous — judges morally
- Vulnerable — circuit breaker (AXIS)

**Key distinction (Vic Desotelle):**
> "Vulnerability is the AXIS (not a point), with Virtuous and Vengeful as the POLES, and Victor, Villain, Victim spinning around the axis — dynamic and alive."

This maps to the trapezium model's dynamic relationship layer — the V-crystal position is the **experienced projection** in the trapezium, the dynamic state that orients the seed in the relational field.

---

## Time Lock and Maturation

The article notes that virtual activation is indirect — meaning takes time and multiple engagements to accumulate. AME captures this as a **30-day time lock**:

- Patterns detected < 30 days ago NOT used for matching
- Seed maturity affects how much weight new signals carry
- Trust cannot be gamed in short windows — it accumulates through sustained virtual activation

This is the temporal dimension of the trapezium: meaning (and trust) builds through repeated virtual activation, not through single events.

---

## Consequences

### Positive

- The linguistic metonymy model provides theoretical grounding for why AME's single-element detection is architecturally sound — detecting one value *should* activate the whole seed, because the sign works metonymically
- The virtuality model explains why the FOT is a field (not a score) — trust is virtually activated, not directly measured
- The trapezium structure provides a design pattern for how to expand AME's architecture: any new element (e.g., a new interaction) should virtually activate the full trapezium (form → concept → projections → relationships)
- The article's distinction between real-world activation and virtual activation is the theoretical foundation for AME's anti-capture design

### Risks

- Overfitting AME to the article's model could lead to ignoring non-linguistic modalities (embodied, spatial, relational)
- V-crystal positions are not yet formally mapped to trapezium components — this needs design work
- The 30-day time lock may be too conservative or too lenient depending on community velocity — empirical tuning needed

### Open Questions

- Does the trapezium model suggest AME should also track "experienced projections" separately from values and beliefs?
- Can the cognitive grammar approach (Langacker) inform how AME generates Why-Cards — making explanations themselves metonymic?
- Should AME's "membrane" (semi-permeable boundary) be mapped to the trapezium's relationship layer?

---

## References

- Article: "The Linguistic Sign: Metonymy and Virtuality" — DOI 10.13092/lo.80.3565, Radden & Kövecses, Linguistik Online, 2017
- AME Implementation Guide v0.2 (github.com/regentribes/mythogen-ame/docs/AME_IMPLEMENTATION_GUIDE.md)
- AME Architecture Mythogen (~/Projects/mythogen-ame/docs/AME-Architecture-Mythogen.md)
- Singulareus Trust Field as Technology Creator (singularius-trust-field-as-technology-creator.md)