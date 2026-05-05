# HEARTBEAT.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.

## Telegram HTML Bug — FIXED

**Bug:** HTML entities like `&rsquo;` (smart quotes) and `&ldquo;/&rdquo;` (curly quotes) were getting sent as raw text in HTML parse_mode, rendering as literal text in Telegram.

**Root cause:** bash heredoc swallowed the `&rsquo;` → `'` replacement earlier. The subagent was writing HTML entities as entity names instead of Unicode code points.

**Fix used:** Python3 heredoc (`<<'PYEOF'`) to avoid bash interpretation, all strings written as actual Unicode characters.

**Prevention:** Use Python3 for all multi-message Telegram sends. Never bash heredoc for HTML content.

## Telegram Bot Token Path
- Token at: `.channels.telegram.accounts.genesis.botToken` (NESTED, not flat)
- Extract with: `jq -r ".channels.telegram.accounts.genesis.botToken" ~/.openclaw/openclaw.json`

## Memory notes
- `memory/2026-05-05.md` → 5 messages (21905-21910) about Integral TRIZ + Vitali paper synthesis

## Active subagents
- 017853c3-16c9-4410-8e9f-8ef1782e36af (telegram-compose, completed)
- fd5a3965-982d-4115-9dbe-4d8992cadd66 (triz-resolution, completed)