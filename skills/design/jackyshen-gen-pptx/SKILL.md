---
name: jackyshen-gen-pptx
description: "Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations, with color palettes of UPerform company; reading, parsing, or extracting text from any .pptx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates, layouts, speaker notes, or comments. Trigger whenever the user mentions \"deck,\" \"slides,\" \"presentation,\" \"幻灯片,\" \"PPT,\" or references a .pptx filename, regardless of what they plan to do with the content afterward. If a .pptx file needs to be opened, created, or touched, use this skill."
author: JackyShen
argument-hint: "[-t THEME] [-noIMG] [-noQA]"
---


# /pptx [-t THEME] [-noIMG] [-noQA] 

生成指定风格的pptx格式幻灯片。

- 不带参数：调度所有任务步骤。
- 参数`-t THEME`：指定[配色方案](#配色方案)
- 参数`-noIMG`：不使用文生图skill进行配图
- 参数`-noQA`：跳过QA步骤

## 快速参考

| 任务 | 指南 |
|------|-------|
| 读取/分析内容 | `python -m markitdown presentation.pptx` |
| 编辑或从模板创建 | 阅读 [editing.md](editing.md) |
| 从零开始创建 | 阅读 [creating.md](creating.md) |

---

## 读取内容

```bash
# 文本提取
python -m markitdown presentation.pptx

# 可视化概览
python scripts/thumbnail.py presentation.pptx

# 原始 XML
python scripts/office/unpack.py presentation.pptx unpacked/
```

---

## 编辑工作的流程

**完整详情请阅读 [editing.md](editing.md)。**

1. 用 `thumbnail.py` 分析模板
2. 解包 → 操作幻灯片 → 编辑内容 → 清理 → 打包

---

## 从零开始创建

**完整详情请阅读 [creating.md](creating.md)。**

当没有模板或参考演示文稿时使用。

---

## 设计思路

**不要制作无聊的幻灯片。** 白底上的纯要点列表不会给任何人留下深刻印象。考虑从这个列表中为每张幻灯片获取灵感。

### 开始前

- **选择一个醒目且与内容相关的配色方案**：配色应该感觉是为这个主题量身定制的。如果把配色换到完全不同的演示文稿中仍然能"work"，说明你的选择还不够具体。
- **主次分明**：一种颜色应该占主导地位（60-70% 的视觉权重），搭配 1-2 种辅助色调和一种锐利的强调色。永远不要给所有颜色同等权重。
- **深浅对比**：标题页和结论页用深色背景，内容页用浅色背景（"三明治"结构）。或者全程使用深色以营造高级感。
- **坚持一个视觉主题**：选择一个独特的元素并重复使用——圆角图片边框、放在彩色圆形中的图标、粗的单侧边框。在每张幻灯片上保持一致。

### 配色方案

选择与主题匹配的配色——不要默认使用通用蓝色。用这些配色方案作为灵感：

缺省默认主题色是**优普丰(UPerform)**

| 主题 | 主色 | 辅助色 | 强调色 |
|-------|---------|-----------|--------|
| **优普丰(UPerform)** | `#0A2540` (深海蓝) | `#1E4976` （海洋蓝）  | `#D4AF37` (尊贵金) |
| **午夜高管** #1E2761`（藏青） #CADCFC`（冰蓝） #FFFFFF`（白） |
| **森林与苔藓** #2C5F2D`（森林绿） #97BC62`（苔藓绿） #F5F5F5`（奶油白） |
| **珊瑚活力** #F96167`（珊瑚红） #F9E795`（金色） #2F3C7E`（藏青） |
| **暖色陶土** #B85042`（陶土红） #E7E8D1`（沙色） #A7BEAE`（鼠尾草绿） |
| **海洋渐变** #065A82`（深蓝） #1C7293`（蓝绿） #21295C`（午夜蓝） |
| **炭灰极简** #36454F`（炭灰） #F2F2F2`（米白） #212121`（黑） |
| **青绿信任** #028090`（青绿） #00A896`（海沫绿） #02C39A`（薄荷绿） |
| **浆果与奶油** #6D2E46`（浆果紫） #A26769`（暗玫瑰） #ECE2D0`（奶油色） |
| **鼠尾草宁静** #84B59F`（鼠尾草绿） #69A297`（桉树绿） #50808E`（石板灰） |
| **樱桃大胆** #990011`（樱桃红） #FCF6F5`（米白） #2F3C7E`（藏青） |


**配色原则：**
- **主导色占60-70%视觉权重**，1-2个辅助色，1个强调色
- 避免所有颜色等权重分配
- 深色背景用于标题和结尾页，浅色用于内容页（”三明治”结构）
- 选一个独特的视觉元素并在每页重复使用


### 对于每张幻灯片

**每张幻灯片都需要一个视觉元素**——图片、图表、图标或形状。纯文字幻灯片容易被遗忘。

**布局选项：**
- 双栏（文字在左，插图在右）
- 图标 + 文字行（图标在彩色圆形中，标题加粗，下方配描述）
- 2x2 或 2x3 网格（图片在一侧，内容块网格在另一侧）
- 半出血图片（占满左或右半边）配内容叠加

**数据展示：**
- 大数字亮点（大号数字 60-72pt，下方配小标签）
- 对比栏（前后对比、优缺点、选项并列）
- 时间线或流程（编号步骤、箭头）

**视觉打磨：**
- 章节标题旁的小彩色圆形图标
- 斜体强调文字用于关键数据或标语

### 字体排版

**选择有趣的字体搭配**——不要默认使用 Arial。选择有个性的标题字体，搭配干净的正文字体。

| 标题字体 | 正文字体 | 适用场景 |
|-------------|-----------|----------|
| 宋体 | 黑体 | 商务、时尚、杂志风 |
| Georgia | Calibri | 正式商务、学术 |
| Arial Black | Arial | 强烈、现代感 |
| Trebuchet MS | Calibri | 科技、现代 |
| Palatino | Garamond | 优雅、传统 |
| Consolas | Calibri | 技术、数据 |
| 演示悠然小楷 | 圆体 | 手绘、亲和 |



| 元素 | 字号 |
|---------|------|
| 幻灯片标题 | 36-44pt 加粗 |
| 章节标题 | 20-24pt 加粗 |
| 正文 | 14-16pt |
| 说明 | 10-12pt 淡色 |

### 间距

- 最小边距 0.5"
- 内容块间距 0.3"-0.5"
- 留出呼吸空间——不要填满每一寸

### 避免（常见错误）

- **不要重复相同的布局**——不同的幻灯片要变换栏位、卡片和强调点
- **正文不要居中对齐**——段落和列表左对齐；仅标题居中
- **不要吝啬字号对比**——标题需要 36pt+ 才能从 14-16pt 的正文中突出
- **不要默认使用蓝色**——选择反映特定主题的配色
- **不要随机混用间距**——选择 0.3" 或 0.5" 的间距并一致使用
- **不要只设计一张幻灯片而让其余的保持朴素**——要么完全投入，要么保持简洁一致
- **不要制作纯文字幻灯片**——添加图片、图标、图表或视觉元素；避免单调的标题 + 要点
- **不要忘记文本框内边距**——当用文本边缘对齐线条或形状时，在文本框上设置 `margin: 0` 或偏移形状以留出内边距
- **不要使用低对比度元素**——图标和文字都需要与背景形成强对比；避免浅色文字配浅色背景或深色文字配深色背景
- **绝对不要在标题下使用强调线**——这是 AI 生成幻灯片的标志；使用留白或背景色代替
- **不要先生成PPT代码再想起来加图片** — 图片是规划出来的，不是事后补救的。如果先写了代码再加水印式图片，布局必然混乱。必须在Task 0阶段就完成所有图片的规划、生成、下载。
- **不要随意放置图片** — 每张图片必须有固定的x/y/w/h，必须在写代码之前就确定位置，而不是写代码时随手一摆。
- **不要让元素超出边界** — 所有元素（包括装饰性元素）必须完全位于幻灯片内（x≥0, y≥0, x+w≤10, y+h≤5.625）。延伸到边界外可能引发渲染问题。
- **不要让主标题换行** - 规划布局时要考虑主标题尽量是在同一行，文本框宽度要足够容纳
---

## QA（质检必做）

**假设存在问题。你的工作是找到它们。**

你的第一次渲染几乎从来不是完全正确的。把 QA 当作 bug hunt，而不是确认步骤。如果你第一次检查没发现任何问题，说明你看得不够仔细。

### 内容 QA

```bash
python -m markitdown output.pptx
```

检查缺失内容、拼写错误、顺序错误。

**使用模板时，检查遗留的占位符文本：**

```bash
python -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum|this.*(page|slide).*layout"
```

如果 grep 返回结果，在宣布成功前修复它们。

### 视觉 QA

**⚠️ spawn sub agents**——即使只有 2-3 张幻灯片。你一直盯着代码，会看到你期望看到的，而不是实际存在的。子代理有新鲜的视角。

首先探测环境中是否存在图像理解(image understanding)模型或相应视觉理解大模型或相应SKILL或服务能力（注意不是视觉生成能力）。如果不存在，则跳过此视觉QA环节。如果存在，则将幻灯片转换为图片（见[转换为图片](##转换为图片)），调用视觉理解模型并使用以下提示词：

```prompt
视觉检查这些幻灯片。假设存在问题——找出它们。

查看：
- 元素重叠（文字穿过形状、线条穿过文字、元素堆叠）
- 文字溢出或在边缘/框边界处被截断
- 装饰线为单行文字设计但标题换行到两行
- 来源引用或页脚与上方内容冲突
- 元素太近（< 0.3" 间距）或卡片/章节几乎相触
- 不均匀的间距（一处大块空白，另一处拥挤）
- 距幻灯片边缘的边距不足（< 0.5"）
- 栏或相似元素不一致对齐
- 低对比度文字（例如，浅灰色文字配奶油色背景）
- 低对比度图标（例如，深色图标配深色背景但没有对比圆形）
- 文本框太窄导致过度换行
- 遗留的占位符内容

对于每张幻灯片，列出问题或关注区域，即使是小问题。

阅读并分析这些图片：
1. /path/to/slide-01.jpg（预期：[简要描述]）
2. /path/to/slide-02.jpg（预期：[简要描述]）

报告发现的所有问题，包括小问题。
```

### 验证循环

1. 生成幻灯片 → 转换为图片 → 检查
2. **列出发现的问题**（如果没有发现问题，再更批判性地看一次）
3. 修复问题
4. **重新验证受影响的幻灯片**——一次修复经常会产生另一个问题
5. 重复直到完整检查没有发现新问题

**在完成至少一个修复-验证循环之前，不要宣布成功。**

---

## 转换为图片

将演示文稿转换为单独的幻灯片图片以便视觉检查：

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

这会创建 `slide-01.jpg`、`slide-02.jpg` 等。

要在修复后重新渲染特定幻灯片：

```bash
pdftoppm -jpeg -r 150 -f N -l N output.pdf slide-fixed
```

---

## 依赖

- `pip install "markitdown[pptx]"` - 文本提取
- `pip install Pillow` - 缩略图网格
- `npm install -g pptxgenjs` - 从零创建
- LibreOffice（`soffice`）- PDF 转换（通过 `scripts/office/soffice.py` 为沙盒环境自动配置）
- Poppler（`pdftoppm`）- PDF 转图片

