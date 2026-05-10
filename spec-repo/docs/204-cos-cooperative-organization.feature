Feature: Cooperative Organization of Work and Resources

  As a member of a regenerative cooperative,
  I want the system to decompose tasks, match skills to work, allocate resources, schedule production, and generate metrics,
  so that the commons operates as a living, self-regulating organism with clear roles and transparent flows.

  Background:
    Given COS (Cooperative Organization System) manages task lifecycle and resource flows
    And COS maintains skill profiles for all active members
    And COS coordinates with ITC for contribution tracking and with OAD for design artifacts
    And cooperative formation and dissolution follow a consent-based chartering process

  @cooperative-formation
  Scenario: Members charter a new cooperative working group
    Given 5 or more members wish to form a cooperative working group
    And they have drafted a charter specifying purpose, roles, decision rules, and dissolution terms
    When CDS (Collaborative Decision System) ratifies the charter through weighted consensus
    Then COS registers the working group as an active cooperative
    And member roles are logged with their skill profiles and ITC rate agreements

  @task-decomposition
  Scenario: Complex project is decomposed into manageable tasks
    Given the cooperative has a funded project "urban-food-grid" with a 6-month timeline
    When COS decomposes the project into discrete tasks with dependencies
    Then each task has a defined deliverable, estimated hours, skill requirements, and deadline
    And task dependencies form a directed acyclic graph (DAG) in COS

  @skill-matching
  Scenario: Tasks are matched to members by verified skill profile
    Given a task "install-drip-irrigation-zone-3" requires "irrigation-design" and "plumbing-basic" skills
    And members @sauda and @taro have verified skill profiles matching these requirements
    When COS assigns the task to @sauda (first match by availability and skill alignment)
    Then @sauda receives the task assignment notification
    And the task status moves from "unassigned" to "in-progress"

  @resource-allocation
  Scenario: Cooperative allocates shared tools and materials to a task
    Given @sauda has accepted the task "install-drip-irrigation-zone-3"
    And the task requires a pipe threader, 50m of HDPE tubing, and emitter kits
    When COS checks availability from the shared tool library and material store
    Then available resources are reserved for the task duration
    And the reservation is logged in the cooperative inventory system

  @production-scheduling
  Scenario: COS generates a production schedule from task DAG
    Given all tasks for the urban-food-grid project are decomposed and assigned
    When COS generates a production schedule respecting task dependencies and member availability
    Then the schedule specifies start/end dates for each task and identifies the critical path
    And the schedule is published to all cooperative members

  @metrics-generation
  Scenario: COS generates contribution metrics for ITC
    Given the urban-food-grid project has 12 active tasks across 4 members
    And some tasks are complete, some in-progress, some delayed
    When COS generates the weekly contribution report
    Then the report includes: completed tasks per member, hours logged, ITC earned, blocked tasks, and velocity
    And the report is routed to the cooperative coordinator and ITC system

  @cooperative-dissolution
  Scenario: Working group dissolves by consent with asset reversion
    Given the urban-food-grid cooperative has completed its project charter
    Or the remaining members vote to dissolve by consent
    When CDS ratifies the dissolution decision
    Then COS archives all member contributions and ITC records
    And all assigned tools, materials, and design artifacts revert to the commons pool
    And the cooperative is marked "dissolved" with a closure report logged in the knowledge graph