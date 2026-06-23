---
name: x-id-research
description: Research creator information using X (Twitter) ID. Fetches X profile, searches web for additional info, and organizes findings into a structured summary. Use when user provides an X/Twitter username and wants to gather information about that creator.
---

# X ID Research

Research a creator's information starting from their X (Twitter) ID.

## Workflow

### Step 1: Fetch X Bio (优先)

首先获取 X bio 信息，这是最直接的信息来源。

#### X 数据源优先级

1. **X 官方** (首选) - `https://x.com/<x_id>`
2. **Sotwe** (备选) - `https://sotwe.com/<x_id>`

如果 X 返回空白/被屏蔽，立即切换到 Sotwe。

#### 搜索引擎优先级

使用 Playwright 绕过反爬虫检测：

1. **Yahoo Japan** (唯一可用) - `https://search.yahoo.co.jp/search?p=<query>`
2. ~~Google~~ — IP 被封，验证码
3. ~~DuckDuckGo~~ — 验证码
4. ~~Bing~~ — 超时
5. ~~Yandex~~ — 验证码

脚本位置：`scripts/search.py`

#### 需要提取的信息

- **Display name** — 显示名
- **Bio/description** — 个人简介，通常包含平台链接
- **Follower count** — 粉丝数
- **Following** — 关注数
- **Posts** — 帖子数
- **Join date** — 注册时间
- **Links** — bio 中的其他平台链接（Fantia, OnlyFans, MyFans, CandFans, Instagram 等）

Bio 中的链接直接用于后续访问，无需搜索。

### Step 2: Extract Creator Name

从 X 显示名或 bio 中提取名字（日文/中文/韩文等），用于网页搜索。

### Step 3: Web Search

Search for the creator using multiple queries. Cast a wide net - don't limit to specific platforms.

#### Search Engine Priority

1. **Google** (primary) - `https://www.google.com/search?q=<query>`
2. **DuckDuckGo** (fallback) - `https://html.duckduckgo.com/html/?q=<query>`

If Google blocks (returns captcha/empty), immediately switch to DuckDuckGo.

#### Search Queries

Suggested search queries (use as starting points, adapt based on findings):
1. `"<creator_name>"` - Exact match for general info
2. `"<x_id>"` - Search by username
3. `"<creator_name>" fantia onlyfans` - Content platforms
4. `"<creator_name>" インスタ タクトック` - Social media
5. `"<creator_name>" 写真集 グラビア` - Photo works
6. `"<creator_name>" プロフィール` - Profile pages

#### Platforms to Check

- Social media: Instagram, TikTok, YouTube, Pixiv
- Content platforms: Fantia, OnlyFans, MyFans, CandFans, Patreon
- Japanese platforms (if Japanese creator)
- News/blog sites
- Forum discussions (Reddit, 5ch, etc.)

### Step 4: Organize Findings

Compile all gathered information into a structured summary:

```
## Research Summary: <x_id>

### Basic Info
- Name: <name>
- Region: <region>
- X: <x_id> (<follower_count> followers)

### Platforms Found
- [Platform]: <link>

### Additional Info
- <any other findings>
```

## Output Format

Return findings as a structured summary suitable for updating `src/meta/list.yaml` and creating a creator file.

## Example Usage

User: "Get info for x_id bu_ivv"

1. Fetch https://x.com/bu_ivv
2. Extract name: "りお♡" / "bu_ivv"
3. Search Google for `"bu_ivv"`, fallback to DuckDuckGo if blocked
4. Find Fantia, MyFans, CandFans, Instagram links
5. Return structured summary
