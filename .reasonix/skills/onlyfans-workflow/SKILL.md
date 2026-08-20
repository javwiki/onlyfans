---
name: onlyfans-workflow
description: 完整工作流：优先从 X 核验创作者，再更新 list.yaml、生成创作者 MD 文件并构建发布；包含假冒账号筛查。
---

# 完整工作流 Complete Workflow

涵盖 OnlyFans 博主索引项目从调研到发布的完整流程。使用本 skill 时需按 Step 1→4 顺序执行。

## 前置条件

- 用户提供 X/Twitter ID（用户名）或创作者名称
- 项目根目录：当前工作目录
- 可能需要 Playwright（用于浏览器自动化搜索与 OnlyFans 直连验证）

---

## Step 1: 调研 (Research)

**核心原则：**
- 未指定平台时，默认优先检索和核验 X；只有在 X 无结果、不可访问或完成 X 核验后，才扩展到其他平台补充信息
- X 账号不是必须的。如果未提供 X ID，使用创作者名称先检索 X，再进行跨平台搜索
- **明确指定平台时**，直接检索和验证用户指定的平台；不执行本 skill 的假冒账号筛查，也不因低粉或推广/诱导信息排除账号
- **未指定平台时**，候选 X 账号在采纳前必须通过假冒账号筛查；命中任意一项特征即不采纳为官方账号，不得把其粉丝数、简介、平台链接或内容归入创作者条目：
  1. **粉丝数低**：X 页面显示少于 1000 名粉丝（项目当前低粉排除阈值）
  2. **明显推广/诱导信息**：简介或公开内容含明显导流、付费诱导、私联交易或招揽信息，例如 QQ/微信、红包口令、付费解锁、福利群、线下交易、原味、定制或类似措辞
- 以上筛查仅适用于未指定平台的 X 优先流程；任意一项即可排除，不要求同时满足。同名、第三方镜像、搜索摘要或转载内容不能覆盖排除结论。排除后只能记录为“未核实/疑似假冒”线索

```
明确指定平台 ────→ 直接检索指定平台 → 1.4 平台直连验证 → 1.5 汇总调研结果
未指定平台/无 X ID → 先用名称检索 X → 获取 X 资料并做假冒筛查 → 1.3 跨平台补充 → 1.4 验证
                                                                                  │
                                                                                  ▼
                                                                           1.5 汇总调研结果
```

### 1.1 获取 X Bio（仅当有 X ID 时）

X 数据源优先级：
1. **X 官方** (首选) - `https://x.com/<x_id>`
2. **Sotwe** (备选) - `https://sotwe.com/<x_id>`

如果 X 返回空白/被屏蔽，立即切换到 Sotwe。

提取以下信息：
- **Display name** — 显示名
- **Bio/description** — 个人简介，通常包含平台链接
- **Follower count** — 粉丝数
- **Following** — 关注数
- **Posts** — 帖子数
- **Join date** — 注册时间
- **Links** — bio 中的其他平台链接（Fantia, OnlyFans, MyFans, CandFans, Instagram 等）

### 1.1.1 假冒账号筛查（仅未指定平台时执行）

仅当用户没有明确指定平台、工作流进入 X 优先检索时，对 X 官方页面或可靠的 X 资料页读取到的候选账号执行筛查。粉丝数低或出现明显推广/诱导信息，任意一项命中即排除，不得作为官方账号采纳。排除账号仍可作为待核实线索记录，但必须明确标注“疑似假冒/未采纳”，不能把其个人资料、粉丝数或外链写入创作者正式条目。

如果用户明确指定了平台（包括 X），跳过本节，直接按指定平台的公开页面进行检索、验证和记录。

Bio 中的链接直接用于后续访问，无需搜索。

> **如果 X 账号已注销/不存在/被屏蔽**：如实记录状态，然后继续进入网页搜索，通过名称搜索寻找其他平台信息。

### 1.2 提取创作者名称

从 X 显示名或 bio 中提取名字（日文/中文/韩文等），用于网页搜索。如果 x_id 为空，使用用户提供的名称或其他已知名称作为搜索关键词。

### 1.3 网页搜索 (Web Search)（核心步骤）

这是**最重要**的步骤。**不要只搜索 X 平台**，必须跨平台多角度搜索。可用 `web_fetch` 工具直接发起 HTTP 搜索请求，无需 Playwright 浏览器自动化。

**搜索引擎优先级：**

未指定平台时，先围绕 X 检索：直接访问 `https://x.com/<x_id>`，并使用 `site:x.com` 搜索账号名、显示名和别名；完成 X 账号筛查后，再用以下搜索引擎扩展到其他平台。跨平台结果只能用于补充或交叉核验，不能绕过 X 候选账号的排除结论。明确指定平台时，以用户指定的平台为首要来源，不切换为 X 优先，也不执行假冒账号筛查。

| 优先级 | 引擎 | 搜索 URL | 适用场景 |
|--------|------|----------|----------|
| 1 | **Google** | `https://www.google.com/search?q=<query>` | 通用搜索（首选） |
| 2 | **DuckDuckGo** | `https://html.duckduckgo.com/html/?q=<query>` | Google 被屏蔽时切换 |
| 3 | **Yahoo Japan** | `https://search.yahoo.co.jp/search?p=<query>` | 日系创作者搜索 |
| 4 | **Bing** | `https://www.bing.com/search?q=<query>` | 备选搜索引擎 |

搜索顺序：Google → 被屏蔽则 DuckDuckGo → 日系创作者补充 Yahoo Japan → 仍不够则 Bing。

Playwright 脚本参考：`scripts/search.py`（Yahoo Japan 示例）、`scripts/google_search.py`（Google 示例）

**搜索维度（必须多维度搜索）：**

| 维度 | 关键词示例 | 目的 |
|------|-----------|------|
| 名称精确匹配 | `"<creator_name>"` | 通用信息 |
| 用户名搜索 | `"<x_id>"`（如有） | 按用户名找踪迹 |
| 内容平台 | `"<creator_name>" onlyfans fantia myfans candfans patreon` | 找内容主页 |
| 社交媒体 | `"<creator_name>" instagram tiktok twitter youtube` | 找社交账号 |
| 中文资料 | `"<creator_name>" 博主 网红 福利` | 中文社区讨论 |
| 日文资料 | `"<creator_name>" プロフィール グラビア 写真集` | 日系创作者资料 |
| 韩文资料 | `"<creator_name>" 프로필` | 韩系创作者资料 |
| 论坛讨论 | `"<creator_name>" reddit 5ch` | 社区评价和链接 |
| 行业资料 | `"<creator_name>" babepedia babe wiki imdb` | 成人行业档案核实 |
| 反向图片搜索线索 | `"<creator_name>" image` | 通过图片找来源 |

**需要关注的平台类型：**
- 社交媒体: Instagram, TikTok, YouTube, Pixiv, Facebook
- 内容平台: OnlyFans, Fantia, MyFans, CandFans, Patreon, Fanclub, XFans
- 直播平台: StripChat, Chaturbate, Twitch, 17Live
- 电商/赞助: Boosty, Gumroad, Ko-fi, Fansly
- 中文平台: 微博, 哔哩哔哩, 抖音, 快手, 小红书
- 区域平台: Japanese sites (日系), Thai sites (泰系), Korean sites (韩系)
- 论坛讨论: Reddit, 5ch, Redian
- 成人行业资料站: Babepedia, BabeWiki, IMDb（核实身份/别名/身体数据；注意同名不同人）

**信息收集清单**（搜索结果需重点关注）：
- ✅ 其他社交平台账号（Instagram, TikTok, YouTube, 微博等）
- ✅ 内容平台主页（OnlyFans, Fantia, MyFans, CandFans 等）
- ✅ 个人简介/介绍资料
- ✅ 粉丝数量级
- ✅ 地区/国籍信息
- ✅ 内容类型和风格
- ✅ 真实姓名或艺名
- ✅ 相关社区讨论和评价
- ✅ OnlyFans 订阅价与活跃状态（Inactive / 最后活跃时间）
- ✅ 成人行业站档案（Babepedia 等）核实别名、出生日期、身体数据

### 1.4 平台直连验证（信息确认关键）

搜索引擎找到平台账号后，**直接访问平台主页验证**，不要只依赖搜索摘要。搜索摘要不可靠且常混入**同名不同人**（运动员、演员、素人等），必须以平台页面本身为准。

#### OnlyFans 直连（重点）

OnlyFans 官网有 Cloudflare 防护，`web_fetch` 常被拦截，**改用 Playwright/浏览器自动化访问**：

- URL: `https://onlyfans.com/<username>`
- 需要提取的信息：
  - 显示名（可能是占位名，如 `u31168010`，不代表真人名）
  - 订阅价格（`$X 每月`）
  - 帖子数（无帖子说明账号空壳/不活跃）
  - 总点赞数
  - 最后活跃时间（页面显示 `Seen <日期>`）
  - 账号状态（`Inactive` = 不活跃）
- 判断：只要页面存在即为有效账号；Inactive 也要如实记录，不因不活跃而删除条目

> 明确指定 OnlyFans 时，页面存在即可按页面状态记录，不执行本 skill 的假冒账号筛查。只有在未指定平台、由 X 优先流程发现并关联到 OnlyFans 时，才适用低粉或推广/诱导信息的排除规则。

#### 成人行业资料站（核实身份）

当创作者为成人模特/camgirl 时，搜索并访问行业资料站确认身份、别名与身体数据：

| 站 | URL | 关键信息 |
|----|-----|----------|
| Babepedia | `https://www.babepedia.com/babe/<name>` | 别名、出生日期、国籍/种族、身高、三围、职业、评分、作品数 |
| BabeWiki | `https://babe.wiki/<name>` | 同上 |
| IMDb | `https://www.imdb.com/find/?q=<name>` | 影视作品履历 |

- 用别名（如 Nyla Lueeth / Nyla San）交叉搜索，确认同一人
- 行业站上的 X/OnlyFans 链接位置常在广告区，**需二次验证归属**后再录入

### 1.5 调研输出

收集所有信息，准备用于更新 list.yaml 和创建 MD 文件。输出结构：

```yaml
# 调研结果示例
x_id: "bu_ivv"
name: "りお♡"
aliases: ["ri〇"]
region: "日本"  # 日本/美国/台湾/泰国/中国/苏丹等
platforms:
  x: "bu_ivv"
  x_alt: ""         # 备用 X 账号
  onlyfans: ""      # OnlyFans 用户名
  fantia: ""        # Fantia 粉丝俱乐部 ID/名称
  myfans: ""        # MyFans 用户名
  candfans: ""      # CandFans 用户名
  instagram: ""     # Instagram 用户名
  tiktok: ""        # TikTok 用户名
  youtube: ""       # YouTube channel ID
  bilibili: ""      # Bilibili UID
  discord: ""       # Discord 邀请码
  website: ""       # 个人网站
  telegram: ""      # Telegram 用户名
  stripchat: ""     # StripChat 用户名
  xfans: ""         # XFans 用户名
  fanclub: ""       # 粉丝俱乐部网址
  weibo: ""         # 微博用户名
  douyin: ""        # 抖音用户名
  xiaohongshu: ""   # 小红书用户名
description: "简介内容（汇总所有发现）"
follower_count: "409.7K"
tags: []           # 标签，如 cosplay, shemale, beautyleg 等
screening:
  applied: true        # 仅未指定平台时为 true；明确指定平台时为 false
  accepted: true
  rejected_reasons: []  # 命中低粉或推广诱导时填写原因，并将 accepted 设为 false
```

---

## Step 2: 更新 list.yaml (Metadata)

编辑 `src/_meta/list.yaml` 添加或更新创作者条目。

### list.yaml 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | ✅ | 创作者名称/艺名 |
| `region` | ✅ | 地区：日本/美国/台湾/泰国/中国/苏丹等 |
| `x` | ❌ | X/Twitter ID（可选，无则留空） |
| `file` | ✅ | MD 文件路径，格式 `src/<首字母>/<key>.md` |
| `status` | ✅ | 状态码：90=完整, 80=常规, 70=不完整, 50=待确认 |
| `aliases` | ❌ | 别名列表 |
| `x_alt` | ❌ | 备用 X 账号 |
| `onlyfans` | ❌ | OnlyFans 用户名 |
| `fantia` | ❌ | Fantia 粉丝俱乐部名或 ID |
| `myfans` | ❌ | MyFans 用户名 |
| `candfans` | ❌ | CandFans 用户名 |
| `instagram` | ❌ | Instagram 用户名 |
| `tiktok` | ❌ | TikTok 用户名 |
| `youtube` | ❌ | YouTube Channel ID |
| `bilibili` | ❌ | Bilibili UID |
| `discord` | ❌ | Discord 邀请码 |
| `website` | ❌ | 个人网站 |
| `telegram` | ❌ | Telegram 用户名 |
| `stripchat` | ❌ | StripChat 用户名 |
| `xfans` | ❌ | XFans 用户名 |
| `fanclub` | ❌ | 粉丝俱乐部网址 |
| `x_file` | ❌ | X 资料文件路径 |
| `tags` | ❌ | 标签列表 |
| `status` | ✅ | 状态码 |

### 添加条目

在 `src/_meta/list.yaml` 末尾添加新条目，格式：

```yaml
<key>:                   # key 使用 x_id（如有）或名称拼音（小写）
  name: <创作者名称>
  aliases:
  - <别名1>
  region: <地区>
  x: <x_id>              # X 账号（可选，无则留空或省略该行）
  onlyfans: <onlyfans_id>
  instagram: <instagram_id>
  file: src/<首字母>/<key>.md
  status: 80
```

**规则：**
- key 优先使用 x_id（小写）；无 x_id 时使用名称拼音/英文标识（小写）
- 字符串值无需引号，除非包含特殊字符
- `aliases` 可以是列表或单行 `[别名1, 别名2]`
- 按照字母顺序插入，保持 YAML 格式整洁（2 空格缩进）
- `status` 默认 80，完整信息可用 90
- 如果没有 X 账号，`x` 字段可以省略或留空字符串 `x: ""`

---

## Step 3: 生成创作者 MD 文件 (Content)

在 `src/<首字母>/<key>.md` 创建创作者 Markdown 文件。

### MD 文件模板

记得在文件顶部添加 frontmatter `tags:`，以便 `mdbook-tagging` 自动生成标签索引页：

```markdown
---
tags: [cosplay, beautyleg]    # 根据实际情况填写，无标签则留空 []
---

# <name>

| 项目 | 内容 |
|------|------|
| **用户名** | `<key>` |
| **别名** | <别名1>、<别名2> |
| **地区** | 🇯🇵 日本（或其他地区 emoji） |
| **内容类型** | <内容类型描述> |
| **风格** | <风格描述> |

## 📝 简介

<综合简介段落：介绍创作者背景、特点、活跃平台等>

## 🔗 相关链接

- [X / Twitter](https://x.com/<x_id>) — <粉丝数> 粉丝  （如有 X 账号）
- [OnlyFans](https://onlyfans.com/<username>)（如有）
- [Fantia](https://fantia.jp/fanclubs/<id>)（如有）
- [MyFans](https://myfans.jp/<username>)（如有）
- [CandFans](https://candfans.jp/<username>)（如有）
- [Instagram](https://instagram.com/<username>)（如有）

---

[◀ 返回 <首字母> 列表](./index.md) · [🏠 首页](../index.md)
```

### 地区 Emoji 对照表

| 地区 | Emoji |
|------|-------|
| 日本 | 🇯🇵 |
| 美国 | 🇺🇸 |
| 台湾 | 🇨🇳（或 🇹🇼） |
| 泰国 | 🇹🇭 |
| 中国 | 🇨🇳 |
| 苏丹 | 🇸🇩 |

### 注意事项

- 文件名统一用小写
- 如果已有文件则更新内容（保留原有格式）
- 文件头部使用 `# <name>` 格式
- 链接部分只列出实际存在的平台
- 末尾保留返回导航链接

---

## Step 4: 更新 SUMMARY.md 并构建 (Build)

### 4.1 生成标签索引页

为所有带有 frontmatter `tags:` 的 markdown 文件生成标签索引页面：

```bash
mdbook-tagging generate .
```

如果某个创作者有 `tags: [cosplay, beautyleg]`，`mdbook-tagging` 会自动生成对应的标签归档页面。

### 4.2 生成 SUMMARY.md

使用 `mdbook-summarizer` 自动生成目录文件：

```bash
mdbook-summarizer --src src --auto-readme
```

### 4.3 本地构建验证

```bash
# 构建 mdBook
mdbook build

# 本地预览（可选）
mdbook serve
```

### 4.4 Git 提交

```bash
git add src/_meta/list.yaml src/<首字母>/<key>.md src/SUMMARY.md
git commit -m "feat: add creator <name> (<key>)"
```

---

## 完整工作流速查表

```
用户提供 X ID 或名称
  │
  ▼
Step 1: 调研 (Research)
  ├─ 1.1 获取 X Bio → x.com / sotwe.com
  ├─ 1.2 提取创作者名称
  ├─ 1.3 网页搜索 → Google / DuckDuckGo / Yahoo Japan / Bing
  ├─ 1.4 平台直连验证 → OnlyFans 直连 / Babepedia 等
  └─ 1.5 汇总调研结果
  │
  ▼
Step 2: 更新 list.yaml
  └─ 追加 src/_meta/list.yaml 条目
  │
  ▼
Step 3: 生成 MD 文件
  └─ 创建 src/<首字母>/<key>.md
  │
  ▼
Step 4: 构建并提交
  ├─ mdbook-tagging generate (标签索引)
  ├─ mdbook-summarizer (SUMMARY.md)
  ├─ mdbook build
  └─ git commit
```

## 相关技能

- 无（调研环节已并入本 skill 的 Step 1）
