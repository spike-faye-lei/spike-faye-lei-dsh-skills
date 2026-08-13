"""AI 技术博客、论坛、期刊源定义 — 共 16 个源"""

SOURCES = {
    # ====== AI 大厂 ======
    "anthropic": {
        "name": "Anthropic", "type": "html", "domain": "anthropic.com",
        "index_url": "https://www.anthropic.com/research",
        "article_link_selector": "a[href^='/research/']",
        "article_link_filter": lambda href: ("/research/" in href and "#" not in href
            and "/team/" not in href and "/categories/" not in href
            and href != "/research/" and not href.endswith("/research")),
        "content_selector": "article, main .post-content, .research-content",
        "date_selector": "time, .date, [datetime]",
    },
    "openai": {
        "name": "OpenAI", "type": "html", "domain": "openai.com",
        "index_url": "https://openai.com/research",
        "article_link_selector": "a[href^='/research/']",
        "article_link_filter": lambda href: "/research/" in href and "#" not in href and href.count("/") >= 3,
        "content_selector": "article, .prose, .research-content, main",
        "date_selector": "time, .date, [datetime]",
    },
    "deepmind": {
        "name": "DeepMind", "type": "html", "domain": "deepmind.google",
        "index_url": "https://deepmind.google/discover/blog/",
        "article_link_selector": "a[href*='/discover/blog/']",
        "article_link_filter": lambda href: "/discover/blog/" in href and "#" not in href,
        "content_selector": "article, .blog-post, .article-content, main",
        "date_selector": "time, .date, [datetime]",
    },
    "meta": {
        "name": "Meta AI", "type": "html", "domain": "ai.meta.com",
        "index_url": "https://ai.meta.com/blog/",
        "article_link_selector": "a[href*='/blog/']",
        "article_link_filter": lambda href: "/blog/" in href and "#" not in href and href.count("/") >= 3,
        "content_selector": "article, .blog-content, .prose, main",
        "date_selector": "time, .date, [datetime]",
    },
    "google-research": {
        "name": "Google Research", "type": "html", "domain": "blog.research.google",
        "index_url": "https://blog.research.google/",
        "article_link_selector": "a[href*='/202']",
        "article_link_filter": lambda href: "/202" in href and "#" not in href,
        "content_selector": "article, .post-content, .blog-content, main",
        "date_selector": "time, .date, [datetime]",
    },
    "microsoft-research": {
        "name": "Microsoft Research", "type": "html", "domain": "microsoft.com",
        "index_url": "https://www.microsoft.com/en-us/research/blog/",
        "article_link_selector": "a[href*='/blog/']",
        "article_link_filter": lambda href: "/blog/" in href and "#" not in href and href.count("/") >= 4,
        "content_selector": "article, .blog-post, .article-content, main",
        "date_selector": "time, .date, [datetime]",
    },
    "nvidia": {
        "name": "NVIDIA Research", "type": "html", "domain": "research.nvidia.com",
        "index_url": "https://research.nvidia.com/blog/",
        "article_link_selector": "a[href*='/blog/']",
        "article_link_filter": lambda href: "/blog/" in href and "#" not in href,
        "content_selector": "article, .blog-post, .article-content, main",
        "date_selector": "time, .date, [datetime]",
    },
    "mistral": {
        "name": "Mistral AI", "type": "html", "domain": "mistral.ai",
        "index_url": "https://mistral.ai/news/",
        "article_link_selector": "a[href*='/news/']",
        "article_link_filter": lambda href: "/news/" in href and "#" not in href and href.count("/") >= 3,
        "content_selector": "article, .prose, .post-content, main",
        "date_selector": "time, .date, [datetime]",
    },
    "cohere": {
        "name": "Cohere", "type": "html", "domain": "cohere.com",
        "index_url": "https://cohere.com/blog",
        "article_link_selector": "a[href*='/blog/']",
        "article_link_filter": lambda href: "/blog/" in href and "#" not in href,
        "content_selector": "article, .prose, .post-content, main",
        "date_selector": "time, .date, [datetime]",
    },
    "xai": {
        "name": "xAI", "type": "html", "domain": "x.ai",
        "index_url": "https://x.ai/blog/",
        "article_link_selector": "a[href*='/blog/']",
        "article_link_filter": lambda href: "/blog/" in href and "#" not in href,
        "content_selector": "article, .prose, .post-content, main",
        "date_selector": "time, .date, [datetime]",
    },

    # ====== 论文/期刊 ======
    "arxiv-cs-ai": {
        "name": "arXiv cs.AI", "type": "arxiv", "domain": "arxiv.org",
        "api_url": "http://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&start=0&max_results=",
    },
    "arxiv-cs-cl": {
        "name": "arXiv cs.CL", "type": "arxiv", "domain": "arxiv.org",
        "api_url": "http://export.arxiv.org/api/query?search_query=cat:cs.CL&sortBy=submittedDate&start=0&max_results=",
    },
    "arxiv-cs-lg": {
        "name": "arXiv cs.LG", "type": "arxiv", "domain": "arxiv.org",
        "api_url": "http://export.arxiv.org/api/query?search_query=cat:cs.LG&sortBy=submittedDate&start=0&max_results=",
    },
    "huggingface-papers": {
        "name": "HuggingFace Daily", "type": "hfpapers", "domain": "huggingface.co",
        "api_url": "https://huggingface.co/api/daily_papers",
    },

    # ====== 论坛/社区 ======
    "hackernews": {
        "name": "Hacker News", "type": "hn", "domain": "news.ycombinator.com",
        "top_stories_url": "https://hacker-news.firebaseio.com/v0/topstories.json",
        "item_url": "https://hacker-news.firebaseio.com/v0/item/{id}.json",
    },
    "reddit-ml": {
        "name": "r/MachineLearning", "type": "reddit", "domain": "reddit.com",
        "index_url": "https://www.reddit.com/r/MachineLearning/hot.json?limit=",
    },
}

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; TechBlogHub/1.0; learning AI blogs)"
}

SEMANTIC_TAGS = [
    "Agent",
    "推理模型",
    "MoE",
    "RAG",
    "风险对齐",
    "长上下文",
    "多模态",
    "训练基础设施",
    "Benchmark评测",
    "提示工程",
    "代码生成",
    "可解释性",
    "安全红队",
    "数据合成",
    "模型压缩",
    "产品发布",
]

SOURCE_COLORS = {
    "anthropic":        {"bg": "#faf5f0", "text": "#d4a574", "dot": "#d4944b"},
    "openai":           {"bg": "#f0f7f4", "text": "#4a9e7e", "dot": "#2d7d5f"},
    "deepmind":         {"bg": "#f0f4fa", "text": "#5b8cce", "dot": "#3b6db5"},
    "meta":             {"bg": "#f5f0fa", "text": "#7b5ea7", "dot": "#5e3d8a"},
    "google-research":  {"bg": "#fdf2f2", "text": "#dc6b5e", "dot": "#c94a3a"},
    "microsoft-research":{"bg": "#f0f7fa", "text": "#4a8db7", "dot": "#2d6e96"},
    "nvidia":           {"bg": "#f2faf2", "text": "#5ba85a", "dot": "#3d8a3d"},
    "mistral":          {"bg": "#faf5f0", "text": "#c4944a", "dot": "#a67c2e"},
    "cohere":           {"bg": "#f5f0fa", "text": "#9b6fc0", "dot": "#7b47a8"},
    "xai":              {"bg": "#f5f5f5", "text": "#555555", "dot": "#333333"},
    "arxiv-cs-ai":      {"bg": "#fef9f0", "text": "#b8860b", "dot": "#8b6508"},
    "arxiv-cs-cl":      {"bg": "#fef9f0", "text": "#b8860b", "dot": "#8b6508"},
    "arxiv-cs-lg":      {"bg": "#fef9f0", "text": "#b8860b", "dot": "#8b6508"},
    "huggingface-papers":{"bg": "#fff5f0", "text": "#e89a3c", "dot": "#d4781a"},
    "hackernews":       {"bg": "#fff5f0", "text": "#e86a3c", "dot": "#d4501a"},
    "reddit-ml":        {"bg": "#fff0f5", "text": "#e85a7b", "dot": "#d43d5e"},
}

SOURCE_NAMES = {k: v["name"] for k, v in SOURCES.items()}
