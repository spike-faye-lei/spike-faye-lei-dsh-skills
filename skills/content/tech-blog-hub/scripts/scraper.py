"""抓取 AI 技术博客、论坛、期刊文章 — 支持 5 种源类型"""

import sys
import json
import time
import re
from defusedxml import ElementTree as ET
from datetime import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from sources import SOURCES, DEFAULT_HEADERS


# ============================================================
# 通用工具
# ============================================================

def fetch_json(url, headers=None, timeout=30):
    resp = requests.get(url, headers=headers or DEFAULT_HEADERS, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def fetch_page(url, headers=None, timeout=30):
    resp = requests.get(url, headers=headers or DEFAULT_HEADERS, timeout=timeout)
    resp.raise_for_status()
    return resp.text, resp.url


def parse_date(date_str):
    """尝试解析各种日期格式，返回 YYYY-MM-DD"""
    if not date_str:
        return ""
    # 已经是标准格式
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        return date_str
    # ISO 格式
    if "T" in date_str:
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00")).strftime("%Y-%m-%d")
        except Exception:
            pass
    # 尝试常见格式
    for fmt in ["%B %d, %Y", "%b %d, %Y", "%d %B %Y", "%Y-%m-%dT%H:%M:%SZ", "%Y%m%d"]:
        try:
            return datetime.strptime(date_str.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return date_str


# ============================================================
# HTML 源处理
# ============================================================

def extract_article_list_html(html, base_url, source_config):
    soup = BeautifulSoup(html, "html.parser")
    selector = source_config["article_link_selector"]
    link_filter = source_config.get("article_link_filter")
    links = soup.select(selector)
    seen = set()
    articles = []

    for link in links:
        href = link.get("href", "")
        if not href:
            continue
        full_url = urljoin(base_url, href)
        if full_url in seen:
            continue
        seen.add(full_url)
        if link_filter and not link_filter(href):
            continue

        # 标题
        title = ""
        title_el = link.select_one("h1, h2, h3, h4, [class*='title'], [class*='heading']")
        if title_el:
            title = title_el.get_text(strip=True)
        if not title:
            direct_texts = [c.strip() for c in link.children if isinstance(c, str)]
            title = " ".join(direct_texts).strip()
        if not title or len(title) < 5:
            title = link.get_text(" ", strip=True)
        if len(title) > 150:
            title = title.split("  ")[0].split("\n")[0].strip()
            if len(title) > 150:
                title = title[:150].rsplit(" ", 1)[0]
        if not title or len(title) < 5:
            title = link.get("aria-label", "") or link.get("title", "")
            if not title:
                continue

        # 日期和摘要
        card = link.parent or link
        date_text = ""
        excerpt = ""
        if card:
            date_el = card.select_one(source_config.get("date_selector", "time"))
            if date_el:
                date_text = date_el.get("datetime", "") or date_el.get_text(strip=True)
            for p in card.select("p, .excerpt, .description"):
                text = p.get_text(strip=True)
                if text and len(text) > 20 and text != title:
                    excerpt = text[:200]
                    break

        articles.append({
            "title": title, "url": full_url,
            "date": parse_date(date_text), "excerpt": excerpt,
        })

    return articles


def extract_article_content_html(html, url, source_config):
    soup = BeautifulSoup(html, "html.parser")
    content_el = soup.select_one(source_config.get("content_selector", "article"))
    if not content_el:
        content_el = soup.find("body")
    if not content_el:
        return {"title": "", "content_md": "", "date": ""}

    for tag in content_el.select("script, style, nav, footer, .nav, .footer, .sidebar, .comments, .related, .share, .social, noscript, iframe"):
        tag.decompose()

    title = ""
    title_el = soup.select_one("h1, .post-title, .article-title, [property='og:title']")
    if title_el:
        title = title_el.get("content", "") or title_el.get_text(strip=True)

    date = ""
    date_el = soup.select_one(source_config.get("date_selector", "time"))
    if date_el:
        date = date_el.get("datetime", "") or date_el.get_text(strip=True)

    content_md = html_to_markdown(content_el)
    return {"title": title, "content_md": content_md, "date": parse_date(date)}


def html_to_markdown(element):
    lines = []
    for child in element.children:
        if isinstance(child, str):
            text = child.strip()
            if text:
                lines.append(text)
            continue
        tag = child.name.lower() if child.name else ""
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = int(tag[1])
            text = child.get_text(strip=True)
            if text:
                lines.append(f"\n{'#' * level} {text}\n")
        elif tag == "p":
            text = child.get_text(strip=True)
            if text:
                lines.append(f"\n{text}\n")
        elif tag in ("ul", "ol"):
            for li in child.find_all("li", recursive=False):
                text = li.get_text(strip=True)
                if text:
                    prefix = "- " if tag == "ul" else "1. "
                    lines.append(f"{prefix}{text}")
            lines.append("")
        elif tag in ("pre", "code"):
            text = child.get_text()
            if tag == "pre":
                code_el = child.find("code")
                lang = ""
                if code_el and code_el.get("class"):
                    for cls in code_el["class"]:
                        if cls.startswith("language-"):
                            lang = cls[9:]
                lines.append(f"\n```{lang}\n{text}\n```\n")
            else:
                lines.append(f"`{text}`")
        elif tag == "blockquote":
            text = child.get_text(strip=True)
            for line in text.split("\n"):
                lines.append(f"> {line}")
            lines.append("")
        elif tag == "img":
            alt = child.get("alt", "")
            src = child.get("src", "")
            if src:
                lines.append(f"![{alt}]({src})\n")
        elif tag in ("table",):
            lines.append(child.get_text(strip=True))
        else:
            lines.append(html_to_markdown(child))
    return "\n".join(line for line in lines if line)


# ============================================================
# arXiv API 处理
# ============================================================

def extract_article_list_arxiv(source_config, count):
    url = source_config["api_url"] + str(count)
    resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=30)
    resp.raise_for_status()

    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom",
    }
    root = ET.fromstring(resp.text)
    articles = []

    for entry in root.findall("atom:entry", ns):
        title = entry.find("atom:title", ns)
        summary = entry.find("atom:summary", ns)
        link_el = entry.find("atom:link", ns)
        published = entry.find("atom:published", ns)
        authors = entry.findall("atom:author/atom:name", ns)

        article_url = link_el.get("href", "") if link_el is not None else ""
        article_title = title.text.strip().replace("\n", " ") if title is not None and title.text else ""
        article_summary = summary.text.strip()[:200] if summary is not None and summary.text else ""
        article_date = published.text[:10] if published is not None and published.text else ""
        author_names = [a.text for a in authors if a.text]

        articles.append({
            "title": article_title,
            "url": article_url,
            "date": article_date,
            "excerpt": f"{', '.join(author_names[:3])} — {article_summary}" if author_names else article_summary,
        })

    return articles


def extract_article_content_arxiv(url, source_config):
    # arXiv 文章页面是 HTML，用简单方式提取摘要
    abs_url = url.replace("/abs/", "/abs/")
    html, _ = fetch_page(abs_url)
    soup = BeautifulSoup(html, "html.parser")
    abstract = soup.select_one("blockquote.abstract")
    title_el = soup.select_one("h1.title")
    title = title_el.get_text(strip=True).replace("Title:", "") if title_el else ""
    content = abstract.get_text(strip=True) if abstract else ""
    return {"title": title, "content_md": content, "date": ""}


# ============================================================
# HuggingFace Daily Papers
# ============================================================

def extract_article_list_hfpapers(source_config, count):
    data = fetch_json(source_config["api_url"])
    articles = []
    for paper in data[:count]:
        p = paper.get("paper", paper)
        articles.append({
            "title": p.get("title", ""),
            "url": f"https://huggingface.co/papers/{p.get('id', '')}",
            "date": p.get("publishedAt", "")[:10] if p.get("publishedAt") else "",
            "excerpt": (p.get("summary", "") or "")[:200],
        })
    return articles


# ============================================================
# Hacker News API
# ============================================================

AI_KEYWORDS = [
    "ai", "llm", "gpt", "claude", "transformer", "deep learning",
    "machine learning", "neural", "rag", "agent", "alignment",
    "openai", "anthropic", "deepmind", "mistral", "llama",
    "diffusion", "rlhf", "chain of thought", "reasoning",
    "multimodal", "embedding", "fine-tun", "inference",
]


def is_ai_related(title):
    title_lower = title.lower()
    return any(kw in title_lower for kw in AI_KEYWORDS)


def extract_article_list_hn(source_config, count):
    top_ids = fetch_json(source_config["top_stories_url"])[:100]  # 取 top 100
    articles = []
    for item_id in top_ids:
        if len(articles) >= count * 3:  # 多取一些用于过滤
            break
        time.sleep(0.1)
        try:
            item = fetch_json(source_config["item_url"].format(id=item_id))
        except Exception:
            continue
        title = item.get("title", "")
        if not title or not is_ai_related(title):
            continue
        url = item.get("url", "") or f"https://news.ycombinator.com/item?id={item_id}"
        articles.append({
            "title": title,
            "url": url,
            "date": datetime.fromtimestamp(item.get("time", 0)).strftime("%Y-%m-%d"),
            "excerpt": f"HN {item.get('score', 0)} points, {item.get('descendants', 0)} comments",
        })
        if len(articles) >= count:
            break
    return articles


# ============================================================
# Reddit API
# ============================================================

def extract_article_list_reddit(source_config, count):
    url = source_config["index_url"] + str(count)
    data = fetch_json(url, headers={**DEFAULT_HEADERS, "User-Agent": "TechBlogHub/1.0"})
    articles = []
    for post in data.get("data", {}).get("children", []):
        p = post["data"]
        if p.get("stickied"):
            continue
        articles.append({
            "title": p.get("title", ""),
            "url": f"https://www.reddit.com{p.get('permalink', '')}",
            "date": datetime.fromtimestamp(p.get("created_utc", 0)).strftime("%Y-%m-%d"),
            "excerpt": (p.get("selftext", "") or "")[:200],
        })
        if len(articles) >= count:
            break
    return articles


# ============================================================
# 主入口
# ============================================================

def cmd_list(source_name, count):
    if source_name not in SOURCES:
        print(json.dumps({"error": f"未知数据源: {source_name}", "available": list(SOURCES.keys())}, ensure_ascii=False, indent=2))
        sys.exit(1)

    config = SOURCES[source_name]
    src_type = config.get("type", "html")

    if src_type == "html":
        html, final_url = fetch_page(config["index_url"])
        articles = extract_article_list_html(html, final_url, config)
    elif src_type == "arxiv":
        articles = extract_article_list_arxiv(config, count)
    elif src_type == "hfpapers":
        articles = extract_article_list_hfpapers(config, count)
    elif src_type == "hn":
        articles = extract_article_list_hn(config, count)
    elif src_type == "reddit":
        articles = extract_article_list_reddit(config, count)
    else:
        print(json.dumps({"error": f"不支持的源类型: {src_type}"}, ensure_ascii=False))
        sys.exit(1)

    result = {"source": source_name, "count": len(articles[:count]), "articles": articles[:count]}
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_fetch(url, source_name):
    if source_name not in SOURCES:
        print(json.dumps({"error": f"未知数据源: {source_name}"}, ensure_ascii=False))
        sys.exit(1)

    config = SOURCES[source_name]
    src_type = config.get("type", "html")

    if src_type == "html":
        html, final_url = fetch_page(url)
        result = extract_article_content_html(html, final_url, config)
    elif src_type == "arxiv":
        result = extract_article_content_arxiv(url, config)
    else:
        # API 源不 fetch 正文，正文由 Claude 在 skill 中抓取
        result = {"title": "", "content_md": "", "date": "", "note": "API source, content should be fetched separately"}

    print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    if len(sys.argv) < 2:
        print("用法: python scraper.py list <source> [--count N]")
        print("       python scraper.py fetch <url> --source <source>")
        print("       python scraper.py sources")
        sys.exit(1)

    command = sys.argv[1]

    if command == "sources":
        sources_list = [{"id": k, "name": v["name"], "type": v.get("type", "html")} for k, v in SOURCES.items()]
        print(json.dumps(sources_list, ensure_ascii=False, indent=2))
        return

    if command == "list":
        if len(sys.argv) < 3:
            print("用法: python scraper.py list <source> [--count N]")
            sys.exit(1)
        source_name = sys.argv[2]
        count = 10
        for i, arg in enumerate(sys.argv):
            if arg == "--count" and i + 1 < len(sys.argv):
                count = int(sys.argv[i + 1])
        cmd_list(source_name, count)

    elif command == "fetch":
        if len(sys.argv) < 4:
            print("用法: python scraper.py fetch <url> --source <source>")
            sys.exit(1)
        url = sys.argv[2]
        source_name = None
        for i, arg in enumerate(sys.argv):
            if arg == "--source" and i + 1 < len(sys.argv):
                source_name = sys.argv[i + 1]
        if not source_name:
            print(json.dumps({"error": "需要 --source 参数"}))
            sys.exit(1)
        cmd_fetch(url, source_name)

    else:
        print(f"未知命令: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
