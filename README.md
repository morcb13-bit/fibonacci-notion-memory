# 🧠 Fibonacci Memory Manager for Notion

> **Submission for [Notion MCP Challenge 2025](https://dev.to/devteam/join-the-notion-mcp-challenge-1500-in-prizes-73e)**  
> Based on the paper: *"Nature Forgets by Addition: A Fibonacci-Based Model for Hierarchical Memory Compression and Weighted Fractal Forgetting"*

---

## What is this?

A biologically-inspired memory management tool for Notion.  
Instead of deleting old pages, it **compresses them** into hierarchical bundles — just like human memory during sleep.

The algorithm uses the **Fibonacci sequence** to define layer capacities.  
When a layer overflows, items are bundled and pushed deeper — preserving importance while reducing detail.

```
New Pages  →  Layer 0  →  Layer 1  →  Layer 2  →  Layer 3
             (detailed)   (bundles)   (coarser)   (archives)
                 1            1           2            3
             ← recent, fine-grained        older, compressed →
```

---

## How It Works

### Fibonacci Forgetting

Each layer has a capacity defined by the Fibonacci sequence: `1, 1, 2, 3, 5, 8, 13...`

When a layer overflows:
1. All items are **bundled** (their weights summed)
2. The bundle is **pushed to the next layer**
3. This cascades downward automatically

### Weighted Fractal Extension

Each page receives a **Fibonacci weight** automatically:
- Newest page → weight `377`
- Second newest → weight `233`
- Third → weight `144`
- ...and so on

This ensures **recent, important pages stay prominent** even after compression.

---

## Demo

```
============================================================
🧠 Fibonacci Memory Manager for Notion
============================================================

📡 Fetching pages from Notion...
   12 pages retrieved

⚙️  Running Fibonacci Forgetting...

📊 Layer State:
   layer_0: [░] 0/1 (cap=1)
   layer_1: [░] 0/1 (cap=1)
   layer_2: [░░] 0/2 (cap=2)
   layer_3: [█░░] 1/3 (cap=3)
   layer_4: [░░░░░] 0/5 (cap=5)

⭐ Top 5 Most Important:
   [377] Weekly Review 2025-03
   [233] Project A Requirements
   [144] Ideas & Notes
   [ 89] Reading Log
   [ 55] Backlog

📝 Creating report in Notion...
✅ Done! Report created:
   https://notion.so/Fibonacci-Memory-Report-...
```

---

## Setup

### Requirements

- Python 3.8+
- Notion account
- Notion Integration Token

### Installation

```bash
git clone https://github.com/your-username/fibonacci-notion-memory
cd fibonacci-notion-memory
pip install -r requirements.txt
```

### Get Your Notion Token

1. Go to https://www.notion.so/profile/integrations
2. Click **New integration**
3. Name it (e.g. `fibonacci-memory`) and create
4. Copy the **Internal Integration Secret** (`ntn_...`)

### Configure

Create a `.env` file in the project folder:

```
NOTION_TOKEN=ntn_your_token_here
```

### Connect Integration to Notion Pages

In Notion, open the pages you want to manage:
1. Click `···` (top right)
2. Select **Connect to** → your integration

### Run

```bash
python fibonacci_memory.py <parent_page_id>
```

Find your page ID from the Notion URL:
```
https://www.notion.so/My-Page-abc123def456...
                                ^^^^^^^^^^^^^^^^
                                This is the page ID
```

---

## The Paper

This tool is a direct implementation of:

**"Nature Forgets by Addition: A Fibonacci-Based Model for  
Hierarchical Memory Compression and Weighted Fractal Forgetting"**  
by moroc.b13 (2024)

Read the full paper on [dev.to](https://dev.to/)

---

## License

MIT License — Copyright (c) 2024 moroc.b13
