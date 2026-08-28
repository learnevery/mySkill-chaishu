# xieshu · 网文写书技能

端到端创作一部完整小说：三层递进式问答定位 → 大纲/人物档案/文风基准规划 → 逐章创作（每章 3000-5000 字、章末悬念钩子、去 AI 味润色）→ 自动校验修复。支持中断续写与三种写作模式（串行 / 子 Agent 并行 / Agent Teams）。

## 与 chaishu 拆书技能联动

xieshu 可直接消费 chaishu 沉淀的拆书知识库（人设/剧情/爽点/节奏/金手指/范式）：

- **Phase 0**：自动检测知识库，报告积累规模（拆过几本书、覆盖哪些赛道）
- **Phase 1**：问答选项优先展示库内有同赛道积累的题材（标记📦）
- **Phase 2**：大纲的情绪曲线、危机递进链、人设搭配逻辑、金手指边界从库内范式取用；每章标注爽点类型与章末钩子类型
- **Phase 3**：每章写前按大纲标注回查知识库，取爽点的铺垫→释放结构和钩子写法落实到正文

无知识库时全部功能照旧，使用内置通用写作指南（13 种章末钩子、十种开头技巧、情节结构模板等）。

对接契约与合规红线详见 [references/flows/kb-integration.md](references/flows/kb-integration.md)：**借鉴骨架，拒绝复制血肉**——取用库内的机制与范式，情节、人物、桥段必须全新原创。

## 目录结构

```
xieshu/
├── SKILL.md                    # 技能定义与核心流程
├── references/
│   ├── flows/                  # 8 个流程文档 + 知识库对接契约
│   │   ├── phase0-initialization.md   # 初始化：偏好 + 知识库检测 + 中断续写
│   │   ├── phase1-layer1-core.md      # 核心定位问答（Q1-Q3）
│   │   ├── phase1-layer2-customize.md # 深度定制问答（Q4-Q8）
│   │   ├── phase1-layer3-title.md     # 标题生成
│   │   ├── phase2-planning.md         # 规划（知识库注入最重的阶段）
│   │   ├── phase3-writing.md          # 逐章创作（三种写作模式）
│   │   ├── phase4-validation.md       # 自动校验修复
│   │   ├── shared-infrastructure.md   # 共享机制（偏好/写作计划/黄金法则）
│   │   └── kb-integration.md          # chaishu 知识库对接契约
│   └── guides/                 # 9 个写作指南
│       ├── chapter-guide.md           # 章节写作（开头技巧/AI痕迹清除）
│       ├── hook-techniques.md         # 悬念钩子十三式 + 章首引子七式
│       ├── character-building.md      # 人物塑造
│       ├── dialogue-writing.md        # 对话写作
│       ├── plot-structures.md         # 情节结构模板
│       ├── content-expansion.md       # 内容扩充
│       ├── title-guide.md             # 标题创作
│       └── outline/character/chapter 模板
└── scripts/
    └── check_chapter_wordcount.py     # 章节字数校验（3000-5000 字）
```

## 使用

在支持 SKILL.md 的智能体平台导入本技能后，对 AI 说：

> 帮我写一部悬疑小说 / 续写我上次没写完的书

推荐先安装 [chaishu](../chaishu) 拆几本同赛道爆款入库，再触发本技能，创作质量直接吃市场验证过的范式。

## 来源与致谢

本技能基于 [penglonghuang/chinese-novelist-skill](https://github.com/penglonghuang/chinese-novelist-skill)（MIT License）改造：

- 重命名 `chinese-novelist` → `xieshu`，项目输出目录 `./chinese-novelist/` → `./小说/`
- 新增拆书知识库联动（`references/flows/kb-integration.md` 及各阶段的注入规则）
- 大纲模板章节规划表新增「爽点设计」列
- 移除原 README 中的第三方 API 推广内容与平台特定表述

感谢原作者 [@PenglongHuang](https://github.com/PenglongHuang) 的高质量基础。
