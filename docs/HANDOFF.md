# Implementation Handoff: agent-md-query MVP (Issues #1–#4)

This document is a self-contained handoff for an implementing AI agent (Cursor, Codex,
Claude Code, etc.). Telling the agent **"`docs/HANDOFF.md` の内容に従って実装してください"**
is enough — this file points to everything else it needs to read.

The MVP (Issues #1–#4) can be implemented in a single pass: the order is sequential
(scaffold → scanner → list → format) but every design decision is already fixed in
`docs/plans/`, so no human input is required mid-way.

---

## 最初に必ず読む（実装前・順番厳守）

1. `README.md` — プロダクト目的とCLI仕様
2. `CLAUDE.md` — プロジェクト憲法（※Cursorは自動で読まないので必ず開くこと）
3. `.claude/rules/00〜40` — 詳細ルール（10:Python構成 / 20:CLI挙動 / 30:scanner /
   40:test・docs）
4. `docs/plans/README.md` — MVP全体計画・実装順序・依存・設計判断ログ・完了定義
5. `docs/plans/issue-001〜004-*.md` — 各Issueの実装計画（設計はここに確定済み）

## 実装順序（厳守・各Issueは独立コミット）

#1 scaffold → #2 scanner → #3 list --where → #4 output formats

各Issueについて以下を行う：

- 対象の `docs/plans/issue-00N-*.md` と該当 `.claude/rules` を読む
- 計画の Design / Tasks に沿って実装する
- 計画の Test plan のケースを pytest で網羅する
- そのIssue分を1コミットにまとめる（コミットメッセージに対応Issue番号を記す）

## 確定済みの設計（計画から。勝手に変えない）

- スタック: Python / `src/agent_md_query/` レイアウト / argparse / PyYAML / pytest
- 構成: cli.py(parse+dispatch) / scanner.py / matcher.py / formatter.py を純関数中心に分離
- title抽出: 本文の最初の H1（`# `）→ 無ければファイル名(stem)
- `--where`: `key=value` と `key!=value`、複数はAND、比較は文字列ベース
- missing-key: `key=value` は欠落キーにマッチしない / `key!=value` は欠落キーにマッチ
- 安全な劣化: Front Matterなし・キー欠落・不正YAMLでクラッシュさせない
- format: markdown(既定) / json / paths。paths は1行1パスのみ（装飾なし）

## 守る制約

- 実装は #1〜#4 のみ。#5/#6/#8/#9 と `docs/plans/post-mvp.md` の項目は実装しない
- `ai-hisho-os` / `workboard` / 具体的プロジェクト名・タスクID をソースにハードコードしない
  （example・fixture・docs でのみ使用可）
- 依存は最小限（argparse / PyYAML / pytest 以外を増やさない）
- 振る舞い変更には必ず pytest を追加。ネットワークは使わない
- README の例は実挙動と一致させる（ズレたらコードかREADMEの一方を直す）
- 計画で「decide and document」とある箇所（build backend、不正YAMLの具体挙動、
  JSON欠落フィールドの扱い等）は、計画の既定方針に従って決め、理由をPR本文か docstring に
  1行残す。判断が割れて自信が持てない箇所だけ、勝手に突き進まず PR本文の Notes に明示する

## 仕上げ（全Issue実装後）

1. `pytest` を全実行し、全テストがパスすることを確認
2. README の例コマンドが実際に動くことを確認
3. `python -m agent_md_query --help` と各 `list --format` の動作を確認
4. 新しいブランチ（例: `feat/mvp-implementation`）に #1〜#4 のコミットを積み、
   PR を1本作成。本文に Closes #1 / Closes #2 / Closes #3 / Closes #4 を記載

## PR本文フォーマット（`.claude/rules/40-testing-docs.md`）

```markdown
## Summary
- Issueごとに何を実装したか

## Related Issue
Closes #1
Closes #2
Closes #3
Closes #4

## Tests
- 実行した pytest コマンドと結果
- 動作確認した CLI コマンド

## Notes
- decide-and-document で下した判断とその理由
- 自信が持てなかった箇所 / フォローアップ
```

---

## 進め方の指示（コピペ用）

```text
docs/HANDOFF.md の内容に従って、MVP（Issue #1〜#4）を一度のセッションで通しで
実装してください。まず #1〜#4 の計画とIssue本文を読み、全体の実装方針を5〜8行で
要約してから実装を始めてください。途中で確認待ちはせず通しで進め、判断が割れた点
だけ最後の PR Notes にまとめてください。
```

## 補足: 一括依頼 vs 分割依頼

このHANDOFFは「1ブランチ・コミット4本・PR1本で #1〜#4 を一括Close」を前提にしている。
各Issueを個別レビューしたい場合は「仕上げ」をIssueごとのPR分割に差し替える。

一括は速いが、小さい差分での人間レビュー（`.claude/rules` / AI実行者ルールの基本）とは
トレードオフ。実験目的の場合、PR Notes の「自信が持てなかった箇所」が、後で一括 vs 分割を
振り返る比較材料になる。
