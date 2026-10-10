# OnlyFans / Adult Model / NSFW Webcam Girl Index

English | [简体中文](./README.zh-CN.md)

A public information index built with Zensical, focused on the keywords `OnlyFans`, `adult model`, `NSFW webcam girl`, and `amateur made`.

`amateur made` is used only for search and classification. Entries cover creators' public identity information, references to voluntarily published content, and official or public platform pages, including publicly accessible adult industry information sites and media reports. The index excludes non-consensual recordings and pirated copies of paid content.

## Features

- 📚 Creators organized alphabetically by username, A–Z
- 🌍 Coverage across multiple countries and regions
- 🔗 Social media links, content platform links, and profiles
- 🔎 Searchable public information about adult models and NSFW webcam creators
- 📱 Automatic deployment to GitHub Pages

## Project structure

```text
docs/
├── 0_meta/          # Background information and metadata
│   ├── list.yaml    # Creator index (YAML)
│   └── source.md    # Information sources
├── A-Z/            # Creator pages grouped by initial letter
└── index.md        # Home page
```

Navigation is generated automatically from directory and file names. The numeric prefix in `0_meta` places background information before the A–Z sections, while the home page remains first. Within each directory, `index.md` comes first, followed by the other pages in filename order. No explicit `nav` configuration is needed.

## Information sources

- X (Twitter)
- OnlyFans
- Wikipedia
- Namu Wiki

## Run locally

1. Check the Zensical version:

```bash
uvx --from zensical==0.0.62 zensical --version
```

2. Start the local preview:

```bash
uvx --from zensical==0.0.62 zensical serve
```

Open http://localhost:8000.

## Automatic deployment

GitHub Actions builds and deploys the project to GitHub Pages:

- Every push to `main` triggers a build
- Navigation is generated automatically from `index.md` pages and the directory structure
- The generated site is deployed to GitHub Pages

## Contributing

To add a creator:

1. Create a `.md` page in the directory for the corresponding initial letter
2. Add an entry to `docs/0_meta/list.yaml`
3. Submit a pull request

The X/Twitter account is optional. Include the `x` field and an X/Twitter link only when the account has been confirmed to belong to the creator. Otherwise, omit both.

### Validate before pushing

Before every push, run these commands from the project root. Push only after both pass:

```bash
uv run --with pyyaml python scripts/validate.py
uvx --from zensical==0.0.62 zensical build --clean --strict
```

The data validator checks duplicate YAML keys, field types, the `status` range, profile files, alphabet index links, and page structure. Missing regions and placeholder profiles produce warnings in normal mode and do not block a push.

To treat these completeness warnings as errors, run `uv run --with pyyaml python scripts/validate.py --strict`. The repository currently has such warnings, so strict data validation does not yet pass. This is separate from the site build's `--strict` check.

### The `status` field

The `status` field in `docs/0_meta/list.yaml` represents information completeness on a scale of 0–100:

| Value | Meaning |
| --- | --- |
| 90 | Mostly complete: a detailed profile, content types, and links to multiple platforms; verified |
| 85 | Mostly complete, with a few fields still missing |
| 80 | Basic public information is available, such as name, region, or links |
| 70 | Placeholder entry: little public information is available or research found no information; needs further work |
| 50 | Only basic references are available; needs the most work |

Set the value according to the available information and increase it as the entry becomes more complete.

## License

MIT License
