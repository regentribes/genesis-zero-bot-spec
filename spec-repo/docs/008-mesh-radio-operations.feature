@regen-tribes @mesh-networking @p2p
Feature: Mesh Radio Contact Exchange
  As a regenerative community member
  I want to exchange contact information with others through mesh radio
  So that I can build my network through real-world proximity interactions

  Background:
    Given Alice operates a Holon node with mesh radio
    And Bob operates a Holon node with mesh radio
    And both devices are operational and mesh-enabled
    And heartbeat interval is 500ms with 80-400ms latency

  Scenario: Mesh discovery and identification
    Given Alice's node is broadcasting presence on mesh
    When Bob's node detects Alice's broadcast
    Then Bob sees Alice's node identifier
    And Alice sees Bob's node identifier
    And neither has internet connectivity required

  Scenario: Raft leader election on mesh
    Given 5 microgrid nodes across 2 villages on mesh radio
    And grid-east-2 is current Raft leader
    When grid-east-2 loses power
    Then remaining nodes detect absence after 2x heartbeat interval
    And a new election is triggered
    And the most-up-to-date-log node becomes leader
    And writes continue within 3 seconds of failure

  Scenario: P2P knowledge sync on mesh
    Given Alice's node has concept graph with 5,000+ concepts
    And Bob's node has a divergent concept graph
    When mesh sync initiates between Alice and Bob
    Then CRDT merge produces consistent graph on both nodes
    And no coordinator or internet is required
    And sync completes within one mesh round-trip

  Scenario: Offline message delivery
    Given Alice sends a message to Bob via mesh
    And internet is unavailable
    When the message traverses mesh hops between nodes
    Then Bob receives the message when in mesh range
    And messages are queued at intermediate nodes
    And delivery is eventual-consistent across mesh topology

  Scenario: Contact exchange via mesh proximity
    Given Alice and Bob are within mesh radio range
    When Alice initiates contact exchange
    Then exchange uses ephemeral X25519 keys for forward secrecy
    And each exchange generates a fresh session key
    And contact records are stored locally on both devices

  Scenario: Mesh network resilience
    Given a mesh network with 12 nodes across 3 villages
    When an intermediate node fails
    Then routes reconverge around the failed node
    And no single point of failure blocks mesh-wide communication
    And Raft consensus continues on surviving nodes
