# 待办

核对日期：2026-11-10。完成一项后删除对应条目。`region` 缺项已统一补为「未知」，待后续逐条核实。

当前校验：`errors=0`，`warnings=1`（W2 占位页 28 个）。

## 一、资料待补充条目（28 条）

正文偏短，或仍缺少可核验的身份、地区与平台链接。补全后删除；确认无公开资料的条目保留「已核查」说明。

### F

- [ ] [Forest Nymph](docs/F/ForestNymph.md) — 占位，地区未知，无外链，status 70，正文约 151 字

### G

- [ ] [高抬腿女教官](docs/G/Gaotaituinvjiaoguan.md) — 占位，地区未知，无外链，status 70，正文约 89 字
- [ ] [Gguesting](docs/G/Gguesting.md) — 占位，地区未知，无外链，status 70，正文约 92 字
- [ ] [GOFLOWER](docs/G/GOFLOWER.md) — 占位，地区未知，无外链，status 70，正文约 148 字
- [ ] [月亮爱神GOL](docs/G/GOL.md) — 占位，地区未知，无外链，status 70，正文约 90 字

### H

- [ ] [Haoleman](docs/H/Haoleman.md) — 占位，地区未知，无外链，status 70，正文约 225 字
- [ ] [きのっぴ](docs/H/Hellokitty0311.md) — 占位，地区未知，外链，status 70，正文约 173 字
- [ ] [honglis2](docs/H/honglis2.md) — 占位，地区未知，无外链，status 70，正文约 149 字
- [ ] [Hongyi0122](docs/H/Hongyi0122.md) — 占位，地区未知，无外链，status 70，正文约 93 字

### K

- [ ] [Kakiooi](docs/K/Kakiooi.md) — 占位，地区未知，无外链，status 70，正文约 90 字
- [ ] [金慧恩](docs/K/KimHyeEun.md) — 占位，地区未知，无外链，status 70，正文约 141 字

### L

- [ ] [林佳](docs/L/lj10010.md) — 占位，地区未知，无外链，status 70，正文约 134 字

### M

- [ ] [MissA](docs/M/MissA.md) — 占位，地区未知，无外链，status 70，正文约 143 字

### N

- [ ] [乃香](docs/N/Naixiang.md) — 占位，地区未知，无外链，status 70，正文约 134 字
- [ ] [南北北](docs/N/Nanbeibei.md) — 占位，地区中国，无外链，status 70，正文约 135 字

### P

- [ ] [帕里斯](docs/P/Palisi.md) — 占位，地区未知，无外链，status 80，正文约 150 字
- [ ] [punipxn](docs/P/punipxn.md) — 占位，地区未知，无外链，status 70，正文约 147 字

### Q

- [ ] [倩倩](docs/Q/Qianqian180.md) — 占位，地区中国，无外链，status 70，正文约 85 字
- [ ] [清心](docs/Q/Qingxin.md) — 占位，地区未知，无外链，status 80，正文约 175 字

### R

- [ ] [ririca](docs/R/ririca.md) — 占位，地区未知，外链，status 70，正文约 165 字

### T

- [ ] [土豆姐](docs/T/Tudoujie.md) — 占位，地区中国，外链，status 80，正文约 168 字

### W

- [ ] [王绾绾](docs/W/Wangwanwan.md) — 占位，地区未知，无外链，status 70，正文约 134 字
- [ ] [吴丽娜](docs/W/Wulina.md) — 占位，地区未知，无外链，status 80，正文约 144 字

### X

- [ ] [小妹](docs/X/Xiaomei.md) — 占位，地区中国，无外链，status 70，正文约 85 字

### Y

- [ ] [연우](docs/Y/YeonWoo.md) — 占位，地区未知，无外链，status 80，正文约 141 字
- [ ] [玥儿](docs/Y/Yueer.md) — 占位，地区未知，无外链，status 70，正文约 139 字
- [ ] [月儿](docs/Y/Yuer.md) — 占位，地区未知，无外链，status 70，正文约 85 字
- [ ] [月牙](docs/Y/Yueya.md) — 占位，地区中国，无外链，status 80，正文约 85 字

## 二、待替换的失效外链（6 条）

已从页面移除超链接并标注「原链接已失效」。找到新地址后恢复链接，否则保持现状。

- [ ] docs/B/Baimint3663.md — Line `@mint.22061188`：https://line.me/ti/p/@mint.22061188
- [ ] docs/C/cookiemon18.md — Pornhub：https://rt.pornhub.org/shorties/642e92c741e7e
- [ ] docs/I/itseunchae.md — EroMe：https://www.erome.com/a/E15CbpeQ
- [ ] docs/I/itseunchae.md — EroMe：https://www.erome.com/a/r2wHTaFo
- [ ] docs/M/miuzxc.md — xHamster：https://xhamster.com/model/miuzxc_official
- [ ] docs/D/Desireeblackkk.md — Snapchat：https://www.snapchat.com/add/thedesireeblack

## 三、其他一致性工作

- [ ] 将 `region` 仍为 `未知` 的 274 条逐条核实为实际地区。
- [ ] tags 覆盖：698 页中 402 页有 tags，决定其余页面是否补标（含国家、平台、内容类型）。
- [ ] 复核从 X 关注名单导入的 OnlyFans 条目：本轮已批量访问 526 个 `x` 用户名，21 个返回 404 并已移除，其余仍需逐条核对账号归属与地区。
- [ ] 无外链页面 95 个，其中 28 个已在第一节；其余按需补充可核验链接。
- [ ] 目标：`python3 scripts/validate.py --strict` 零警告（依赖第一节完成）。
