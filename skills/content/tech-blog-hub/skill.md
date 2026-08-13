---
name: tech-blog-hub
description: 抓取 AI 大厂技术博客，翻译成中文，生成个人离线知识库网站
---

# Tech Blog Hub

抓取 AI 大厂（Anthropic、OpenAI、DeepMind、Meta 等）技术博客，自动翻译成中文、生成摘要和语义标签，构建可离线浏览的个人知识库网站。

## 支持的数据源（16 个）

### AI 大厂博客
| 代码 | 名称 | 类型 |
|------|------|------|
| `anthropic` | Anthropic Research | HTML |
| `openai` | OpenAI Research | HTML |
| `deepmind` | Google DeepMind | HTML |
| `meta` | Meta AI | HTML |
| `google-research` | Google Research | HTML |
| `microsoft-research` | Microsoft Research | HTML |
| `nvidia` | NVIDIA Research | HTML |
| `mistral` | Mistral AI | HTML |
| `cohere` | Cohere | HTML |
| `xai` | xAI | HTML |

### 论文/期刊
| 代码 | 名称 | 类型 |
|------|------|------|
| `arxiv-cs-ai` | arXiv cs.AI | API |
| `arxiv-cs-cl` | arXiv cs.CL | API |
| `arxiv-cs-lg` | arXiv cs.LG | API |
| `huggingface-papers` | HuggingFace Daily | API |

### 论坛/社区
| 代码 | 名称 | 类型 |
|------|------|------|
| `hackernews` | Hacker News (AI筛选) | API |
| `reddit-ml` | r/MachineLearning | API |

## 工作流程

### 第一步：抓取文章列表

用户说"抓 Anthropic 近期 10 篇"时：

```bash
python .claude/skills/tech-blog-hub/scripts/scraper.py list <source> --count <n>
```

这会输出 JSON 格式的文章列表（标题、URL、日期、摘要）。

### 第二步：逐篇抓取正文并处理

对每篇文章：

1. **抓取正文**：
   ```bash
   python .claude/skills/tech-blog-hub/scripts/scraper.py fetch <url> --source <source>
   ```
   输出英文原文（Markdown 格式）

2. **翻译成中文**：将正文翻译成流畅的中文

3. **生成摘要**：用 2-3 句话概括文章核心内容

4. **打语义标签**：从下列 16 个标签中选择最匹配的 1-3 个：
   - Agent、推理模型、MoE、RAG、风险对齐、长上下文、多模态
   - 训练基础设施、Benchmark评测、提示工程、代码生成
   - 可解释性、安全红队、数据合成、模型压缩、产品发布

### 第三步：保存数据

将每篇文章保存为 JSON 对象，追加/更新到 `output/data/articles.json`：

```json
{
  "id": "anthropic-2024-06-15-context-window",
  "source": "anthropic",
  "title": "原文标题",
  "title_zh": "中文标题",
  "url": "原文链接",
  "date": "2024-06-15",
  "summary_zh": "中文摘要",
  "content_zh": "中文翻译全文",
  "content_md": "原文Markdown",
  "tags": ["长上下文", "Agent"],
  "reading_time_min": 8
}
```

### 第四步：生成网站

```bash
python .claude/skills/tech-blog-hub/scripts/site_generator.py
```

生成 `output/site/index.html`，一个完整的离线知识库网站。

## 用法示例

- "帮我抓 Anthropic 近期 10 篇" → 只抓 Anthropic
- "帮我抓 OpenAI 和 Anthropic 最近两周的文章" → 多源抓取
- "更新知识库" → 增量抓取所有源的最新文章
- "打开知识库" → 用浏览器打开网站

## 注意事项

- 抓取频率：每次请求间隔 2 秒，避免被限流
- 翻译质量：保留技术术语的英文原文，如 "Transformer"、"RLHF"、"attention mechanism"
- 增量更新：检查 URL 是否已存在，避免重复抓取
- 离线设计：网站不依赖任何 CDN 或外部 API
