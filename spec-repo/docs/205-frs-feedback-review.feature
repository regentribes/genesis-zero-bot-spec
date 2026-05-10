Feature: Feedback and Review System for Institutional Learning

  As a steward of the regenerative commons,
  I want the system to continuously ingest signals, detect patterns, diagnose issues, and route recommendations to the right subsystems,
  so that the commons learns and evolves as a living institution, not a static structure.

  Background:
    Given FRS (Feedback Review System) is the perceptual layer of the Integral Collective
    And FRS ingests signals from all subsystems: CDS, OAD, ITC, COS, and external environment
    And FRS detects patterns across time horizons: real-time, weekly, quarterly, annual
    And FRS routes outputs to the appropriate subsystem or governance body

  @signal-ingestion
  Scenario: FRS ingests a real-time alert from a subsystem
    Given the water recycling subsystem reports a 15% drop in filtered water quality
    When FRS receives the alert via its signal ingestion API
    Then the signal is timestamped, tagged by domain and severity, and stored in the signal ledger
    And FRS triggers a diagnostic check for correlated environmental factors

  @pattern-detection
  Scenario: FRS detects a weekly pattern in contribution data
    Given FRS has 8 weeks of ITC contribution data across 12 members
    And member @taro's weekly contributions have declined from 8h to 2h over the last 3 weeks
    When FRS runs its weekly pattern detection
    Then FRS flags @taro's declining contribution as a pattern (not noise)
    And the flag includes a confidence score and contributing factors

  @diagnostics
  Scenario: FRS diagnoses a systemic bottleneck in task completion
    Given FRS detects that the urban-food-grid project is 3 weeks behind schedule
    And 8 of 12 tasks have been delayed by resource unavailability
    When FRS runs its diagnostic routine
    Then it identifies the shared tool library as the bottleneck (reservations exceed availability 80% of the time)
    And a diagnostic report is generated with evidence and confidence level

  @routing-to-cds
  Scenario: FRS routes a governance recommendation to CDS
    Given FRS has identified a chronic decision backlog in the commons
    And average deliberation time has exceeded the 72-hour target by 200% for 4 consecutive weeks
    When FRS routes a governance signal to CDS
    Then CDS creates a need entry for "deliberation process reform"
    And CDS assigns a working group to draft a process improvement proposal

  @routing-to-oad
  Scenario: FRS routes a design quality signal to OAD
    Given FRS pattern detection finds that designs in the "water-systems" domain fail simulation at 3x the rate of other domains
    When FRS routes a design quality signal to OAD
    Then OAD flags all water-systems designs for mandatory peer review escalation
    And OAD notifies the design authors with FRS diagnostic evidence

  @routing-to-itc
  Scenario: FRS flags a fairness anomaly in ITC distribution
    Given FRS detects that ITC distribution across members is heavily skewed (top 20% hold 80% of credits)
    And the fairness weighting has not compensated for the skew in 2 consecutive quarters
    When FRS routes a fairness signal to ITC
    Then ITC adjusts the fairness weighting parameter upward
    And the adjustment is logged with FRS evidence for CDS review

  @routing-to-cos
  Scenario: FRS detects resource conflicts across active projects
    Given two active cooperatives are competing for the same specialized tool (pipe threader)
    And tool reservation conflicts have caused 5 task delays in the last 30 days
    When FRS routes a resource conflict signal to COS
    Then COS creates a mediation task for resource scheduling
    And both cooperatives are notified of the conflict and the mediation process

  @institutional-learning
  Scenario: FRS generates an annual systemic health report
    Given FRS has 12 months of signal data across all subsystems
    When the annual review cycle is triggered
    Then FRS produces a systemic health report covering: decision velocity, design quality trends, ITC fairness index, task completion rates, and boundary metric scores
    And the report is routed to CDS for governance review and commons-wide transparency

  @boundary-monitoring
  Scenario: FRS monitors external boundary conditions for the commons
    Given the commons operates within a geographic boundary with defined ecological thresholds
    And FRS has real-time data feeds for water table level, air quality index, and soil moisture
    When any boundary metric crosses its warning threshold
    Then FRS issues a boundary alert tagged by domain and severity
    And the alert is routed to COS for operational response and to CDS for policy review if needed