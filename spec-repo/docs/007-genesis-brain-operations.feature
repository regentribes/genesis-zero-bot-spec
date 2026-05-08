@regen-tribes @knowledge-infrastructure @genesis-brain
Feature: Genesis Brain Knowledge Graph Operations

  The rule verifies that knowledge infrastructure operations function correctly
  for regenerative community knowledge management.

  Background:
    Given SurrealDB running at ws://127.0.0.1:8000
    And 5,000+ concepts with vector embeddings
    And NARS epistemic truth values for each concept

  Scenario Outline: Query by semantic similarity
    Given a query "<query>"
    When the system performs sparse BM25 and dense HNSW search
    And combines results using Reciprocal Rank Fusion
    Then results show 20-49% improvement over single-method retrieval

    Examples:
      | query                                |
      | nitrogen-fixing trees near water     |
      | solar power management for off-grid  |
      | Ostrom principle conflict resolution |

  Scenario: Knowledge ingestion from document
    Given a source document ingested via Kreuzberg
    When the document is processed by the pipeline
    Then concepts are extracted and stored with embeddings
    And relationships are mapped between concepts
    And the doc is linked to the source in sources/

  Scenario: Spatial addressing lookup
    Given a location expressed as graph traversal
    When the system resolves the spatial address
    Then no GPS coordinates are required
    And the address is resolved through relationship graph traversal

  Scenario: Cross-module correlation via shared latent variables
    Given DHT22 temperature/humidity sensor readings
    And soil moisture sensor readings
    And water tank level readings
    When correlated inference runs across all three modules
    Then shared weather_state is computed as latent variable
    And each module updates its Bayesian beliefs accordingly

  Scenario: Delta-consensus CRDT propagation
    Given schema change propagated via delta-consensus
    When nodes are mesh-connected with 80-400ms latency
    Then each node merges changes without global coordination
    And split-brain does not occur over mesh radio network

  Scenario: Proof-of-regeneration verification
    Given an agent claims regenerative practice
    When ecological metrics are verified as improved
    Then rewards are unlocked only after verification
    And the feedback loop connects action to outcome

  Scenario: Offline knowledge retrieval
    Given total internet blackout
    And edge nodes operating on mesh radio
    When a member queries the knowledge graph
    Then retrieval continues without cloud dependency
    And P2P sync maintains consistency across mesh
