# 🎲 @randomskill/mcp-random

> **No more fake LLM dice rolls.**

Cryptographically secure randomness MCP Server for Claude Code and all MCP-compatible agents.

## The Problem

LLMs don't actually roll dice.

```
Me: "Roll a D4"
LLM: "I rolled a 2! 🎲"

Reality: It just picked the number that sounded most reasonable.
Path 2 (Analytical) gets picked 80% of the time.
```

This server fixes that — **True CSPRNG randomness, no LLM preference bias**.

## Installation

### 1. Build
```bash
cd mcp-server
npm install
npm run build
```

### 2. Add to Claude Code Config

In `~/.claude-desktop/config.json` or Claude Code settings:

```json
{
  "mcpServers": {
    "randomskill-mcp-random": {
      "command": "node",
      "args": ["/full/path/to/RandomAgent/mcp-server/dist/index.js"]
    }
  }
}
```

### 3. Restart Claude

Done! Now your Skill has TRUE randomness.

---

## Tools Available

| Tool | Purpose |
|------|---------|
| `get_all_random_seeds` | **MANDATORY FIRST STEP** — Get all 5 random seeds at once |
| `roll_dice` | Roll any dice (D4, D6, D10, D20, etc.) |
| `pick_random` | Pick N items from a list, fairly |

---

## Why This Matters

**Without this server, your "random" Skill is just LLM theater.**

This is the hardware abstraction layer for true randomness.

Works in:
- ✅ Claude Code
- ✅ Claude Desktop
- ✅ Any MCP-compatible Agent
- ✅ Cline, Roo Code, etc.
