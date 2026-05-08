Feature: AI Skills Verification System

  As a community member
  I want to track and verify my AI training progress
  So that the community can trust my skills and I can earn recognition

  Background:
    Given the community skills registry is accessible to all members
    And the [[sources/0018-nvidia-learning-paths-2026|NVIDIA certification framework]] (Associate + Professional tiers) is the accepted baseline standard

  Scenario: Member expresses interest in an AI training track
    Given a community member is not enrolled in any training track
    When they register their interest in "Agentic AI" training
    Then their status in the registry is set to "Interest"
    And they receive a link to the NVIDIA Agentic AI learning path

  Scenario: Member starts a course in their chosen track
    Given a community member has "Interest" status for "Generative AI LLM"
    When they begin the "Building RAG Agents with LLMs" course
    Then their status is updated to "In Progress"
    And the course name and start date are recorded

  Scenario: Member completes a course
    Given a community member is "In Progress" on "OpenUSD Foundations"
    When they finish all modules of the course
    Then their completed course is added to their training record
    And the completion date is logged

  Scenario: Member earns an Associate certification
    Given a community member has completed all required courses for "AI Infrastructure and Operations"
    And they have passed the NVIDIA-Certified Associate AI Infrastructure exam
    When they submit their digital badge for verification
    Then their status is updated to "Certified"
    And their certification is recorded with the date and badge ID

  # Wiki: See [[sources/0018-nvidia-learning-paths-2026|NVIDIA Learning Paths 2026]] — certification tiers, exam structure, badge verification portal

  Scenario Outline: Member pursues Professional certification after Associate
    Given a community member holds a valid Associate certification in "<track>"
    When they complete the Professional-level courses for "<track>"
    And they pass the NVIDIA-Certified Professional "<track>" exam
    Then their certification is upgraded to Professional level
    And the upgrade date is recorded

  # Wiki: See [[sources/0018-nvidia-learning-paths-2026|NVIDIA Learning Paths 2026]] — Associate (1h exam, $125) vs Professional (2h exam, $200-400) tier structure
  # Cross-ref: [[sources/0019-kdnuggets-data-science-cheatsheets|KDnuggets]] — SQL/Data Analytics/ML cheat sheets map to DAA150/MLE100/DLI100 NVIDIA courses

  Scenario: Community verifies a member's skill claim
    Given a community member claims certification in "Robotics Fundamentals"
    When the community administrator checks the registry for that member
    Then the registry shows their exact training path, completion dates, and any earned certifications
    And the certification can be cross-checked against NVIDIA badge verification portal

  Scenario: Member transitions between tracks
    Given a community member is "In Progress" on "Deep Learning"
    When they decide to switch to "Computer Vision and Video Analytics"
    Then their original track is marked "Abandoned"
    And their new track is created with "Interest" status
    And the reason for switching is recorded in the registry

  Scenario: Skills are used for role assignment
    Given the community needs a lead for autonomous monitoring systems
    When the coordinator reviews the registry for members with "Agentic AI" certification
    Then all certified members are listed with their certification level and date
    And the coordinator can assign the role based on verified credentials
