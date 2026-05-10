Feature: Open Access Design of the Commons

  As a contributor to the regenerative commons,
  I want to submit designs, receive peer review, validate them in simulation, and publish approved work to the commons,
  so that knowledge and solutions circulate freely and improve continuously through collective scrutiny.

  Background:
    Given the Integral Collective maintains a design commons as shared infrastructure
    And OAD (Open Access Design) governs the lifecycle of every design artifact
    And designs move through stages: submission, review, simulation/validation, versioning, publication, refinement
    And FRS (Feedback Review System) signals trigger design refinement when needed

  @design-submission
  Scenario: Contributor submits a design to the commons
    Given I am a contributor with an artifact (code, schematic, protocol, or model)
    When I submit the artifact to OAD with metadata (author, domain, dependencies, license)
    Then OAD assigns a versioned design ID and records the submission timestamp
    And the artifact enters the peer review queue

  @peer-review
  Scenario: Peer reviewers assess a submitted design
    Given design "design-101" has been submitted
    And at least two reviewers have been assigned by skill matching
    When each reviewer submits an assessment (feasibility, safety, alignment with commons values)
    Then the aggregated review score is computed
    And design-101 advances to simulation if score meets the threshold
    Or design-101 is returned to the author with revision notes

  @simulation-validation
  Scenario: Design passes simulation validation
    Given design "design-101" has a review score above the acceptance threshold
    When OAD runs the design through domain-specific simulation (stress test, energy balance, safety check)
    Then simulation results are logged with pass/fail per criterion
    And design-101 is cleared for versioning if all criteria pass
    Or design-101 is flagged for revision with diagnostic output

  @version-control
  Scenario: Approved design is versioned and committed to the commons
    Given design-101 has passed simulation validation
    When OAD creates an immutable versioned entry (v1.0.0) in the commons
    Then the versioned entry includes the artifact, metadata, review scores, and simulation results
    And a diff view is available against any prior version of the same design family

  @commons-publication
  Scenario: Versioned design is published to the commons catalog
    Given design-101 has been versioned as v1.0.0
    When OAD publishes the design to the commons catalog
    Then the catalog entry includes the design ID, author, domain tags, and access license
    And the design is discoverable by domain, author, or dependency graph

  @frs-triggered-refinement
  Scenario: FRS signals trigger design refinement
    Given design-101 is live in the commons
    And FRS detects a pattern suggesting the design underperforms under real-world conditions
    When FRS routes a refinement signal to the design's author or steward
    Then OAD creates a revision branch (v1.0.1-dev) linked to the triggering FRS report
    And the author has 30 days to address the flagged issues
    And the revised design re-enters the review pipeline