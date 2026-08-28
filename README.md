# chaishu · 网文拆书与写书工具箱

[![CI](https://github.com/learnevery/mySkill-chaishu/actions/workflows/ci.yml/badge.svg)](https://github.com/learnevery/mySkill-chaishu/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](./pyproject.toml)

**逆向解剖爆款网文，再用提炼出的范式写你自己的书。** 本项目把网文作者的行业基本功做成了开源工具箱：三个可直接安装的 AI 技能 + 一个零依赖的 Python 命令行工具，覆盖 **拆 → 入库 → 写 → 校验** 完整闭环。

> 拆书研究"这本书为什么火"的工业化叙事逻辑（开篇钩子、人设体系、节奏情绪曲线、大纲结构、赛道偏好）；写书则用这些市场验证过的范式驱动创作。只借鉴骨架、不复制血肉。

## 解决什么问题

| 痛点 | 工具箱的解法 |
|------|-------------|
| 拆书靠悟性——看爆款只知道"好看"，扒不出为什么好看 | `chaishu` 按五大维度结构化拆解，附检查清单、逐章标记表与报告模板 |
| 拆完就忘——经验散落各处笔记，写书时想不起来用 | `chaishu-builder` / `chaishu kb add` 把精华沉淀到六个知识库文件，随拆随积累 |
| AI 写书没有依据——通用 AI 只有套路，不含市场验证 | `xieshu` 自动检测知识库，用拆出的爽点、节奏、人设范式驱动大纲与逐章创作 |
| 写不完——开篇三章就太监 | `xieshu` 问答定位后全自动逐章推进，字数与连贯性自动校验，支持中断续写 |

## 核心组成

| 组件 | 说明 |
|------|------|
| `skills/chaishu` | AI 拆书技能：五大维度拆解、粗拆/深度细拆双模式、仿写训练，产出 MD + 精排版 HTML 双格式报告 |
| `skills/chaishu-builder` | AI 入库技能：把拆书精华持续沉淀到 人设/剧情/爽点/节奏/金手指/范式 知识库 |
| `skills/xieshu` | AI 写书技能：端到端创作整部小说——问答定位、大纲规划、逐章创作、自动校验；自动检测并消费上述知识库 |
| `chaishu` CLI | 命令行工具：报告骨架生成、MD→HTML 渲染、报告校验、规则化知识库入库、技能打包，**不依赖 AI 也能跑通拆书侧全流程** |

## 完整工作流

知识库是拆与写之间的桥：拆书侧往里沉淀，写书侧取用。

```
chaishu 拆书 ──→ 拆书报告 ──→ kb add / chaishu-builder ──→ 知识库（6 个 md 文件）
（五大维度）      （MD+HTML）                             （人设/剧情/爽点/节奏/金手指/范式）
                                                                      │
                                                                      ▼
xieshu 写书：Phase 0 检测知识库 → 问答选项带同赛道推荐 → 大纲套用库内
情绪曲线/人设搭配/金手指边界 → 每章按大纲标注回查爽点写法与钩子样式 → 自动校验 → 成稿
```

### 快速开始：三步走完闭环

```bash
# 安装（Python 3.9+，零运行时依赖）
pip install -e .

# 第一步：拆一本同赛道爆款
chaishu new 神通者 --mode deep                  # 生成报告骨架（AI 对话填写，或手工填写）
chaishu validate 拆书/拆书报告-神通者-深度细拆.md   # 校验完整性（必填章节/作者目的列/范式仿写）
chaishu build 拆书/拆书报告-神通者-深度细拆.md      # 渲染精排版 HTML，浏览器阅读/分享

# 第二步：精华入库（重复自动去重，跨书持续积累）
chaishu kb add 拆书/拆书报告-神通者-深度细拆.md
chaishu kb stats                                # 查看各知识库条目数

# 第三步：基于知识库写书
# 在智能体平台对 AI 说"帮我写一部XX小说"（触发 xieshu 技能）
# 产出 ./小说/{时间戳}-{书名}/：大纲、人物档案、文风基准、写作计划、各章正文
```

> 拆书报告的填写与 xieshu 的创作由 AI 技能在对话中完成；CLI 负责骨架、校验、渲染、入库等确定性环节——没有 AI 也能跑通拆书侧全流程。

## 技能详解

### chaishu — 拆书：逆向解剖爆款

按**五大维度**结构化拆解：① 卖点与开篇（黄金三章、章末钩子类型、信息抛出顺序）② 人设体系（主角欲望痛点、金手指边界、配角反派衬托）③ 节奏与情绪曲线（爽点铺垫与释放比例、高潮密度，最核心）④ 大纲与故事结构（主线分卷、危机递进）⑤ 赛道读者偏好（吃哪种梗、雷点清单）。

**两种模式**：粗拆（1-2 小时扫榜，看前 10-20 章，批量摸风向）／深度细拆（挑完整故事单元逐章标记，反推"作者为什么这么安排"）。**选书三原则**：拆近不拆远、拆同赛道、用榜单数据选书。

每份报告必含**可复用范式清单 + 仿写训练片段 + 内化行动清单**——只拆不写等于白拆。

### chaishu-builder — 入库：让积累可检索

每次拆完，把人设搭配逻辑、剧情模块、爽点结构（铺垫→释放比例）、节奏模板、金手指边界分别追加到六个知识库文件，条目带来源标注、重复自动去重。知识库随拆书持续变厚，成为个人的创作弹药库。

### xieshu — 写书：端到端创作整部小说

完整流程：**三层递进问答**（题材/主角/冲突必答；世界观/视角/主题/读者/章节数可选，支持随机与跳过）→ **规划**（大纲、人物档案、文风基准、机器可读的写作计划）→ **逐章创作**（每章 3000-5000 字，章首引子 + 章末悬念钩子，对话占比 ≥30%，深度润色去 AI 味）→ **自动校验修复**（字数与连贯性，不合格自动重写，最多 3 轮）。支持**中断续写**与三种写作模式（串行 / 子 Agent 并行 / Agent Teams）。

**知识库联动**（无知识库时独立工作，使用内置通用写作指南）：

| 写书阶段 | 读取 | 用法 |
|---------|------|------|
| Phase 0 初始化 | 全部 | 检测知识库，报告积累规模（拆过几本、覆盖哪些赛道） |
| Phase 1 问答 | 剧情/爽点 | 题材选项标记📦同赛道积累，冲突选项纳入库内高频类型 |
| Phase 2 规划 | 节奏/剧情/人设/金手指/范式 | 情绪曲线、危机递进链、人设搭配逻辑、金手指边界从库内取；每章标注爽点与钩子类型 |
| Phase 3 写作 | 爽点/范式 | 每章写前回查本章爽点的铺垫→释放结构与钩子写法 |

对接契约详见 [skills/xieshu/references/flows/kb-integration.md](./skills/xieshu/references/flows/kb-integration.md)。

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

1. 下载 [skills/chaishu.zip](./skills/chaishu.zip)、[skills/chaishu-builder.zip](./skills/chaishu-builder.zip) 与 [skills/xieshu.zip](./skills/xieshu.zip)；
2. 在支持 SKILL.md 的智能体平台中执行技能导入（如 `/install-capability`），选择本地 zip 导入；
3. 推荐搭配：先用 `chaishu` 拆书写报告，用 `chaishu-builder`（或 `chaishu kb add`）把精华沉淀进知识库，最后用 `xieshu` 基于知识库写自己的书。

技能源码就是仓库里的 `skills/` 目录，修改后执行 `chaishu pack` 重新打包。

## 目录结构

```
.
├── skills/                  # 三个 AI 技能源码 + 可下载 zip
│   ├── chaishu/         #   拆书技能（五大维度手册/报告模板/HTML规范/仿写指南）
│   ├── chaishu-builder/ #   知识库入库技能（追加格式规范）
│   └── xieshu/          #   写书技能（9 流程文档 + 10 写作指南 + 字数校验脚本）
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
- `xieshu` 取用知识库时只复用机制与范式，产出的大纲与正文必须原创；
- 请遵守目标作品所在平台规则与版权法律法规。

## 贡献

欢迎提交 PR：补充拆解维度检查清单、改进报告/HTML 模板、CLI 新功能（附测试）。参见 [CONTRIBUTING.md](./CONTRIBUTING.md)。

## 致谢

`skills/xieshu` 基于 [penglonghuang/chinese-novelist-skill](https://github.com/penglonghuang/chinese-novelist-skill)（MIT）改造，感谢原作者 [@PenglongHuang](https://github.com/PenglongHuang)。

## License

[MIT](./LICENSE)
