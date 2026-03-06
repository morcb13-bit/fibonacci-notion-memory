---
title: Fibonacci Memory Manager for Notion — 自然は足し算で忘れる
published: true
tags: notionchallenge, devchallenge, mcp, ai
---

## 作ったもの

**フィボナッチ数列**を使ってNotionのページを自動圧縮・整理するツールです。人間の睡眠中の記憶整理メカニズムからインスパイアされています。

古いページを削除する代わりに、**階層的なバンドルに圧縮**します。重要度を保ちながら詳細を減らす — 深いレイヤーほど古く、粗い記憶になります。

**GitHub:** https://github.com/morcb13-bit/fibonacci-notion-memory

---

## アイデアの源泉：自然は足し算で忘れる

人間の記憶は削除しません — 圧縮します。睡眠中、脳は経験を再整理し、重要でない詳細を深いレイヤーへ押しやりながら、最近の重要な記憶を鮮明に保ちます。

このアイデアを論文にまとめました：

> *「Nature Forgets by Addition: A Fibonacci-Based Model for Hierarchical Memory Compression and Weighted Fractal Forgetting」*

核心的な洞察：**フィボナッチ数列（1, 1, 2, 3, 5, 8, 13...）** は足し算だけで自然な成長を定義します。同じ原理をメモリ圧縮に応用できます。

---

## 仕組み

### Fibonacciレイヤー

各レイヤーの容量はフィボナッチ数列で定義されます：

```
Layer 0: 容量 1  ← 最新、最も詳細
Layer 1: 容量 1
Layer 2: 容量 2
Layer 3: 容量 3
Layer 4: 容量 5  ← 最古、最も圧縮
```

レイヤーが満杯になると、アイテムは**バンドル化**されて次のレイヤーへ — 自動的にカスケードします。

### 重みつきフラクタル拡張

各Notionページには自動的に**フィボナッチ重み**が付与されます：

```
最新ページ  → 重み 377
2番目      → 重み 233
3番目      → 重み 144
...
```

これにより、最近の重要なページは圧縮後も**目立ち続けます**。

### Notion API連携

このツールはNotionワークスペースに直接接続し、ページを読み込み、Fibonacci圧縮アルゴリズムを実行し、構造化された**メモリレポート**を自動的にNotionに書き戻します。

---

## デモ

```
============================================================
🧠 Fibonacci Memory Manager for Notion
============================================================

📡 Notionからページを取得中...
   12 ページ取得完了

⚙️  Fibonacci Forgettingを実行中...

📊 レイヤー状態:
   layer_0: [░] 0/1 (cap=1)
   layer_1: [░] 0/1 (cap=1)
   layer_2: [░░] 0/2 (cap=2)
   layer_3: [█░░] 1/3 (cap=3)
   layer_4: [░░░░░] 0/5 (cap=5)

⭐ 重要度TOP5:
   [377] 週次レビュー 2025-03
   [233] プロジェクト要件定義
   [144] アイデアメモ
   [ 89] 読書ノート
   [ 55] バックログ

📝 Notionにレポートを作成中...
✅ 完了！Notionにレポートが作成されました。
```

Notionに自動作成されるレポート：

```
## 概要
取得ページ数: 12
アルゴリズム: Fibonacci Forgetting (Weighted Fractal Extension)

## レイヤー状態
- layer_0: 0/1 (容量=1)
- layer_1: 0/1 (容量=1)
- layer_2: 0/2 (容量=2)
- layer_3: 1/3 (容量=3)

## 重要度Top10（Fibonacci重みづけ）
- [377] 週次レビュー 2025-03
- [233] プロジェクト要件定義
...

## 参考論文
Nature Forgets by Addition
by moroc.b13 (2024)
```

---

## セットアップ

```bash
git clone https://github.com/morcb13-bit/fibonacci-notion-memory
cd fibonacci-notion-memory
pip install -r requirements.txt
```

`.env` ファイルを作成：
```
NOTION_TOKEN=ntn_あなたのトークン
```

実行：
```bash
python fibonacci_memory.py <notionページID>
```

---

## なぜこれが重要か

多くの生産性ツールは情報過多を**削除**で解決します — アーカイブ、ゴミ箱、消去。

しかし生物学的システムは削除しません。**目的を持って圧縮します** — 重要なものを保ち、そうでないものを抽象化します。

Fibonacci ForgettingはこのアイデアをNotionワークスペースに持ち込みます：
- 手動アーカイブ不要
- 重要度が自動的に保持される
- フラクタルのように自己組織化

これこそが「human-in-the-loop」AIワークフローのあるべき姿です — あなたと*共に*働くインテリジェントな圧縮。

---

## 論文

dev.toの元論文: [Nature Forgets by Addition](https://dev.to/)

GitHub: https://github.com/morcb13-bit/fibonacci-notion-memory

**Notion MCP Challenge 2025** への応募作品 🏆
