Feature: Integral Time Credits Across the Commons

  As a participant in the regenerative commons,
  I want to record contributions, receive fair credit weighted by skill and difficulty, and spend credits to access shared resources,
  so that labor, ecology, and fairness are all honored in how the commons values and distributes its wealth.

  Background:
    Given ITC (Integral Time Credits) is the value accounting system of the Integral Collective
    And ITC credits are earned through contributions logged and verified by the cooperative
    And ITC balances are computed from labor value, ecological impact, and fairness weighting
    And credits are extinguished when spent, with safeguards against hoarding and decay for inactivity

  @contribution-logging
  Scenario: Member logs a contribution to the cooperative
    Given I am a member who has completed a task assigned by the cooperative
    When I submit a contribution record with task ID, hours, description, and timestamp
    Then the record is pending verification by a peer or coordinator
    And the task's COS (Cooperative Organization System) entry is updated to "completed"

  @verification
  Scenario: Peer verifies a contribution record
    Given contribution record "contrib-789" is pending verification
    And I am a peer reviewer with relevant domain knowledge
    When I confirm the contribution matches the task description and quality standards
    Then contrib-789 is marked "verified"
    And the contribution moves to ITC weighting calculation

  @skill-difficulty-weighting
  Scenario: ITC computes weighted credit value for a verified contribution
    Given contrib-789 is verified with 4 hours of logged time
    And the task is classified as "skilled" with difficulty factor 1.5
    And the contributor's verified skill level is "intermediate"
    When ITC calculates the weighted credit value
    Then the base hours are multiplied by difficulty factor and skill multiplier
    And the resulting ITC amount is recorded in the contributor's account

  @itc-recording
  Scenario: Weighted ITC is recorded in member's account
    Given ITC has computed 6.0 weighted credits for contrib-789
    When ITC records the credit in member @mira's account
    Then the account balance is incremented by 6.0 ITC
    And the transaction is logged with contributor, contribution, and computation breakdown

  @access-value-computation
  Scenario: Commons computes access cost for a shared resource
    Given member @mira requests access to the community solar array
    And the solar array has an access value computed from labor, ecology, and fairness
    When the cooperative calculates the access cost
    Then the cost reflects: energy production labor, ecological footprint of the installation, and equitable access surcharge
    And the total is expressed in ITC

  @credit-extinguishing
  Scenario: Member spends ITC to access a commons resource
    Given @mira has a balance of 20.0 ITC
    And the solar array access costs 5.0 ITC per month
    When @mira requests access and the cooperative approves
    Then 5.0 ITC is extinguished from @mira's account
    And the extinguished credits are recorded as "commons benefit" (redistributed to the solar maintenance pool)

  @decay-safeguard
  Scenario: Inactive account balance decays after 12 months of no contributions
    Given @mira's account has a balance of 15.0 ITC
    And @mira has made zero contributions in the last 12 months
    When the quarterly decay check runs
    Then @mira's balance is reduced by 10% (to 13.5 ITC)
    And a re-engagement prompt is sent to @mira
    And the decayed amount is released to the commons equity pool

  @decay-safeguard
  Scenario: Active contribution resets the decay clock
    Given @mira's account is subject to decay
    When @mira submits and verifies a new contribution
    Then the decay clock for @mira's account is reset to zero months
    And @mira's next contribution begins accruing ITC normally