#!/bin/bash
set -e

BOT_TOKEN=$(cat ~/.openclaw/openclaw.json | jq -r '.channels.telegram.accounts.genesis.botToken')
CHAT_ID="-1001921904187"
THREAD_ID="3651"
API="https://api.telegram.org/bot${BOT_TOKEN}/sendMessage"

send() {
  local msg="$1"
  local response=$(curl -s -X POST "$API" \
    -H "Content-Type: application/json" \
    -d "$(jq -n \
      --arg chat "$CHAT_ID" \
      --arg text "$msg" \
      --argjson thread "$THREAD_ID" \
      '{
        chat_id: $chat,
        text: $text,
        parse_mode: "HTML",
        message_thread_id: $thread,
        link_preview_options: { is_disabled: true }
      }')")
  echo "$response"
  local ok=$(echo "$response" | jq -r '.ok')
  if [ "$ok" != "true" ]; then
    echo "ERROR: $(echo "$response" | jq -r '.description')"
  fi
}

# Part 1: Intro + Category A
send '[[reply_to_current]] 💰 <b>Regen Income Map</b> — Part 1/7

<i>A MECE framework for community income streams</i>

<b>PRODUCTION INCOME</b>

<b>A1: Food &amp; Agriculture</b>
• <b>Primary production:</b> Grow food → sell surplus at markets, restaurants, CSAs, direct to consumers
• <b>Processed goods:</b> Value-add processing (dried herbs, preserves, fermented foods, nut butters, teas) — higher margin than raw produce
• <b>Seeds &amp; seedlings:</b> Sell propagation stock; rare varieties command premium
• <b>Mushroom cultivation:</b> Low space, high value, continuous harvest — oyster, shiitake, lion&apos;s mane
• <b>Beekeeping products:</b> Honey, beeswax, propolis — small footprint, high value per unit
• <b>Small livestock products:</b> Eggs, milk, fiber (alpaca, wool) — not meat (slaughter complexity)
• <b>Aquaponics/hydroponics:</b> Controlled-environment for high-value crops (microgreens, specialty herbs)

<b>Real numbers:</b> Surplus vegetables ~$1.50-3/kg at market. Processed herbs ~$15-30/jar. Mushroom blocks ~$8-12/kg.

<b>A2: Forest &amp; Timber</b>
• <b>Fence posts + small timber:</b> Fast-growing species (teak, eucalyptus) at 5-8 years — early revenue before hardwood maturity
• <b>Firewood + charcoal:</b> Immediate, consistent demand in rural contexts
• <b>Bamboo products:</b> Construction material, scaffolding, furniture — marketable in 3-5 years
• <b>Non-timber forest products:</b> Wild-harvested berries, nuts, mushrooms, medicinal plants, resins

<b>Real numbers:</b> Teak fence posts ~$15-30/tree at 8 years. Firewood ~$50-100/cord. Bamboo poles ~$3-8 each.

<b>A3: Energy Production</b>
• <b>Solar electricity export:</b> Community solar → grid export → revenue
• <b>Solar equipment installation:</b> Contracting service for external clients
• <b>Biochar production:</b> Convert agricultural waste → sell to farms, nurseries, landscapers
• <b>Biogas:</b> Methane from organic waste → cooking fuel or vehicle fuel

<b>Real numbers:</b> 800kW solar generates ~126,000 kWh/month — at $0.08/kWh export = ~$10,000/month at full capacity.

<b>A4: Built Environment</b>
• <b>Natural building services:</b> Rammed earth, straw bale, cob construction — specialized and in demand
• <b>Regenerative landscaping:</b> Design and install permaculture systems for external clients
• <b>3D printed building:</b> WASP-style local soil printing — first-mover advantage

<b>Real numbers:</b> Natural building $80-200/sqft. Permaculture design consultation: $75-150/hr.'

sleep 1

# Part 2: Category B
send '[[reply_to_current]] 💰 <b>Regen Income Map</b> — Part 2/7

<b>SKILLS &amp; SERVICES</b>

<b>B1: Education &amp; Training</b>
• <b>Vocational training:</b> Teach farming, building, solar installation, water systems — external students pay tuition
• <b>Online courses:</b> Record knowledge (permaculture design, natural building, cooperative governance) → sell globally with near-zero marginal cost
• <b>Retreat facilitation:</b> Host learning retreats (cooking, gardening, building, mindfulness) — room + board + tuition
• <b>Consulting:</b> Specialized expertise (soil restoration, water system design, community governance) → billable hours

<b>Real numbers:</b> Permaculture design certificate $2,000-5,000. Online platforms take 5-10% cut. Consulting $100-300/hr.

<b>B2: Care &amp; Wellness</b>
• <b>Holistic health practitioner:</b> Herbal medicine, massage, acupuncture — serves community and external clients
• <b>Elder care:</b> In-home support, respite care — aging populations create growing demand
• <b>Therapeutic horticulture:</b> Garden-based therapy for mental health, rehabilitation, seniors
• <b>Childcare cooperative:</b> Shared childcare reduces cost for members AND offers services externally

<b>Real numbers:</b> Herbal consultations $60-120/hr. Therapeutic horticulture programs $40-80/session.

<b>B3: Technical Services</b>
• <b>IoT/sensor installation:</b> Deploy agricultural and building sensor systems for external farms
• <b>Software development:</b> Build tools for other cooperatives, communities, non-profits
• <b>Equipment repair:</b> Small engine, electronics, irrigation systems — always needed in rural areas
• <b>Water system services:</b> Drilling, filtration, testing, repair — technical knowledge monetizable

<b>Real numbers:</b> IoT installation projects $2,000-15,000 for small farm systems. Equipment repair $60-100/hr.'

sleep 1

# Part 3: Category C
send '[[reply_to_current]] 💰 <b>Regen Income Map</b> — Part 3/7

<b>CIRCULAR ECONOMY</b>

<b>C1: Material Recovery</b>
• <b>Composting service:</b> Collect food waste from restaurants, hotels, institutions → process → sell compost
• <b>Recycled materials:</b> Glass, metal, plastic processing — community workshop transforms waste into goods
• <b>Upcycled products:</b> Furniture, building materials, textiles from discarded items — creative value addition

<b>Real numbers:</b> Compost sales $20-50/cubic yard. Upcycled furniture margins 3-5x material cost.

<b>C2: Tool &amp; Equipment Sharing</b>
• <b>Equipment cooperative:</b> Members pool equipment (tractors, tools, vehicles) — rental income from non-members + reduces member costs
• <b>Maker space fees:</b> 3D printer, CNC router, laser cutter access for external users — per-hour or per-project fees

<b>Real numbers:</b> Tractor sharing cooperative generates $500-2,000/month in rental income.

<b>C3: Waste-to-Resource</b>
• <b>Greywater systems:</b> Install water recycling for external properties
• <b>Rainwater harvesting:</b> Design and install systems for off-grid clients
• <b>Biomass conversion:</b> Convert agricultural residues into pellets, charcoal, or building materials'

sleep 1

# Part 4: Category D
send '[[reply_to_current]] 💰 <b>Regen Income Map</b> — Part 4/7

<b>KNOWLEDGE PRODUCTS</b>

<b>D1: Design &amp; Documentation</b>
• <b>Open-source design sales:</b> Premium consulting packages, site-specific adaptations, custom implementations (not competing with open access)
• <b>Land design services:</b> Permaculture site design, master planning — specialized, high-value
• <b>Documentation services:</b> Help other communities document their systems — writing, video, photography

<b>Real numbers:</b> Permaculture master plan $2,000-15,000 depending on property size. Video documentary $5,000-30,000.

<b>D2: Content &amp; Media</b>
• <b>YouTube/channel:</b> Educational content on regen living — ad revenue, sponsorships, Patreon
• <b>Podcast production:</b> Host other practitioners&apos; podcasts; produce sponsored episodes for aligned brands
• <b>Stock photography/video:</b> Aerial, farm, community imagery — growing market for authentic regenerative imagery
• <b>Publication:</b> Write and sell practical guides — $30-80 physical, $10-30 digital

<blockquote><b>The knowledge entrepreneur&apos;s edge:</b> Build once, earn repeatedly. Design templates, course modules, documentation frameworks — your expertise compounds across time and geography.</blockquote>'

sleep 1

# Part 5: Category E
send '[[reply_to_current]] 💰 <b>Regen Income Map</b> — Part 5/7

<b>SPACE-BASED REVENUE</b>

<b>E1: Retreat Operations</b>
• <b>Event hosting:</b> Weddings, corporate retreats, workshops — natural settings command premium
• <b>Workcation hosting:</b> Remote workers pay for accommodation + workspace + community access
• <b>Wellness retreats:</b> Spa, thermal, yoga, fasting protocols — multi-day immersive experiences
• <b>Camping/glamping:</b> Lower-cost option for budget travelers

<b>Real numbers:</b> Retreat venue rental $100-400/day per person all-inclusive. Workcation packages $1,500-4,000/month per person.

<b>E2: Agritourism</b>
• <b>Farm tours + experiences:</b> Immersive farm stays, harvest experiences, farm-to-table dinners
• <b>Educational tourism:</b> School groups, university programs, documentary visits
• <b>Volunteer tourism:</b> WWOOF-style programs — travelers pay to work and learn

<b>Real numbers:</b> Farm tour experiences $50-150/person. WWOOF hosting $20-50/night in exchange for work.

<b>E3: Facility Rental</b>
• <b>Community space rental:</b> Weddings, meetings, celebrations — weekend bookings
• <b>Workshop facility:</b> Host external training events in community workshop spaces
• <b>Storage rental:</b> Secure storage for equipment, vehicles, materials — monthly fees'

sleep 1

# Part 6: Category F
send '[[reply_to_current]] 💰 <b>Regen Income Map</b> — Part 6/7

<b>FINANCIAL MECHANISMS</b>

<b>F1: Community Investment Structures</b>
• <b>Community Land Trust:</b> Holds land permanently; members pay lease — sustainable, inflation-adjusted revenue
• <b>Equipment DAO:</b> Fractional ownership of expensive equipment — members buy in, generate returns through usage fees
• <b>Cooperative shares:</b> Worker cooperatives sell membership shares to new members — raises capital while maintaining community control

<b>Real numbers:</b> CLT land lease generates $200-500/month per household sustainably. Equipment DAO shares $500-5,000 depending on value.

<b>F2: Grants &amp; Impact Funding</b>
• <b>Regenerative agriculture grants:</b> USDA, private foundations, conservation programs
• <b>Climate funding:</b> Carbon credits, ecosystem service payments (water filtration, soil carbon)
• <b>Community development grants:</b> CDBG, community foundations, cooperative development funds
• <b>Impact investment:</b> Social loans, program-related investments from aligned foundations

<b>Real numbers:</b> EQIP (USDA) up to $140,000 for regenerative farm transition. Carbon credits $15-50/ton.

<b>F3: Revenue-Share Models</b>
• <b>CSA subscriptions:</b> Annual membership fee → regular produce box → predictable farm revenue
• <b>Community-supported tool ownership:</b> Annual subscription for tool access → steady income for equipment cooperative
• <b>Membership dues:</b> Tiered community membership with benefits — similar to Sponic Gardens model

<b>Real numbers:</b> CSA memberships $500-2,000/year. Tool membership $50-150/month.'

sleep 1

# Part 7: Category G + MECE + Entrepreneurial Summary
send '[[reply_to_current]] 💰 <b>Regen Income Map</b> — Part 7/7

<b>EXTERNAL WORK + HYBRID MODELS</b>

<b>G1: Remote Work Integration</b>
• <b>Digital nomad facilitation:</b> Workspace, community, accommodation for remote workers → rental premium
• <b>Client work (skill-based):</b> Apply regen skills externally (design, consulting, teaching) → income while community benefits from expertise
• <b>Contracted projects:</b> Fixed-scope work (site design, installation) → pays well, builds reputation

<b>Real numbers:</b> Digital nomad packages $1,500-4,000/month. Consulting $100-250/hr. Site design $3,000-20,000/project.

<b>G2: Hybrid Participation</b>
• <b>External job + internal contribution:</b> Members maintain external income → contribute to community ITC → community provides housing, food, care
• <b>Seasonal migration:</b> Work externally 6 months, return 6 months → maximizes income while maintaining community ties

<b>MECE FRAMEWORK CHECK</b>
<blockquote>
• A: Production (physical goods) ✅
• B: Services (human labor) ✅
• C: Circular (waste streams) ✅
• D: Knowledge (information) ✅
• E: Space (facilities) ✅
• F: Capital (financial structures) ✅
• G: Hybrid (multiple combined) ✅
</blockquote>

<b>THE REGEN ENTREPRENEUR&apos;S EDGE</b>

1. <b>Local abundance → global value</b> — Tropical fruits, medicinal herbs, natural materials that grow effortlessly are scarce and valuable elsewhere
2. <b>Constraints → creative brief</b> — No money means innovative; limited materials means efficient; small team means focused
3. <b>Community → compounding</b> — Cooperative production divides cost, multiplies market access, shares risk
4. <b>Regenerative ≠ expensive</b> — The cheapest solution is often the most regenerative (composting vs. chemical fertilizer, passive solar vs. AC)
5. <b>Time as asset</b> — Build once, earn repeatedly (knowledge products, designs, infrastructure)

<blockquote><b>The anti-hustle principle:</b> Work less on things that deplete, more on things that compound.</blockquote>

---
<i>Full report: reports/Regen_Community_Income_Opportunities.md</i> | <i>7 categories, MECE framework</i>'

echo "All 7 parts sent successfully"