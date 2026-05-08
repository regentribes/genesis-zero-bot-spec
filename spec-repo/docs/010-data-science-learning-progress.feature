Feature: Community Data Science Learning Tracker

  As a community member learning data science,
  I want to track my cheat sheet completion and assessment progress,
  so that I can build competency systematically and get mentorship support.

  Background:
    Given the [[sources/0019-kdnuggets-data-science-cheatsheets|KDnuggets "Complete Collection of Data Science Cheat Sheets"]] is adopted as community reference
    And the collection covers 12 categories
    And [[sources/0018-nvidia-learning-paths-2026|NVIDIA certification]] is the primary curriculum framework

  Rule: All categories are available for self-directed learning
                    Note: Some categories are more relevant to active IoT Toolkit projects
                    Note: Members may request mentorship pairing for any category

  Rule: Progress is tracked per member per category

  @progress-tracking
    Scenario: Member tracks cheat sheet completion for SQL category
      Given I am a community member with access to the learning tracker
      And I am working through the "SQL" category cheat sheets
      When I mark all SQL cheat sheets as reviewed
      Then my "SQL" category status is updated to "cheat-sheets-complete"
      And the system records the completion date for each cheat sheet

  @quiz-assessment
    Scenario: Member completes a quiz assessment for Machine Learning category
      Given I have completed the "Machine Learning" cheat sheets
      When I score 70% or higher on the ML assessment quiz
      Then my "Machine Learning" category status is updated to "assessed"
      And the system records my score and assessment date

  @quiz-assessment
    Scenario: Member fails quiz and requests reassessment
      Given I have completed the ML cheat sheets
      And I scored below 70% on the ML assessment quiz
      When I request a reassessment attempt
      Then the system creates a "reassessment-pending" status for my ML category
      And I receive a list of recommended review topics before retrying

  @mentorship-pairing
    Scenario: Member requests mentorship pairing for Deep Learning
      Given I am a community member working through the "Deep Learning" category
      And I need guidance on PyTorch, Keras, and TensorFlow workflows
      When I submit a mentorship request specifying "Deep Learning" category
      Then the system matches me with a mentor who has "Deep Learning" expertise
      And both I and the mentor receive a pairing notification

  @mentorship-pairing
    Scenario: Mentor and mentee schedule structured learning sessions
      Given I am matched with a mentor for the "NLP" category
      When my mentor and I agree on a session schedule of biweekly 1-hour calls
      Then the system creates a "mentorship-active" record for our NLP pairing
      And each session is logged with topic covered and next steps

  @project-based-assessment
    Scenario: Member applies Data Engineering skills to IoT Toolkit pipeline
      Given I am a community member working on the Farmers IoT Toolkit
      And I have been working through the "Data Engineering" cheat sheets
      When I complete a working data pipeline prototype using at least 3 of the covered tools
      Then my "Data Engineering" category status is updated to "project-assessed"
      And the prototype is logged as evidence of applied competency

  @project-based-assessment
    Scenario: Member builds a community dashboard applying BI and Data Analytics skills
      Given I have completed the "Business Intelligence" and "Data Analytics" cheat sheets
      And I have access to community metrics data
      When I build a dashboard visualization using a BI tool
      Then my "Business Intelligence" category is marked complete
      And the dashboard is linked as the project-based assessment artifact

  @curriculum-overview
    Scenario: Curriculum owner views community-wide learning progress
      Given I am a curriculum owner or community coordinator
      And community members have logged progress across categories
      When I view the learning dashboard
      Then I see aggregated completion rates per category
      And I see which categories have the most mentorship requests
      And I see which members are ready for peer teaching or mentorship roles

  @curriculum-overview
    Scenario: New member starts learning pathway from zero
      Given I am a new community member with no data science background
      When I join the learning program
      Then I am assigned the recommended starting category order
      And I am offered an optional mentorship pairing for my first category

  @assessment-recording
    Scenario: Learning progress is recorded in community knowledge graph
      Given I complete a category assessment or project
      When the system records my completion
      Then the knowledge graph is updated with my member identity and category completed
      And the assessment type and competency score or project link
      And this record is available for curriculum review and peer recognition

  # Wiki: [[sources/0019-kdnuggets-data-science-cheatsheets|KDnuggets]] provides the 12-category curriculum.
  # [[sources/0018-nvidia-learning-paths-2026|NVIDIA]] provides certification alignment.
  # See [[syntheses/wikivault-synthesis-2026-05-08|Wiki Vault Synthesis]] for Gap 5 (IoT toolkit ↔ governance verification bridge)
