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

## AME Architecture — Metonymic Activation and Virtual Trust Field

### Context

The article "The Linguistic Sign: Metonymy and Virtuality" (DOI: 10.13092/lo.80.3565, published 2017-02-02) by Radden and Kövecses is the source.
Extended by Langacker Cognitive Grammar.
It provides a formal model for how linguistic signs activate meaning.

AME (Affinity Mapping Engine) from the Mythogen framework operates on a structurally identical mechanism.
A single detected value activates the entire relational field.
The overlap is significant enough to warrant documentation as an ADR.

### The Article: Exact Statements

DOI: https://doi.org/10.13092/lo.80.3565

Title: The Linguistic Sign: Metonymy and Virtuality

Authors: Radden and Kövecses (cognitive linguists)

Core claim:
The linguistic sign means not by direct reference to the real world.
It means by **virtually activating a trapezium-like configuration** of forms, concepts, experienced projections, and relationships.
The process is metonymic (a part activates the whole) and virtual (indirect, not literal).

Exact quote from abstract:

> "it means by virtue of the linguistic form activating (virtually) the entire trapezium-like configuration of forms, concepts, experienced projections, and relationships between all of the above.
> Activation of the real world remains dubious or indirect.
> The process is both metonymic and virtual, in the sense specified."

Key architectural elements from the article:

1. **Classical model** (Saussure): signifier ↔ signified (intimate two-term connection)
2. **Classical model** (Ogden and Richards): semiotic triangle (form → thought → reference)
3. **Radden and Kövecses extension**: the sign functions **metonymically**.
A part activates the whole triangular configuration.
4. **Further extension**: trapezium model.
Calibrated with Peirce conception of **virtuality** and Langacker Cognitive Grammar.
5. **Virtuality**: meaning is not directly present.
It is activated indirectly, through the web of relations.
The real world is not directly accessed.

Trapezium model:

```text
Form → Concept → Experienced Projections
         ↕
   Relationships (between all above)
```

The linguistic form (word) activates the concept.
The concept in turn virtually activates experienced projections and the relational network between them.
The whole configuration is engaged.
Not just the literal referent.

---

### AME Architecture: Living Seed Pattern

#### Living Seed (from AME spec)

A Living Seed is NOT a static user profile.
It is a growing entity.

```text
LivingSeed {
  needs: Vec<Need>        // survival, belonging, growth
  beliefs: Vec<Belief>     // theories about reality
  principles: Vec<Principle> // action guides
  values: Vec<Value>      // what is lived with others

  state: SeedState        // GROWING | DORMANT | BLOOMING | SEEDING
  maturity: u8            // 0-100

  fot: FOTRecord          // 5 indicators, virtual trust field
  v_crystal: VPosition    // Victor|Villain|Victim|Vengeful|Virtuous|Vulnerable

  affinities: Vec<AffinityLink>
  trust_radius: u8
}
```

#### The Four Distinctions — Architecturally Separated

AME stores four distinct types of content.
Never conflated.

| Type | Changes | Stored Separately |
|------|---------|------------------|
| **Needs** | Weekly | ✅ |
| **Beliefs** | Monthly | ✅ |
| **Principles** | Quarterly | ✅ |
| **Values** | Annually or slower | ✅ |

Values require others to practice.
The Desert Island Test: you cannot practice generosity alone.
This is the relational foundation.

#### Trust Formula

```text
Authentic Expression + Witnessed Resonance + Emotional Density = Trust Field (FOT)
```

**FOT = Field of Trust**.
A virtual field.
Not directly observable.
Inferred from 5 indicators.

| Indicator | Measures |
|-----------|----------|
| Mutual Support | Unprompted help events |
| Response Velocity | Rally speed from request to response |
| Difficult Topic | Conflict raised and resolution rate |
| Benefit Distribution | Value flow Gini coefficient |
| Psychological Safety | Unsafe disclosures and safe responses |

**Hologram Principle:**
FOT composite = `Math.min()` of all 5 indicators.
One off.
The whole field degrades.
Not averaged.

---

### The Structural Isomorphism

#### Article: Trapezium Model of Linguistic Sign

```text
Form (word)
  ↓ virtually activates
Concept
  ↓ virtually activates
Experienced Projections + Relationships
```

Activation flows through a **configuration of relations**.
The real world is not directly accessed.
Process is **metonymic** (a part activates the whole) and **virtual** (indirect).

#### AME: Living Seed Activation Model

```text
Single detected VALUE
  ↓ metonymically activates
Entire Living Seed (needs + beliefs + principles + values)
  ↓ virtually activates
FOT (virtual trust field)
  ↓ virtually activates
Affinity connections + matching
```

AME metonymic activation:
Detecting one value in a message does not just flag that value.
It activates the entire seed relational configuration.
The detected value metonymically activates the whole person.

AME virtual trust:
The FOT is not directly visible.
It is a virtual field inferred from behavioral indicators (the 5 FOT measures).
The community real trust cannot be directly measured.
It is only virtually activated through its effects.

#### Direct Mapping

| Article Concept | AME Equivalent |
|----------------|----------------|
| Linguistic form | Detected seed element (a value, a need, a belief) |
| Concept | The Living Seed — the whole person |
| Experienced projections | V-crystal position, maturity, bloom cycles |
| Relationships | Affinity links, trust radius, FOT indicators |
| Virtuality | FOT = virtual field, not directly observable |
| Metonymy | One detected element activates the whole seed |
| Trapezium | Living Seed structure: needs + beliefs + principles + values + state + FOT |

#### Key Shared Insight

The article central claim:
"activation of the real world remains dubious or indirect"

This maps directly to AME anti-capture architecture.

AME deliberately does NOT directly measure the real world.
It only measures **expression patterns**:

- What people say
- How they respond
- What they ask about

It cannot see the real person behavior directly.
It virtually activates the trust field through proxies:

- Expression count → authenticity
- Resonance detection → witnessed resonance
- Emotional density → emotional density

These are all **virtual activations**.
Not direct real-world measurements.

---

### V-Crystal and the Vulnerability Axis

AME spec adds a crucial layer not present in the article.
The **V-Crystal immune system**.

The 6 positions:

- Victor — wins/succeeds
- Villain — causes harm
- Victim — feels powerless
- Vengeful — seeks retaliation
- Virtuous — judges morally
- Vulnerable — circuit breaker (AXIS)

Key distinction (Vic Desotelle):

> "Vulnerability is the AXIS (not a point).
> Virtuous and Vengeful are the POLES.
> Victor, Villain, Victim spin around the axis.
> Dynamic and alive."

This maps to the trapezium model dynamic relationship layer.
The V-crystal position is the **experienced projection** in the trapezium.
The dynamic state that orients the seed in the relational field.

---

### Time Lock and Maturation

The article notes that virtual activation is indirect.
Meaning takes time and multiple engagements to accumulate.

AME captures this as a **30-day time lock**:

- Patterns detected less than 30 days ago are NOT used for matching.
- Seed maturity affects how much weight new signals carry.
- Trust cannot be gamed in short windows.
It accumulates through sustained virtual activation.

This is the temporal dimension of the trapezium.
Meaning (and trust) builds through repeated virtual activation.
Not through single events.

---

### Consequences

#### Positive

- The linguistic metonymy model provides theoretical grounding for why AME single-element detection is architecturally sound.
Detecting one value *should* activate the whole seed.
Because the sign works metonymically.
- The virtuality model explains why the FOT is a field (not a score).
Trust is virtually activated.
Not directly measured.
- The trapezium structure provides a design pattern for how to expand AME architecture.
Any new element (e.g., a new interaction) should virtually activate the full trapezium: form → concept → projections → relationships.
- The article distinction between real-world activation and virtual activation is the theoretical foundation for AME anti-capture design.

#### Risks

- Overfitting AME to the article model could lead to ignoring non-linguistic modalities (embodied, spatial, relational).
- V-crystal positions are not yet formally mapped to trapezium components.
This needs design work.
- The 30-day time lock may be too conservative or too lenient depending on community velocity.
Empirical tuning needed.

#### Open Questions

- Does the trapezium model suggest AME should also track "experienced projections" separately from values and beliefs?
- Can the cognitive grammar approach (Langacker) inform how AME generates Why-Cards?
Making explanations themselves metonymic?
- Should AME "membrane" (semi-permeable boundary) be mapped to the trapezium relationship layer?

---

### References

- Article: "The Linguistic Sign: Metonymy and Virtuality" — DOI 10.13092/lo.80.3565, Radden and Kövecses, Linguistik Online, 2017
- AME Implementation Guide v0.2 (github.com/regentribes/mythogen-ame/docs/AME_IMPLEMENTATION_GUIDE.md)
- AME Architecture Mythogen (~/Projects/mythogen-ame/docs/AME-Architecture-Mythogen.md)
- Singulareus Trust Field as Technology Creator (singularius-trust-field-as-technology-creator.md)
