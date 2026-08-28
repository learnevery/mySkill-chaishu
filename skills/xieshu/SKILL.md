---
name: xieshu
description: |
  网文写书技能，端到端创作一部完整小说。当用户想要写小说、写网文、创作故事、写章节正文、连载创作、写长篇、构思大纲、设计人设、写黄金三章、续写之前写到一半的小说时使用。流程：三层递进式问答定位（题材/主角/冲突必答，世界观/视角/主题可选）→ 生成大纲、人物档案、文风基准与写作计划 → 逐章创作（每章 3000-5000 字、章末悬念钩子、去 AI 味润色）→ 自动校验修复。可与 chaishu 拆书技能的知识库联动，用市场验证过的爽点、节奏、人设范式驱动创作。触发词：写小说、写书、创作小说、写网文、写正文、写章节、连载、写长篇、续写小说、小说大纲、小说人设、xieshu。
metadata:
  trigger: 创作中文小说、分章节故事、长篇网文创作
  source: 基于 penglonghuang/chinese-novelist-skill（MIT）改造，接入 chaishu 拆书知识库
---

# 写书（xieshu）：网文创作技能

端到端创作一部完整小说：从问答定位到逐章成稿，全程自动校验。搭配 chaishu 拆书技能时，直接用拆书沉淀的市场验证范式驱动创作，形成「拆 → 写」闭环。

## 三大黄金法则

1. **展示而非讲述** - 用动作和对话表现，不要直接陈述
2. **冲突驱动剧情** - 每章必须有冲突或转折
3. **悬念承上启下** - 每章结尾必须留下钩子

## 特性说明

- **拆书知识库联动**：检测 chaishu 拆书技能沉淀的知识库（人设/剧情/爽点/节奏/金手指/范式），规划与写作阶段直接套用市场验证过的范式。无知识库时使用内置通用指南，功能不受影响
- **中断续写**：自动检测未完成项目，从断点继续创作
- **自动校验**：创作完成后自动检查字数和质量，不合格自动修复
- **并行写作**（可选）：支持子 Agent 并行写作，通过 `02-写作计划.json` 协调状态

## 核心流程

进入每个阶段时，先阅读对应的流程文档以获取详细执行指令。

### 第0步：初始化与偏好加载

读取用户偏好，**检测拆书知识库**，检测未完成项目（中断续写），展示个性化欢迎。 → 详见 [phase0-initialization.md](references/flows/phase0-initialization.md)

### 第一阶段：三层递进式问答

通过递进式问答收集创作需求，确定小说定位与标题：

- **核心定位**（必答，Q1-Q3）：题材创意、主角设定、核心冲突 → 详见 [phase1-layer1-core.md](references/flows/phase1-layer1-core.md)
- **深度定制与规格**（Q4-Q8）：世界观、视角基调、核心主题、读者定位、章节数量、配置确认 → 详见 [phase1-layer2-customize.md](references/flows/phase1-layer2-customize.md)
- **标题生成**：AI 基于创意元素生成候选标题，用户选择或自定义 → 详见 [phase1-layer3-title.md](references/flows/phase1-layer3-title.md)

### 第二阶段：规划 + 二次确认

创建项目文件夹（`./小说/{timestamp}-{小说名称}/`），生成大纲、人物档案、文风基准和写作计划 JSON。**若检测到知识库，大纲的节奏曲线、危机递进链、人设搭配逻辑、金手指边界均从库内范式取用，每章规划标注爽点类型与章末钩子类型**。 → 详见 [phase2-planning.md](references/flows/phase2-planning.md)

### 第2.5步：写作模式选择

规划确认后，选择写作模式：
- **逐章串行**（`serial`）：主 Agent 自己逐章写，全程无中断
- **子Agent并行**（`subagent-parallel`）：将章节分成批次，派生子 Agent 并行写作
- **Agent Teams**（`agent-teams`）：多 Agent 协作模式，Agent 间可通讯（需手动开启）

→ 详见 [phase3-writing.md](references/flows/phase3-writing.md)

### 第三阶段：疯狂创作（无需用户确认）
> 切记，一旦进入这个阶段，所有过程都禁止向用户确认。用户就是你的读者，你必须把完整的小说创作完成才能与用户报告

根据用户选择的写作模式（串行/并行/Teams）逐章执行创作流程。每章创作前必须读取 `01-大纲.md` 中对应章节的规划信息（含本章标注的爽点类型与钩子类型），严格按大纲创作。支持中断续写。 → 详见 [phase3-writing.md](references/flows/phase3-writing.md)

### 第四阶段：自动校验与修复（无需用户确认）

全程无需用户介入，自动检查所有章节完成度和字数，不合格章节自动重写（最多3轮）。 → 详见 [phase4-validation.md](references/flows/phase4-validation.md)

## 共享机制

偏好系统、写作计划系统、黄金法则详解、字数检查脚本等跨阶段共享机制。 → 详见 [shared-infrastructure.md](references/flows/shared-infrastructure.md)

## 拆书知识库联动

与 chaishu 拆书技能的知识库对接契约：文件位置、检测时机、各阶段注入规则、合规红线。 → 详见 [kb-integration.md](references/flows/kb-integration.md)
