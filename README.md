# spike-faye-lei-dsh-skills

DeepSeek Harness (DSH) 技能合集 — 从社区收集整理的 **1300+ 技能 + 94 个 agent**，按类别分目录整理。

A curated collection of **1300+ skills and 94 agents** for [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness), organized by category.

## 目录结构 / Structure

```
skills/
├── agents/        # agent 工作流（89）
├── research/      # 科研/学术/论文（107）
├── design/        # 设计/绘图/视觉（41）
├── platforms/     # 平台集成（109）
├── dev-tools/     # 开发工具/工程流（96）
├── automation/    # Composio/Rube SaaS 自动化（812）
├── data/          # 数据/数据库/ML（16）
├── content/       # 写作/内容/职场（12）
└── other/         # 其他（113）
agents/            # agent 定义（94）
```

> 注：DSH 技能发现只支持一层深度（`<root>/<name>/SKILL.md`），所以分目录后需先 flatten 再安装。

## 安装 / Install

用 `flatten.sh` 把分目录技能铺平到 `~/.dsh/skills/`：

```sh
./flatten.sh            # 铺平到 ~/.dsh/skills/
# 或指定目标目录
./flatten.sh /path/to/dir
```

或手动：

```sh
find skills -mindepth 2 -maxdepth 2 -type d -exec cp -r {} ~/.dsh/skills/ \;
```

## 技能格式 / Format

每个技能是一个目录 `<name>/SKILL.md`，frontmatter 要求：

```yaml
---
name: kebab-case-name
description: 一句话说明何时使用
---
```

技能名必须是 kebab-case（`^[a-z0-9]+(?:-[a-z0-9]+)*$`）。

## 许可 / License

本仓库整理结构采用 MIT 许可。各技能保留其原始许可（见各 `SKILL.md` frontmatter 的 `license` 字段）。

> 注：Anthropic 官方 `docx`/`pdf`/`pptx`/`xlsx` 四个技能为专有许可（Proprietary），未收录。
