#!/usr/bin/env python3
"""Reconstruct message IDs from canonical spec to find Vitali occurrences."""
import subprocess, json, time

TOKEN = "8602786638:AAGqOq4nxRpNZtEePC4wmH9sVzvvKlfOz9o"
CHAT = "-1001921904187"
START_ID = 22334
MAX_CHARS = 1800

def api(method, payload):
    r = subprocess.run(["curl","-s","-X","POST",
        f"https://api.telegram.org/bot{TOKEN}/{method}",
        "-H","Content-Type: application/json","-d",json.dumps(payload)],
        capture_output=True, text=True)
    return json.loads(r.stdout)

def edit(original_mid, new_text):
    d = api("editMessageText", {
        "chat_id": CHAT,
        "message_id": original_mid,
        "text": new_text
    })
    return d.get("ok"), d.get("description", "unknown")

MAX = 1800

def smart_chunk(lines, max_chars=MAX):
    buffer = []
    buf_len = 0
    for line in lines:
        line_len = len(line) + 1
        if not buffer:
            if line_len > max_chars:
                yield line
            else:
                buffer.append(line)
                buf_len = line_len
            continue
        if buf_len + line_len > max_chars:
            yield "\n".join(buffer)
            if line_len > max_chars:
                yield line
                buffer = []
                buf_len = 0
            else:
                buffer = [line]
                buf_len = line_len
        else:
            buffer.append(line)
            buf_len += line_len
    if buffer:
        yield "\n".join(buffer)

# Read and chunk exactly like canonical_spec.py
with open("/tmp/integral_spec_canonical.txt") as f:
    raw = f.read()

sections = raw.split("=" * 80)
header = sections[0].strip()
toc = sections[1].strip()
body = "=".join(sections[2:])
body_lines = body.split("\n")

# Build list of (msg_id, text, starts_with_section_marker)
# simulating what subagent sent
msg_id = START_ID
planned = []  # (msg_id, text, contains_vitali)

# Header
planned.append((msg_id, header, "vitali" in header.lower()))
msg_id += 1

# TOC
toc_chunks = list(smart_chunk(toc.split("\n")))
for chunk in toc_chunks:
    planned.append((msg_id, chunk, "vitali" in chunk.lower()))
    msg_id += 1

# Body
body_chunks = list(smart_chunk(body_lines))
for chunk in body_chunks:
    planned.append((msg_id, chunk, "vitali" in chunk.lower()))
    msg_id += 1

print(f"Total planned messages: {len(planned)}")
print(f"Message ID range: {planned[0][0]} to {planned[-1][0]}")
print(f"Completion message would be: {msg_id}")

vitali_hits = [(mid, text) for mid, text, has_v in planned if has_v]
print(f"\nMessages containing 'vitali': {len(vitali_hits)}")
for mid, text in vitali_hits:
    vitali_lines = [l for l in text.split('\n') if 'vitali' in l.lower()]
    print(f"  Msg {mid}: {len(vitali_lines)} lines with vitali")
    for vl in vitali_lines[:3]:
        print(f"    {vl[:100]}")
    # Show what the replacement text would be
    new_text = text.replace("Vitali Cognitive Architecture", "Cognitive Deliberation Architecture")
    new_text = new_text.replace("Vitali model", "cognitive deliberation model")
    new_text = new_text.replace("Vitali", "the cognitive architecture")
    print(f"  Replacements made: {text.count('Vitali')} -> {new_text.count('the cognitive architecture') + new_text.count('Cognitive Deliberation Architecture')}")

# Now perform the edits
print(f"\nPerforming edits...")
success = 0
fail = 0
for mid, text in vitali_hits:
    new_text = text.replace("Vitali Cognitive Architecture", "Cognitive Deliberation Architecture")
    new_text = new_text.replace("Vitali model", "cognitive deliberation model")
    new_text = new_text.replace("Vitali", "the cognitive architecture")
    
    ok, desc = edit(mid, new_text)
    if ok:
        print(f"  OK msg {mid}")
        success += 1
    else:
        print(f"  FAIL msg {mid}: {desc}")
        fail += 1
    time.sleep(0.5)

print(f"\nResults: {success} edited, {fail} failed")
