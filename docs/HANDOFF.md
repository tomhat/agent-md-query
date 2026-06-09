# Implementation Handoff: agent-md-query

This document is a self-contained handoff for an implementing AI agent (Cursor, Codex,
Claude Code, etc.). Telling the agent **"`docs/HANDOFF.md` の内容に従って実装してください"**
is enough — this file points to everything else it needs to read.

> **Status**: the MVP (Issues #1–#4) is implemented and merged into `main`.
> - For the MVP flow, see **"MVP (Issues #1–#4)"** below (kept for reference).
> - For the current work, see **"Post-MVP 並行実装 (#5 / #6 / #8)"** at the bottom —
>   point each agent at its issue subsection.

---

## MVP (Issues #1–#4)

The MVP can be implemented in a single pass: the order is sequential
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

---

# Post-MVP 並行実装 (#5 / #6 / #8)

MVP は merged 済み。次は Issue **#5（タグフィルタ）/ #6（summary）/ #8（validate）** を
**並行実装**する。3件は互いに独立（いずれも `scanner` にのみ依存）なので、別ブランチ・
別PRで同時に進められる。各エージェントには、このファイルの該当 Issue サブセクションを
指定する：「`docs/HANDOFF.md` の "Issue #N" セクションに従って実装してください」。

> **#9（fixtures/docs）は今は実装しない**。#5/#6/#8 が出揃ってから最終化する方が
> README 整合の手戻りが小さい（`docs/plans/issue-009-fixtures-docs.md` 参照）。

## 並行作業の唯一の注意: `cli.py` の競合

3件とも `src/agent_md_query/cli.py` に手を入れる（#5=`--tag` 追加 / #6=`summary`
サブコマンド / #8=`validate` サブコマンド）。並行ブランチでは `cli.py` がコンフリクトする。

各エージェントは次を守ること：

- `cli.py` は **既存コードを書き換えず、追加だけ** にする（サブコマンド登録と `main` の
  dispatch 分岐の追加のみ）。
- 他ファイル（`matcher.py` / `formatter.py` / `validator.py` / `tests/*`）は重複しないので
  競合しない。
- マージは順次（#5 → #6 → #8）。2本目以降は `main` を rebase してから `cli.py` の軽微な
  追加コンフリクトを解消する。

## 全 Issue 共通ルール

- 実装前に、対象 `docs/plans/issue-00N-*.md` と Issue 本文、`CLAUDE.md`
  （※エージェントが自動で読まない場合は必ず開く）、該当 `.claude/rules` を読む。
- 担当 Issue **以外**の機能には触れない。
- ソースに `ai-hisho-os` 等の固有名をハードコードしない（example/fixture/docs のみ可）。
- 依存は増やさない（argparse / PyYAML / pytest）。ネットワーク不使用。
- 振る舞い変更には pytest を追加。`python -m pytest -q` 全パスを確認。
- 専用ブランチに実装し、`Closes #N` を含む PR を1本作成。PR 本文は
  `.claude/rules/40-testing-docs.md` のフォーマット（Summary / Related Issue / Tests / Notes）。

---

## Issue #5 — タグフィルタ

- 計画: `docs/plans/issue-005-tag-filtering.md` / ルール: `.claude/rules/20-cli-behavior.md`
- ブランチ: `feat/issue-5-tag-filtering`

実装（計画どおり）：

- `matcher.py` に `matches_tags(metadata, required_tags)` を追加。複数タグは AND、
  `tags` 欠落は安全に非マッチ、スカラ `tags` は1要素 list へ寛容変換、それ以外の型は非マッチ。
- `cli.py` の `list` サブコマンドに `--tag`（`action="append"`, `default=[]`）を追加し、
  `run_list` で `matches(...) and matches_tags(...)` により絞り込む。
- pytest: マッチ / 非マッチ / `tags` 欠落 / `--where` 併用 / 複数 `--tag`。

スコープ外: タグ式・OR・否定、summary、validate。

## Issue #6 — summary --group-by

- 計画: `docs/plans/issue-006-summary-group-by.md` / ルール: `.claude/rules/20-cli-behavior.md`
- ブランチ: `feat/issue-6-summary`

実装（計画どおり）：

- `formatter.py` に `format_summary(results, group_by)` を追加。見出しは `# Summary`、
  任意フィールドで group 化、欠落値は `(no <field>)` バケットへ（末尾ソート）、各項目は
  `- status / priority: title` と `  - file:` 行。
- 既存 `format_markdown` の公開挙動は変えない。共通化は簡素な範囲のみ（不要な抽象化はしない）。
- `cli.py` に `summary <path> --group-by <field>`（`--group-by` 必須）と `run_summary` を追加、
  `main` に dispatch 分岐を追加。path 不在は `run_list` と同じく exit 1。
- pytest: group 化 / 欠落値 / file パス出力 / 空結果。

スコープ外: ソート、`--limit`、複数 group-by、非 Markdown 出力、tag、validate。

## Issue #8 — validate（設計判断は案A確定）

- 計画: `docs/plans/issue-008-validate.md` /
  ルール: `.claude/rules/20-cli-behavior.md`, `.claude/rules/30-markdown-scanner.md`
- ブランチ: `feat/issue-8-validate`

実装（計画どおり）：

- `validator.py` を新規追加：
  `RECOMMENDED_FIELDS = ("type","id","project","status","priority","updated_at")`、
  `missing_fields(metadata)`（欠落＝キー無し or `None`/空文字、schema 順）、`validate(results)`。
- `cli.py` に `validate <path>` と `run_validate` を追加、`main` に dispatch 追加。
  出力は `OK: <path>` / `MISSING: <path> -> f1, f2`。全件 OK で exit 0、欠落ありで exit 1
  （exit code は `main([...])` 経由でテストする）。
- **設計判断＝案A確定**：不正 YAML ファイルは `scanner` が skip+warn する現挙動のまま。
  validate では警告止まりとし、検証失敗扱いにしない（`scanner` は改修しない）。
- pytest: 全件有効→exit0 / 無効含む→`MISSING:` 出力＋exit1 / Front Matter 無し→全推奨
  フィールド MISSING。

スコープ外: 値（enum）検証、設定可能スキーマ、auto-fix、JSON 出力、tag、summary。

---

## 進め方の指示（コピペ用・並行）

各エージェントへ個別に：

```text
docs/HANDOFF.md の "Issue #5" セクションに従って、Issue #5 だけを実装してください。
まず該当 plan と Issue 本文を読み、実装方針を3〜5行で要約してから進めてください。
cli.py は既存コードを書き換えず追加だけにし、Closes #5 を含む PR を作成してください。
```

（#6 は "Issue #6" と `Closes #6`、#8 は "Issue #8" と `Closes #8` に置換）
