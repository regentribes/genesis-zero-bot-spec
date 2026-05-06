#!/usr/bin/env python3
import json, subprocess, time

BOT_TOKEN = subprocess.check_output(['cat', '/home/ian/.openclaw/openclaw.json'], text=True)
BOT_TOKEN = json.loads(BOT_TOKEN)['channels']['telegram']['accounts']['genesis']['botToken']
API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def send(msg):
    try:
        r = subprocess.run(['curl', '-s', '-X', 'POST', API, '-H', 'Content-Type: application/json',
               '-d', json.dumps({'chat_id': '-1001921904187', 'text': msg, 'message_thread_id': 3651})],
            capture_output=True, text=True, timeout=10)
        resp = json.loads(r.stdout)
        mid = resp.get('result', {}).get('message_id')
        if not mid:
            desc = resp.get('description','')
            print(f"ERR: {desc}")
            if 'retry after' in desc.lower():
                wait = int(''.join(filter(str.isdigit, desc)))
                print(f"Waiting {wait}s...")
                time.sleep(wait + 2)
        return mid
    except Exception as e:
        print(f"Exception: {e}")
        return None

with open('/tmp/opportunities100.json') as f:
    all_opps = json.load(f)

new_only = [o for o in all_opps if o.get('source') == 'new']

send("━━━ NEW OPPORTUNITIES (72-107) ━━━")
time.sleep(2)

for i, o in enumerate(new_only):
    num = 72 + i
    send(f"\n#{num} {o['name']} | Income: {o['income']} | Startup: {o['cost']} | Time: {o['time']} | {o['cat']} | {o.get('desc','')}")
    time.sleep(2)  # 2 second gap to avoid rate limit

time.sleep(2)
summary = """━━━ 100-OPPORTUNITY COMPLETE LIST ━━━

A1 FOOD (11): Regenerative Farming, Coop Grocery, Primary Food Production, Mushroom Cultivation, Beekeeping, Eggs & Dairy, Seedling Sales, Seed Saving, Ecotourism Guide, Permaculture Design, Water Harvesting

A2 FOREST (4): Teak Fence Posts, Firewood/Charcoal, Bamboo Products, Solar Grid Export

A3 ENERGY (3): Solar Installation, Solar Installation Contract, Biochar Production

A4 BUILT (3): Natural Building Services, Permaculture Landscaping, 3D Printed Building

B1 EDUCATION (6): Regenerative Consulting, Permaculture Certificate Courses, Online Courses, Consulting, Retreat Facilitation, Vocational Training

B2 CARE (4): Herbal Consultations, Elder Care Services, Therapeutic Horticulture, Childcare Cooperative

B3 TECHNICAL (4): IoT Sensor Installation, Equipment Repair, Water System Services, Software Development

C1 MATERIAL (5): Composting, Composting Service, Upcycled Furniture, Recycled Materials Processing, Biomass Pellet Production

C2 TOOL SHARING (3): Tool Library Op, Equipment Cooperative Rental, Maker Space Fees

C3 WASTE (2): Greywater System Install, Rainwater Harvesting Design

D1 DESIGN (2): Permaculture Master Plans, Documentary Production

D2 MEDIA (4): Video Content/YouTube, Stock Photography, Book Publication, Podcast Production

E1 RETREAT (3): Retreat Venue Rental, Workcation Hosting, Wellness Retreats

E2 AGRITOURISM (2): Farm Tour Experiences, WWOOF/Volunteer Tourism

E3 RENTAL (3): Community Space Rental, Workshop Facility Rental, Storage Rental

F1 INVESTMENT (3): CLT Lease, Equipment DAO Shares, Cooperative Membership Shares

F2 GRANTS (3): USDA EQIP Grants, Carbon Credits, Community Development Grants

F3 REVENUE-SHARE (2): CSA Subscriptions, Tool Membership Dues

G1 REMOTE (3): Digital Nomad Hosting, Client Contracting, Regen Tourism Package

G2 MIGRATION (1): Seasonal Migration Work

H INFRASTRUCTURE (9): UNTP Verification Node, DPP Issuance Service, x402 Payment Gateway, Nostr Relay Operator, Solid Pod Hosting, Holochain hApp Hosting, SurrealDB Migration Service, VC Issuer, RISC-V Edge Deployment

I TOKENIZATION (5): Physical Asset Tokenization, Equipment DAO Operator, Community Bond Issuance, Carbon Credit Tokenization, Regenerative Impact NFT

J CONSULTANCY (7): CLT Legal, Cooperative Formation, Integral Architecture Consulting, RetroPGF Strategy, Supply Chain Compliance, Regen Finance Advisor, Bio-Regional Planning

K DATA/AI (5): Community Data Marketplace, AI Agent Training, Predictive Farm Analytics, FRS Monitoring, Digital Twin Maintenance

L EMERGING (10): Seed Bank, Apothecary, Water Testing, Community Radio, Dispute Resolution, Migration Coach, Ecosystem Accounting, Repair Cafe, Community Security

TOTAL: 107 unique opportunities. Income $0-$25K/mo. Startup $0-$2M. Time 0-60 months. All Integral-aligned. All drain corporate/state system.

PICK. EXECUTE. REPEAT. 🌿⚡"""

send(summary)
print(f"\nAll sent!")