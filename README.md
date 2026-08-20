# OnlyFans / Adult Model / NSFW Webcam Girl 索引

这是一个使用 mdBook 构建的公开资料索引项目，定位关键词为 `OnlyFans`、`adult model`、`NSFW webcam girl` 与 `amateur leak`。

其中 `amateur leak` 仅作为检索与分类关键词；项目不收录、转载、链接或分发泄露及非自愿私密内容，只记录合法公开的创作者资料与官方/公开平台页面。

## 项目特点

- 📚 按用户名首字母 A-Z 分类
- 🌍 覆盖多个国家和地区
- 🔗 包含社交媒体、内容平台链接和简介
- 🔎 支持成人模特、NSFW webcam girl 等公开身份线索检索
- 📱 支持 GitHub Pages 自动部署

## 项目结构

```
src/
├── _meta/           # 元数据
│   ├── list.yaml    # 创作者索引（YAML格式）
│   └── source.md    # 数据来源
├── A-Z/             # 按字母分类的博主页面
├── index.md         # 首页
└── SUMMARY.md       # 自动生成的目录
```

## 数据来源

- X (Twitter)
- OnlyFans
- Wikipedia
- Namu Wiki

## 本地运行

1. 安装 mdBook 与目录生成器：
```bash
cargo install mdbook mdbook-summarizer
```

2. 生成目录文件（`SUMMARY.md` 由 CI 自动生成并被 gitignore，本地需手动生成）：
```bash
mdbook-summarizer --src src --auto-readme
```

3. 本地预览：
```bash
mdbook serve
```

4. 访问 http://localhost:3000

## 自动部署

项目使用 GitHub Actions 自动部署到 GitHub Pages：

- 每次推送到 `main` 分支时自动构建
- 自动生成 `SUMMARY.md` 目录文件
- 部署到 GitHub Pages

## 贡献指南

欢迎提交新的博主信息！请按照以下格式：

1. 在对应字母目录下创建 `.md` 文件
2. 在 `src/_meta/list.yaml` 中添加索引条目
3. 提交 Pull Request

### `status` 字段说明

`src/_meta/list.yaml` 中每条目的 `status` 字段表示信息完整度（0–100）：

| 值 | 含义 |
|----|------|
| 90 | 信息较完整：包含详细简介、内容类型、多平台链接，已核实 |
| 85 | 信息较完整，少量字段待补 |
| 80 | 有基本公开信息（姓名/地区/链接） |
| 70 | 占位条目：公开信息很少或未搜索到，待补充 |
| 50 | 仅基础线索，最需补充 |

提交新条目时请如实标注，信息补全后可逐步上调。

## 许可证

MIT License
