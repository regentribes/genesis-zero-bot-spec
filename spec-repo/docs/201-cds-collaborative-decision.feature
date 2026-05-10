Feature: Collaborative Decision-Making Through Syntegrity

  As a participant in a regenerative community,
  I want to systematically identify needs, draft proposals, and reach decisions that account for everyone's objections,
  so that we act with genuine collective intelligence and shared commitment.

  Background:
    Given the Integral Collective uses Syntegrity as its consensus mechanism
    And CDS (Collaborative Decision System) governs all community decisions
    And proposals pass through stages: need identification, drafting, deliberation, objection mapping, weighted consensus, escalation, authorization, logging

  @need-identification
  Scenario: Member identifies a community need
    Given a member observes an unmet need in the community
    When they submit a need statement to CDS with evidence and affected stakeholders
    Then the need is logged in the decision register with a unique ID
    And relevant working groups are notified of the new need

  @proposal-drafting
  Scenario: Working group drafts a proposal to address an identified need
    Given a need has been logged with ID "need-042"
    And a working group has been assigned ownership
    When the group drafts a proposal specifying action, resources, timeline, and success metrics
    Then the proposal is linked to the originating need in the register
    And the proposal enters the deliberation stage

  @objection-mapping
  Scenario: Deliberation surfaces a minority objection
    Given a proposal "prop-042-a" is in deliberation
    And three members raise distinct concerns
    When CDS maps each concern as an objection with severity and affected parties
    Then each objection is weighted by number of affected members and systemic impact
    And objectors receive acknowledgment with a pathway to resolution

  @weighted-consensus
  Scenario: CDS reaches weighted consensus on a low-impact decision
    Given proposal "prop-042-a" has been deliberated for 72 hours
    And objections have been addressed or overridden with documented rationale
    And no objection exceeds the escalation threshold (20% of weighted votes)
    When CDS records a "consensus-passed" outcome
    Then the decision is authorized for implementation
    And all participants receive a decision summary

  @syntegrity-escalation
  Scenario: High-impact decision triggers Syntegrity escalation
    Given a proposal affects more than 30% of active members
    And objection weight exceeds the threshold for simple consensus
    When CDS escalates the decision to Syntegrity
    Then a structured grid is convened with all affected stakeholders
    And the grid produces a resolution within a defined window (7 days)
    And the outcome is binding on all parties

  @decision-authorization
  Scenario: Authorized decision is dispatched to responsible agent
    Given a decision has passed consensus or Syntegrity
    And the decision specifies a responsible role and deadline
    When CDS records the authorization with timestamp and authorizing participants
    Then the decision is dispatched to the assigned agent or role
    And a reminder is scheduled for the deadline

  @decision-logging
  Scenario: Completed decision cycle is archived for institutional learning
    Given a decision has been implemented and a retrospective filed
    When CDS archives the complete decision record (need, proposal, objections, outcome, lessons)
    Then the archive is indexed in the commons knowledge graph
    And future decision-makers can reference precedents from this record