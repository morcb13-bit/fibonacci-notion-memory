"""
Fibonacci Memory Manager for Notion
====================================
Fibonacci Forgetting アルゴリズムを使って
Notionのページを階層的に圧縮・整理するツール

論文: "Nature Forgets by Addition: A Fibonacci-Based Model for
       Hierarchical Memory Compression and Weighted Fractal Forgetting"
著者: moroc.b13
"""

import os
import json
import requests
from datetime import datetime
from typing import Any, Optional
from dotenv import load_dotenv

load_dotenv()
# ============================================================
# 設定（.envファイルまたは環境変数から読み込み）
# ============================================================
NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
NOTION_VERSION = "2022-06-28"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": NOTION_VERSION,
}

# ============================================================
# Fibonacci Forgetting コア実装
# ============================================================
FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
FIB_WEIGHTS = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377][::-1]


class FibonacciLayer:
    """単一レイヤーのFibonacciメモリ"""

    def __init__(self, level: int, max_depth: int = 6):
        self.level = level
        self.max_depth = max_depth
        self.items: list[dict] = []
        self.bundles: list[dict] = []
        self.capacity = FIB[min(level, len(FIB) - 1)]

    def add(self, item: dict) -> Optional[dict]:
        """アイテムを追加。オーバーフロー時はバンドルを返す"""
        weight_idx = min(len(self.items), len(FIB_WEIGHTS) - 1)
        item["weight"] = FIB_WEIGHTS[weight_idx]
        self.items.append(item)

        if len(self.items) > self.capacity:
            return self._bundle()
        return None

    def _bundle(self) -> dict:
        """アイテムをバンドル化して圧縮する"""
        total_weight = sum(i.get("weight", 1) for i in self.items)
        bundle = {
            "type": "bundle",
            "level": self.level,
            "count": len(self.items),
            "total_weight": total_weight,
            "items": self.items[:],
            "created_at": datetime.now().isoformat(),
        }
        self.items.clear()
        return bundle


class FibonacciNotionMemory:
    """
    Fibonacci Forgetting × Notion MCP 統合システム

    NotionページをFibonacciアルゴリズムで自動整理:
    - Layer 0: 最新ページ（詳細保持）
    - Layer 1: 小バンドル（軽い圧縮）
    - Layer 2+: 大バンドル（深い圧縮）
    """

    def __init__(self, depth: int = 5):
        self.layers = [FibonacciLayer(i) for i in range(depth)]
        self.depth = depth

    def ingest(self, page: dict) -> list[str]:
        """
        ページを取り込み、Fibonacci圧縮を実行。
        Returns: 実行されたアクションのログ
        """
        logs = []
        bundle = self.layers[0].add(page)
        logs.append(f"📥 Layer 0 に追加: {page.get('title', 'Untitled')} (weight={page.get('weight')})")

        level = 0
        while bundle and level < self.depth - 1:
            level += 1
            logs.append(f"🔀 Layer {level-1} → Layer {level} にバンドル転送 (count={bundle['count']}, weight={bundle['total_weight']})")
            next_bundle = self.layers[level].add(bundle)
            bundle = next_bundle

        return logs

    def state_summary(self) -> dict:
        """各レイヤーの状態サマリーを返す"""
        return {
            f"layer_{i}": {
                "capacity": layer.capacity,
                "items": len(layer.items),
                "utilization": f"{len(layer.items)}/{layer.capacity}",
            }
            for i, layer in enumerate(self.layers)
        }

    def get_important_items(self, top_n: int = 10) -> list[dict]:
        """重要度順（weight降順）でアイテムを取得"""
        all_items = []
        for layer in self.layers:
            all_items.extend(layer.items)
        all_items.sort(key=lambda x: x.get("weight", 0), reverse=True)
        return all_items[:top_n]


# ============================================================
# Notion API ユーティリティ
# ============================================================

def search_notion_pages(query: str = "", max_results: int = 20) -> list[dict]:
    """Notion MCPを通じてページを検索"""
    url = "https://api.notion.com/v1/search"
    payload = {
        "query": query,
        "filter": {"value": "page", "property": "object"},
        "page_size": max_results,
        "sort": {"direction": "descending", "timestamp": "last_edited_time"},
    }
    resp = requests.post(url, headers=HEADERS, json=payload)
    resp.raise_for_status()
    return resp.json().get("results", [])


def extract_page_info(notion_page: dict) -> dict:
    """NotionページオブジェクトからFibonacci用情報を抽出"""
    props = notion_page.get("properties", {})

    # タイトル取得（各種プロパティ形式に対応）
    title = "Untitled"
    for key in ["Name", "Title", "title"]:
        if key in props:
            rich = props[key].get("title", props[key].get("rich_text", []))
            if rich:
                title = rich[0].get("plain_text", "Untitled")
                break

    return {
        "id": notion_page["id"],
        "title": title,
        "url": notion_page.get("url", ""),
        "last_edited": notion_page.get("last_edited_time", ""),
        "created": notion_page.get("created_time", ""),
        "parent_type": notion_page.get("parent", {}).get("type", "unknown"),
    }


def create_notion_page(parent_page_id: str, title: str, content_md: str) -> dict:
    """Notionに新しいページを作成（バンドルレポート用）"""
    url = "https://api.notion.com/v1/pages"

    # Markdownをシンプルなブロックに変換
    lines = content_md.strip().split("\n")
    blocks = []
    for line in lines[:90]:  # Notion API制限: 100ブロックまで
        if line.startswith("## "):
            blocks.append({"object": "block", "type": "heading_2",
                           "heading_2": {"rich_text": [{"type": "text", "text": {"content": line[3:]}}]}})
        elif line.startswith("### "):
            blocks.append({"object": "block", "type": "heading_3",
                           "heading_3": {"rich_text": [{"type": "text", "text": {"content": line[4:]}}]}})
        elif line.startswith("- "):
            blocks.append({"object": "block", "type": "bulleted_list_item",
                           "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": line[2:]}}]}})
        elif line.strip():
            blocks.append({"object": "block", "type": "paragraph",
                           "paragraph": {"rich_text": [{"type": "text", "text": {"content": line}}]}})

    payload = {
        "parent": {"page_id": parent_page_id},
        "properties": {
            "title": {"title": [{"type": "text", "text": {"content": title}}]}
        },
        "children": blocks,
    }
    resp = requests.post(url, headers=HEADERS, json=payload)
    resp.raise_for_status()
    return resp.json()


# ============================================================
# メイン実行
# ============================================================

def run_fibonacci_manager(parent_page_id: str, search_query: str = ""):
    """
    Fibonacci Memory Manager のメイン処理

    Args:
        parent_page_id: バンドルレポートを作成するNotionページのID
        search_query: 対象ページの検索クエリ（空なら全ページ）
    """
    print("=" * 60)
    print("🧠 Fibonacci Memory Manager for Notion")
    print("=" * 60)

    # 1. Notionからページを取得
    print("\n📡 Notionからページを取得中...")
    notion_pages = search_notion_pages(query=search_query, max_results=30)
    print(f"   {len(notion_pages)} ページ取得完了")

    # 2. Fibonacci Memoryに投入
    print("\n⚙️  Fibonacci Forgettingを実行中...")
    memory = FibonacciNotionMemory(depth=5)

    all_logs = []
    for np in notion_pages:
        page_info = extract_page_info(np)
        logs = memory.ingest(page_info)
        all_logs.extend(logs)

    # 3. 結果表示
    print("\n📊 レイヤー状態:")
    for layer_key, info in memory.state_summary().items():
        bar = "█" * info["items"] + "░" * (info["capacity"] - info["items"])
        print(f"   {layer_key}: [{bar}] {info['utilization']} (cap={info['capacity']})")

    print("\n⭐ 重要度TOP5:")
    for item in memory.get_important_items(5):
        print(f"   [{item.get('weight'):>3}] {item.get('title', 'Untitled')}")

    # 4. Notionにレポートページを作成
    print("\n📝 Notionにレポートを作成中...")
    report_content = _build_report(memory, all_logs, notion_pages)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    report_title = f"🧠 Fibonacci Memory Report — {timestamp}"

    created = create_notion_page(parent_page_id, report_title, report_content)
    print(f"\n✅ 完了！Notionにレポートを作成しました:")
    print(f"   {created.get('url', '')}")

    return memory


def _build_report(memory: FibonacciNotionMemory, logs: list[str], pages: list[dict]) -> str:
    """レポートのMarkdownを生成"""
    lines = [
        f"## 概要",
        f"取得ページ数: {len(pages)}",
        f"実行時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"アルゴリズム: Fibonacci Forgetting (Weighted Fractal Extension)",
        "",
        "## レイヤー状態",
    ]
    for layer_key, info in memory.state_summary().items():
        lines.append(f"- {layer_key}: {info['utilization']} (容量={info['capacity']})")

    lines += ["", "## 重要度Top10（Fibonacci重みづけ）"]
    for item in memory.get_important_items(10):
        lines.append(f"- [{item.get('weight'):>3}] {item.get('title', 'Untitled')}")

    lines += ["", "## 処理ログ（抜粋）"]
    for log in logs[:20]:
        lines.append(f"- {log}")

    lines += [
        "",
        "## 参考論文",
        "Nature Forgets by Addition: A Fibonacci-Based Model for",
        "Hierarchical Memory Compression and Weighted Fractal Forgetting",
        "by moroc.b13 (2024)",
    ]
    return "\n".join(lines)


# ============================================================
# エントリーポイント
# ============================================================
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("使い方: python fibonacci_memory.py <parent_page_id> [search_query]")
        print("")
        print("例:")
        print("  python fibonacci_memory.py abc123def456  ")
        print("  python fibonacci_memory.py abc123def456 'プロジェクト'")
        sys.exit(1)

    page_id = sys.argv[1].replace("-", "")
    query = sys.argv[2] if len(sys.argv) > 2 else ""

    run_fibonacci_manager(page_id, query)
