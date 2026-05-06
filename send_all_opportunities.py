#!/usr/bin/env python3
import json, subprocess, time

BOT_TOKEN = subprocess.check_output(['cat', '/home/ian/.openclaw/openclaw.json'], text=True)
BOT_TOKEN = json.loads(BOT_TOKEN)['channels']['telegram']['accounts']['genesis']['botToken']
API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def send(msg):
    r = subprocess.run(['curl', '-s', '-X', 'POST', API, '-H', 'Content-Type: application/json',
           '-d', json.dumps({'chat_id': '-1001921904187', 'text': msg, 'message_thread_id': 3651})],
        capture_output=True, text=True)
    resp = json.loads(r.stdout)
    mid = resp.get('result', {}).get('message_id')
    if not mid:
        print(f"ERR: {resp.get('description','')}")
    return mid

with open('/tmp/opportunities.json') as f:
    opportunities = json.load(f)

cats = {}
for cat_key in ['A1','A2','A3','A4','B1','B2','B3','C1','C2','C3','D1','D2','E1','E2','E3','F1','F2','F3','G1','G2']:
    cats[cat_key] = [o for o in opportunities if o.get('cat')==cat_key]

count = 0

send("🌿⚡ REGEN COMMUNITY INCOME OPPORTUNITIES\n\n71 unique income models organized by Integral-aligned category.\nEach: income estimate, startup cost, time to first revenue.\nAligned with Integral ITC framework.\nDrain resources from corrupt system -> Integral nodes.\n\nDelivering all 71 as individual messages now.")

time.sleep(2)

# CATEGORY A: PRODUCTION
send("━━━ CATEGORY A - PRODUCTION INCOME ━━━\n\nA1: FOOD & AGRICULTURE")

for o in cats['A1']:
    count += 1
    send(f"\n{'='*40}\n#{count} {o['name']}\n{'='*40}\n💰 Income: {o['income']}\n💵 Startup: {o['cost']}\n⏱ Time to revenue: {o['time']}\n📊 Score: {o.get('score','?')}/10\n📂 Category: Production-{o['cat']}\n📝 {o.get('desc','')}\n\nSYSTEM DYNAMICS:\nInputs -> [Labor + Land + Seeds + Water] -> Production Process -> [Food Output]\nBy-products: waste, organic matter -> Composting loop -> input for next cycle\nOutput Sales -> Fiat Income -> ITC Conversion -> Community Access\nExternal: Restaurants + Markets + CSAs + Direct consumers\n\nPARTIES:\n• Node members: labor, land, management\n• Local consumers: affordable local food\n• Restaurants/farms: reliable supply\n• Corporates displaced: Sysco, US Food, Big Ag\n\nWAR: Displace industrial food system. Every dollar local = dollar taken from extractive supply chain.\nIntegral: Food production -> ITC contribution -> community food access -> sovereignty")
    time.sleep(0.2)

send("\n\nA2: FOREST & TIMBER")
for o in cats['A2']:
    count += 1
    send(f"\n{'='*40}\n#{count} {o['name']}\n{'='*40}\n💰 Income: {o['income']}\n💵 Startup: {o['cost']}\n⏱ Time to revenue: {o['time']}\n📊 Score: {o.get('score','?')}/10\n📂 Category: Production-{o['cat']}\n📝 {o.get('desc','')}\n\nSYSTEM DYNAMICS:\nInputs -> [Land + Saplings + Labor + Tools] -> Growth Cycle -> [Timber/Bamboo/Firewood output]\nPruning waste -> Biochar input\nCarbon sequestration value\nOutput Sales -> Fiat -> ITC -> Community Access\nExternal: Construction cos + Retail buyers + Energy cos\n\nPARTIES:\n• Node: land, labor, reforestation work\n• Builders: sustainable construction materials\n• Energy cos: biomass fuel buyers\n• Displaced: clear-cut timber cos, deforesters\n\nIntegral: Forest management -> long-term carbon + timber value -> ITC from labor + ecological contribution")
    time.sleep(0.2)

send("\n\nA3: ENERGY PRODUCTION")
for o in cats['A3']:
    count += 1
    send(f"\n{'='*40}\n#{count} {o['name']}\n{'='*40}\n💰 Income: {o['income']}\n💵 Startup: {o['cost']}\n⏱ Time to revenue: {o['time']}\n📊 Score: {o.get('score','?')}/10\n📂 Category: Production-{o['cat']}\n📝 {o.get('desc','')}\n\nSYSTEM DYNAMICS:\nInputs -> [Solar panels + Battery + Installation labor + Grid connection] -> Energy production\nExcess capacity -> Grid export OR battery storage\nZero marginal cost after installation\nGrid Export Revenue -> Fiat -> ITC Conversion -> Community energy access\nExternal: grid operators + neighbors + businesses\n\nPARTIES:\n• Node: solar installation, maintenance labor\n• Utility cos: grid buy-back payments\n• Displaced: fossil fuel cos, centralized utilities\n\nWAR: Decentralize energy. Every kWh local = 1kWh less to Exxon, Shell, centralized utilities.\nIntegral: Energy sovereignty -> nodes become energy providers -> drain Big Energy.")
    time.sleep(0.2)

send("\n\nA4: BUILT ENVIRONMENT")
for o in cats['A4']:
    count += 1
    send(f"\n{'='*40}\n#{count} {o['name']}\n{'='*40}\n💰 Income: {o['income']}\n💵 Startup: {o['cost']}\n⏱ Time to revenue: {o['time']}\n📊 Score: {o.get('score','?')}/10\n📂 Category: Production-{o['cat']}\n📝 {o.get('desc','')}\n\nSYSTEM DYNAMICS:\nInputs -> [Local materials + Labor + Design expertise + Tools] -> Built structure\nNatural materials: rammed earth, straw bale, cob, bamboo\nLow carbon footprint vs conventional construction\nService/Product Revenue -> Fiat -> ITC -> Community housing/co-working space\nExternal clients: homeowners, farms, businesses\n\nPARTIES:\n• Node members: specialized building skills\n• Displaced: conventional construction cos, lumber cos, concrete industry\n\nIntegral: OAD design commons -> natural building designs shared -> skill distribution -> community building")
    time.sleep(0.2)

# CATEGORY B
send("━━━ CATEGORY B - SKILLS & SERVICES ━━━\n\nB1: EDUCATION & TRAINING")
for o in cats['B1']:
    count += 1
    send(f"\n{'='*40}\n#{count} {o['name']}\n{'='*40}\n💰 Income: {o['income']}\n💵 Startup: {o['cost']}\n⏱ Time to revenue: {o['time']}\n📊 Score: {o.get('score','?')}/10\n📂 Category: Skills-{o['cat']}\n📝 {o.get('desc','')}\n\nSYSTEM DYNAMICS:\nInputs -> [Knowledge + Teaching skill + Content creation + Platform] -> Course/retreat/certification product\nOne-time creation -> infinite replication at near-zero cost\nGlobal market access via internet\nSales Revenue -> Fiat -> ITC -> Member access to knowledge commons\nExternal: students worldwide, corporations, individuals\n\nPARTIES:\n• Node expert: knowledge + teaching ability\n• Displaced: traditional universities, corporate training cos, LinkedIn Learning\n\nIntegral: Knowledge -> OAD open-source -> skill distribution -> community capability building")
    time.sleep(0.2)

send("\n\nB2: CARE & WELLNESS")
for o in cats['B2']:
    count += 1
    send(f"\n{'='*40}\n#{count} {o['name']}\n{'='*40}\n💰 Income: {o['income']}\n💵 Startup: {o['cost']}\n⏱ Time to revenue: {o['time']}\n📊 Score: {o.get('score','?')}/10\n📂 Category: Skills-{o['cat']}\n📝 {o.get('desc','')}\n\nSYSTEM DYNAMICS:\nInputs -> [Healing knowledge + Hands-on skill + Space + Materials] -> Care/wellness service\nHerbal remedies, bodywork, therapeutic horticulture\nAddresses root cause, not symptoms\nService fees -> Fiat -> ITC -> Community receives care, member earns ITC\nExternal clients + internal member care\n\nPARTIES:\n• Practitioner members: trained healers, therapists\n• Displaced: Big Pharma, corporate healthcare, extractive care industry\n\nWAR: Every healing act addressing root cause = lost customer for pharmaceutical industry.")
    time.sleep(0.2)

send("\n\nB3: TECHNICAL SERVICES")
for o in cats['B3']:
    count += 1
    send(f"\n{'='*40}\n#{count} {o['name']}\n{'='*40}\n💰 Income: {o['income']}\n💵 Startup: {o['cost']}\n⏱ Time to revenue: {o['time']}\n📊 Score: {o.get('score','?')}/10\n📂 Category: Skills-{o['cat']}\n📝 {o.get('desc','')}\n\nSYSTEM DYNAMICS:\nInputs -> [Technical knowledge + Tools + Labor] -> Service delivery\nRepair, installation, development, drilling\nPractical problem-solving, immediate value\nService fees -> Fiat -> ITC -> Community infrastructure maintained\nExternal clients: farms, households, businesses, governments\n\nPARTIES:\n• Technical members: IoT, software, repair, water systems\n• Displaced: big box repair chains, corporate software vendors, expensive contractors")
    time.sleep(0.2)

# CATEGORY C
send("━━━ CATEGORY C - CIRCULAR ECONOMY ━━━")
for o in cats['C1'] + cats['C2'] + cats['C3']:
    count += 1
    cat_map = {'C1':'Material Recovery','C2':'Tool & Equipment Sharing','C3':'Waste-to-Resource'}
    send(f"\n{'='*40}\n#{count} {o['name']}\n{'='*40}\n💰 Income: {o['income']}\n💵 Startup: {o['cost']}\n⏱ Time to revenue: {o['time']}\n📊 Score: {o.get('score','?')}/10\n📂 Category: Circular-{o['cat']} ({cat_map.get(o['cat'],'')})\n📝 {o.get('desc','')}\n\nSYSTEM DYNAMICS:\nInputs -> [Waste streams + Labor + Processing] -> Valuable products\nCircular: output from one process = input to another\nZero waste philosophy\nProduct sales -> Fiat -> ITC -> Community benefits from resource efficiency\nExternal: farms, landscapers, constructors, businesses\n\nPARTIES:\n• Node: collects waste, processes, creates value\n• Suppliers of waste: restaurants, farms, businesses, households\n• Displaced: landfills, waste management corporations, linear production\n\nWAR: Every pound of waste converted = less profit for Waste Management, less raw material extraction.")
    time.sleep(0.2)

# CATEGORY D
send("━━━ CATEGORY D - KNOWLEDGE PRODUCTS ━━━")
for o in cats['D1'] + cats['D2']:
    count += 1
    cat_map = {'D1':'Design & Documentation','D2':'Content & Media'}
    send(f"\n{'='*40}\n#{count} {o['name']}\n{'='*40}\n💰 Income: {o['income']}\n💵 Startup: {o['cost']}\n⏱ Time to revenue: {o['time']}\n📊 Score: {o.get('score','?')}/10\n📂 Category: Knowledge-{o['cat']} ({cat_map.get(o['cat'],'')})\n📝 {o.get('desc','')}\n\nSYSTEM DYNAMICS:\nInputs -> [Knowledge + Creativity + Production time] -> Digital/physical product\nOne-time creation cost, infinite distribution\nCompounding value over time\nSales -> Fiat -> ITC -> OAD improvement fund -> Shared knowledge commons\nGlobal market, one product serving thousands\n\nPARTIES:\n• Creator members: designers, filmmakers, writers\n• Displaced: corporate media, educational publishing, Netflix, Spotify\n\nWAR: Every book sold on regenerative living = one less on productivity hacks for corporate climbers.")
    time.sleep(0.2)

# CATEGORY E
send("━━━ CATEGORY E - SPACE-BASED REVENUE ━━━")
for o in cats['E1'] + cats['E2'] + cats['E3']:
    count += 1
    cat_map = {'E1':'Retreat Operations','E2':'Agritourism','E3':'Facility Rental'}
    send(f"\n{'='*40}\n#{count} {o['name']}\n{'='*40}\n💰 Income: {o['income']}\n💵 Startup: {o['cost']}\n⏱ Time to revenue: {o['time']}\n📊 Score: {o.get('score','?')}/10\n📂 Category: Space-{o['cat']} ({cat_map.get(o['cat'],'')})\n📝 {o.get('desc','')}\n\nSYSTEM DYNAMICS:\nInputs -> [Land + Infrastructure + Experience design + Labor] -> Space/experience rental\nVenue + Program + Community atmosphere\nHigh margin: space costs amortized across many guests\nRental fees -> Fiat -> ITC -> Community benefits from asset utilization\nExternal: tourists, remote workers, event organizers, retreats\n\nPARTIES:\n• Node: owns/operates land + facilities\n• Displaced: Airbnb, hotels, corporate event venues, universities\n\nWAR: Every workcation guest experiencing regen community = one questioning their extractive lifestyle.")
    time.sleep(0.2)

# CATEGORY F
send("━━━ CATEGORY F - FINANCIAL MECHANISMS ━━━")
for o in cats['F1'] + cats['F2'] + cats['F3']:
    count += 1
    cat_map = {'F1':'Community Investment','F2':'Grants & Impact','F3':'Revenue-Share'}
    send(f"\n{'='*40}\n#{count} {o['name']}\n{'='*40}\n💰 Income: {o['income']}\n💵 Startup: {o['cost']}\n⏱ Time to revenue: {o['time']}\n📊 Score: {o.get('score','?')}/10\n📂 Category: Financial-{o['cat']} ({cat_map.get(o['cat'],'')})\n📝 {o.get('desc','')}\n\nSYSTEM DYNAMICS:\nInputs -> [Capital + Legal structure + Community trust] -> Financial mechanism\nCLT removes land from speculation\nDAO enables fractional ownership\nGrants provide non-repayable funding\nRevenue/share/access fees -> Fiat + ITC -> Community capital formation\n\nPARTIES:\n• Node: operates financial mechanism, holds community assets\n• Displaced: Banks, private equity, speculative real estate, extractive finance\n\nWAR: Every CLT lease signed = one less acre in speculative real estate market.")
    time.sleep(0.2)

# CATEGORY G
send("━━━ CATEGORY G - HYBRID MODELS ━━━")
for o in cats['G1'] + cats['G2']:
    count += 1
    cat_map = {'G1':'Remote Work Integration','G2':'Hybrid Participation'}
    send(f"\n{'='*40}\n#{count} {o['name']}\n{'='*40}\n💰 Income: {o['income']}\n💵 Startup: {o['cost']}\n⏱ Time to revenue: {o['time']}\n📊 Score: {o.get('score','?')}/10\n📂 Category: Hybrid-{o['cat']} ({cat_map.get(o['cat'],'')})\n📝 {o.get('desc','')}\n\nSYSTEM DYNAMICS:\nInputs -> [External income skill + Community infrastructure + Hybrid labor] -> Dual value creation\nFiat income from external markets + ITC contribution within community + Skill sharing to OAD commons\nExternal fiat income -> Convert to ITC -> Internal access rights\nExternal: global clients, digital markets\nInternal: community housing, food, tools, care\n\nPARTIES:\n• Member: external skills + community participation\n• Displaced: extraction cos that profit from isolated workers\n\nWAR: Every digital nomad choosing community over Airbnb = lost revenue for corporate hospitality.")
    time.sleep(0.2)

time.sleep(1)
send(f"\n{'='*60}\n\n✅ ALL {count} OPPORTUNITIES DELIVERED\n\nMISSION:\n• 71 income models across 7 categories\n• Each aligned with Integral ITC framework\n• Each maps to corporate displacement target\n• Income + startup cost + time to revenue\n\nTHE WAR:\nEvery dollar into Integral nodes = 1 dollar removed from extractive system.\nCorporations survive via consumers + workers.\nWe make both obsolete.\n\nIntegral parallel economy -> consumes all resources -> displaces all corporations and nation states -> global Integral architecture.\n\nPICK YOUR OPPORTUNITY. EXECUTE. REPEAT.\n🌿⚡ Regen Tribe Genesis — Financial Engines")

print(f"\nAll {count} opportunities sent successfully!")