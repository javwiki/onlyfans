# OnlyFans 博主介绍

这是一个使用 mdBook 构建的 OnlyFans 博主索引项目，收录了来自全球的优秀创作者。

## 项目特点

- 📚 按用户名首字母 A-Z 分类
- 🌍 覆盖多个国家和地区
- 🔗 包含社交媒体链接和简介
- 📱 支持 GitHub Pages 自动部署

## 项目结构

```
src/
├── _meta/           # 元数据
│   ├── list.yaml    # 创作者索引（YAML格式）
│   └── source.md    # 数据来源
├── A-Z/             # 按字母分类的博主页面
├── README.md        # 首页
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
mdbook-summarizer --src src
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

## 许可证

MIT License
