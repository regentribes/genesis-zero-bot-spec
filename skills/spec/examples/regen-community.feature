Feature: Community Knowledge Query
  As a regenerative community member
  I want to query the knowledge base using natural language
  So that I can find relevant practices and observations without technical expertise

  Scenario: Query soil observation by parcel
    Given the field worker is located at parcel L-14
    And the soil observation report contains pH=6.2, organic_matter=3.8%
    When the worker submits the observation via SMS gateway
    Then the knowledge graph stores the observation with metadata parcel=L-14
    And the worker receives species recommendations within 30 seconds

  Scenario: Request similar conditions search
    Given the member asks "nitrogen-fixing trees near waterlogged soil"
    When the system performs sparse BM25 search and dense HNSW search
    And combines results using Reciprocal Rank Fusion
    Then results show 20-49% improvement over single-method retrieval
    And individual token matches are honored even when full-sequence similarity is lower

  Scenario: Adaptive dimension search on low-power device
    Given a field worker on a 2W solar rig queries "species compatible with parcel L-19"
    And the query specifies a latency budget under 5ms
    When the system performs adaptive-dimension search at coarseness level 384
    Then results return with 75% less compute
    And the system falls back to full 1536-dimension search only if needed

  Scenario: Raft leader election after power failure
    Given 5 microgrid nodes across 2 villages with mesh radio communication at 80-400ms latency
    And grid-east-2 (current Raft leader) loses power due to grid fault
    When remaining nodes detect absence after 2x heartbeat interval (1000ms)
    Then a new election is triggered
    And the most-up-to-date-log node (grid-east-3) becomes the new leader
    And writes continue without requiring full re-election
    And the system recovers to full read/write availability within 3 seconds

  Scenario: CRDT schema change propagation across mesh network
    Given the community adds a new "biomass_density" field to soil observations
    And this schema change must propagate to all 12 nodes across village A, B, and C
    When delta-consensus propagates the schema change via CRDT
    Then each node's local change merges without coordination (no global lock required)
    And the merged schema change is consistent across all nodes (no split-brain)
    And the CRDT ensures this works even with out-of-order message arrival over mesh radio
