@regen-tribes @ostrom-principles @governance
Feature: Ostrom's 8 Principles Compliance

  The rule verifies that commons governance operations follow Ostrom's 8 principles
  for successful self-governance at any scale.

  Background:
    Given a Holon Unit operating as a local biome
    And Ostrom's 8 principles as the governance foundation

  Scenario: Boundary rules — clear membership
    Given a community commons resource
    Then the boundaries of the resource must be clearly defined
    And the individuals with rights to withdraw from the resource must be clearly defined

  Scenario: Congruence — local conditions
    Given allocation and appropriation rules
    Then rules should be adapted to local conditions
    And the costs of rules should be borne by the appropriators

  Scenario: Collective-choice arrangements — participation
    Given most affected by the commons
    Then they should be included in collective-choice arrangements
    And rules can be modified by most affected participants

  Scenario: Monitoring — accountability
    Given monitors who are accountable to the appropriators
    Then the monitors should be accountable to the appropriators
    And if they are not directly accountable, they should be the appropriators themselves

  Scenario: Graduated sanctions — proportional response
    Given rule violations by appropriators
    Then sanctions should be graduated
    And the costs of sanctions should be proportionate to the violation

  Scenario: Conflict-resolution — accessible mechanisms
    Given conflicts among appropriators
    Then low-cost conflict-resolution mechanisms should be available
    And the resolution should be rapid and binding

  Scenario: Recognized rights — nested tiers
    Given the commons operates at multiple scales
    Then the rights of appropriators to devise their own rules
    And recognized external authorities should respect those rights
    And nested tiers of organization should be permitted

  Scenario: Polycentric governance — overlapping jurisdictions
    Given multiple governance units across village, regional, and global scales
    Then polycentric governance enables efficient information flow
    And localized decision-making for local conditions
    And coordination across tiers without centralization
