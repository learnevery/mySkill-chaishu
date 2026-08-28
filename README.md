# chaishu · 网文拆书工具箱

[![CI](https://github.com/learnevery/skills/actions/workflows/ci.yml/badge.svg)](https://github.com/learnevery/skills/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](./pyproject.toml)

**逆向解剖爆款网文，提炼成可复用的创作方法论。** 本项目把"拆书"这套网文作者的行业基本功做成了开源工具箱：两个可直接安装的 AI 技能 + 一个零依赖的 Python 命令行工具，覆盖 **拆 → 提炼 → 入库 → 内化** 完整闭环。

> 拆书是研究"这本书为什么火"的工业化叙事逻辑（开篇钩子、人设体系、节奏情绪曲线、大纲结构、赛道偏好），只借鉴骨架、不复制血肉。

---

## 核心组成

| 组件 | 说明 |
|------|------|
| `skills/chaishu` | AI 拆书技能：五大维度拆解、粗拆/深度细拆双模式、仿写训练，产出 MD + 精排版 HTML 双格式报告 |
| `skills/chaishu-builder` | AI 入库技能：把拆书精华持续沉淀到 人设/剧情/爽点/节奏/金手指 五大知识库 |
| `chaishu` CLI | 命令行工具：报告骨架生成、MD→HTML 渲染、报告校验、规则化知识库入库、技能打包，**不依赖 AI 也能跑通全流程** |

## 快速开始

```bash
# 安装（Python 3.9+，零运行时依赖）
pip install -e .

# 1. 生成报告骨架（deep=深度细拆 / rough=粗拆扫榜）
chaishu new 神通者 --mode deep

# 2. 按骨架填写拆解内容后：校验完整性
chaishu validate 拆书/拆书报告-神通者-深度细拆.md

# 3. 渲染精排版 HTML（自带封面/可折叠目录/逐章标记表格样式）
chaishu build 拆书/拆书报告-神通者-深度细拆.md

# 4. 五大维度精华入库（人设/剧情/爽点/节奏/金手指/范式.md）
chaishu kb add 拆书/拆书报告-神通者-深度细拆.md

# 5. 查看知识库积累
chaishu kb stats
```

### 命令一览

| 命令 | 作用 |
|------|------|
| `chaishu new <书名> [--mode deep\|rough]` | 生成拆书报告骨架到 `拆书/` |
| `chaishu build <报告.md> [-o out.html]` | Markdown 报告 → 精排版 HTML（复用技能同款模板） |
| `chaishu validate <报告.md>` | 校验：必填章节、`作者目的` 列、范式/仿写/内化是否齐备、占位符是否填写 |
| `chaishu kb add <报告.md> [--force]` | 按规则把人设/金手指/节奏/爽点/大纲/范式提取入库，重复自动去重 |
| `chaishu kb stats` | 知识库各文件条目数统计 |
| `chaishu pack` | 把 `skills/` 下技能目录打成 UTF-8 文件名的 zip（跨平台解压不乱码） |

## AI 技能安装

技能面向支持 SKILL.md 格式的智能体平台：

1. 下载 [skills/chaishu.zip](./skills/chaishu.zip) 与 [skills/chaishu-builder.zip](./skills/chaishu-builder.zip)；
2. 在支持 SKILL.md 的智能体平台中执行技能导入（如 `/install-capability`），选择本地 zip 导入；
3. 推荐搭配：先用 `chaishu` 拆书写报告，再用 `chaishu-builder`（或 `chaishu kb add`）把精华沉淀进知识库。

技能源码就是仓库里的 `skills/` 目录，修改后执行 `chaishu pack` 重新打包。

## 方法论速览

**五大拆解维度**（详见[五大维度拆解手册](./skills/chaishu/references/五大维度拆解手册.md)）：

1. **卖点与开篇**：黄金三章、书名简介钩子、章末钩子类型、信息抛出顺序
2. **人设体系**：主角欲望痛点、金手指边界频率、配角反派衬托、冲突来源
3. **节奏与情绪曲线**（最核心）：爽点铺垫与释放、高潮密度、甜虐坑伏笔
4. **大纲与故事结构**：主线分卷、危机递进、赛道高频模块
5. **赛道读者偏好**：读者吃哪种梗、雷点清单、赛道风向

**两种模式**：粗拆（1-2 小时扫榜，看前 10-20 章）、深度细拆（挑完整故事单元逐章标记，反推"作者为什么这么安排"）。

**选书三原则**：拆近不拆远、拆同赛道、用榜单数据选书。

## 目录结构

```
.
├── skills/                  # 两个 AI 技能源码 + 可下载 zip
│   ├── chaishu/         #   拆书技能（五大维度手册/报告模板/HTML规范/仿写指南）
│   └── chaishu-builder/ #   知识库入库技能（追加格式规范）
├── src/chaishu/            # CLI 源码（零运行时依赖）
│   ├── cli.py               #   命令入口
│   ├── mdrender.py          #   Markdown 子集解析 + HTML 渲染
│   ├── render.py            #   报告组装：封面/目录/九大章节/红线页脚
│   ├── kb.py                #   五大维度规则化入库
│   ├── validate.py          #   报告完整性校验
│   ├── report.py / pack.py  #   骨架生成 / 技能打包
│   └── data/                #   报告骨架模板 + HTML 页面模板
├── tests/                   # pytest 测试（21 个用例）
└── docs/                    # 推广文章等文档
```

## 合规红线

- 拆**写作机制、情绪模型、节奏范式**，不窃取情节、人设、桥段；
- 借鉴骨架，拒绝复制血肉；拆书 ≠ 洗稿（洗稿是抄袭）；
- 报告不含书籍原文摘录，仿写片段必须换世界观、换人名、换能力；
- 请遵守目标作品所在平台规则与版权法律法规。

## 贡献

欢迎提交 PR：补充拆解维度检查清单、改进报告/HTML 模板、CLI 新功能（附测试）。参见 [CONTRIBUTING.md](./CONTRIBUTING.md)。

## License

[MIT](./LICENSE)
