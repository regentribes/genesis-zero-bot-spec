Feature: IoT Sensor Governance Bridge

  As a regenerative community
  I want sensor readings to verify and drive DAO governance decisions
  So that physical-world evidence grounds collective decisions in real conditions

  Background:
    Given the Farmers IoT Toolkit modules deployed: water tank sensor, soil moisture, solar powerbank, WiFi hub
    And DHT22 temperature/humidity sensors available as shared latent variables
    And the Integral Collective Node running five-subsystem governance: OAD, ITC, CDS, COS, FRS
    And SurrealDB evidence store configured as state broker
    And the Active Inference Bridge mediates sensor-to-governance flow

  Scenario: Soil moisture drops below threshold triggers irrigation governance vote
    Given soil moisture reading is 22% (below 25% threshold)
    When the Active Inference Bridge receives the sensor reading
    Then the bridge stores evidence with confidence_score 0.92 in SurrealDB
    And the bridge emits irrigation_claim to ITC
    And ITC verifies correlation with recent DHT22 humidity reading (68%)
    And ITC resolves the claim as non-contradicted within 3 seconds
    Then ITC emits verified_claim to CDS
    And CDS proposes an irrigation resource allocation vote
    When CDS vote passes with weighted consensus above 0.75
    Then CDS updates governance state with irrigation_approved
    And COS executes drip irrigation via actuator command
    And FRS records audit trail: sensor_reading → ITC_verification → CDS_vote → COS_execution

  Scenario: Water tank below 20% triggers emergency resource allocation
    Given water tank level reads 17% (below 20% emergency threshold)
    When the bridge receives the reading
    Then the bridge flags emergency_claim with priority_high
    And the bridge queries ITC for contradiction check
    And ITC cross-validates with soil moisture sensor (dry conditions confirm low tank urgency)
    And ITC emits emergency_verified_claim to CDS
    When CDS receives emergency_verified_claim
    Then CDS triggers expedited governance review (skip standard deliberation delay)
    And CDS enacts emergency water allocation from community reserves
    And COS releases allocated water volume to affected plots
    And FRS records: emergency_trigger → ITC_validation → CDS_enactment → COS_execution

  Scenario: Solar powerbank SOC low triggers energy allocation governance review
    Given solar powerbank state-of-charge reads 31% (below 40% caution threshold)
    When the bridge receives the reading
    Then the bridge emits energy_allocation_review_claim to ITC
    And ITC correlates with recent DHT22 temperature (high temp reduces battery efficiency)
    And ITC checks solar generation forecast (cloud cover predicted)
    Then ITC emits multi_factor_verified_claim to CDS
    When CDS reviews energy allocation claim
    Then CDS proposes non-critical loads reduction vote
    When vote passes
    Then CDS updates energy allocation policy
    And FRS adjusts community energy budget in next governance cycle
    And bridge marks evidence_record with governance_resolution: pending_next_cycle

  Scenario: DHT22 temperature exceeds safety range triggers system-wide pause
    Given DHT22 temperature reads 41°C (above 40°C safety threshold)
    And DHT22 humidity reads 89% (high humidity加剧 heat stress)
    When the bridge receives the reading
    Then the bridge emits safety_claim to ITC with temperature_exceedance flag
    And the bridge queries weather station data for outdoor temperature cross-validation
    When ITC confirms temperature claim (outdoor sensor reads 38°C, within validation range)
    Then ITC marks claim as temperature_verified
    And ITC emits safety_verified_claim to CDS
    When CDS receives safety_verified_claim
    Then CDS pauses all non-critical governance decisions
    And CDS alerts community via Telegram notification
    And COS suspends scheduled maintenance tasks
    And bridge stores safety_event with full evidence chain in SurrealDB

  Scenario: Sensor data contradicts DAO governance claim
    Given DAO governance claim states: irrigation water allocation is adequate
    And actual soil moisture readings are 19% (critically dry)
    When the bridge receives soil moisture reading of 19%
    Then the bridge emits contradiction_alert to ITC
    And ITC queries SurrealDB for all recent sensor readings on water allocation
    And ITC identifies systematic discrepancy: claimed adequacy vs actual dryness
    Then ITC emits contradicted_claim_notification to CDS
    When CDS receives contradicted_claim_notification
    Then CDS initiates governance recalibration process
    And CDS proposes revision of water allocation policy
    And CDS flags prior allocation vote for retrospective audit
    And FRS records: contradiction_detected → ITC_resolution → CDS_recalibration → prior_vote_audit

  Scenario: Bridge receives offline sensor data with gap
    Given water tank sensor last reported 4 hours ago
    And current time shows 31% (unchanged from last reading)
    When the bridge receives the stale reading
    Then the bridge marks evidence_record with confidence: 0.45 (degraded due to age)
    And the bridge queries ITC for missing_data_estimation
    When ITC estimates missing data using correlated DHT22 humidity trend (rising, consistent with tank consumption)
    Then ITC emits estimated_claim with confidence: 0.6
    And ITC flags the estimate for retroactive verification when sensor comes online
    And bridge stores evidence with offline_estimation flag in SurrealDB
    And CDS governance decisions using this evidence are flagged with reduced_confidence

  Scenario: Cross-module inference via shared DHT22 latent generates correlated governance claim
    Given soil moisture is 24% (borderline)
    And DHT22 temperature is 36°C (elevated)
    And DHT22 humidity is 52% (dropping)
    When the bridge receives all three readings within a 2-minute window
    Then the bridge performs cross-module inference: moisture_low ∧ temp_high ∧ humidity_drop → evaporation_stress_score: 0.87
    And the bridge aggregates correlated evidence into single governance claim
    And the bridge emits aggregated_irrigation_urgency claim to ITC
    When ITC validates the aggregated claim
    Then ITC confirms cross-module correlation strengthens claim confidence (0.87 vs 0.71 for single-sensor)
    And ITC emits high_confidence_verified_claim to CDS
    And CDS proposes irrigation vote with priority_elevated flag
    And CDS records cross_module_inference_used: true in governance state

  Scenario: DAO decision verified by retroactive sensor data
    Given DAO governance decision allocated water to Plot A three days ago
    When soil moisture sensor reports Plot A at 41% (adequate)
    And water tank sensor reports consumption consistent with allocation
    When the bridge receives Plot A readings
    Then the bridge queries FRS for governance decision reference: allocation_vote_2026-05-05
    And the bridge compares actual sensor data against claimed outcomes
    And the bridge emits retroactive_verification_claim to ITC
    When ITC confirms sensor data matches governance-decided outcomes
    Then ITC marks governance decision as verified_retroactively
    And FRS updates audit trail: decision_verified → sensor_confirms_claimed_outcome
    And CDS governance history reflects: decision_confirmed_post_hoc via sensor_verification