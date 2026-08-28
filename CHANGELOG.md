# Changelog

## 0.2.0 (2026-08-28)

新增写书技能 `skills/xieshu`，仓库从"拆书工具箱"升级为"拆 → 入库 → 写 → 校验"全闭环。

- 写书技能 `xieshu`（基于 penglonghuang/chinese-novelist-skill MIT 改造，署名致谢）：
  - 端到端创作：三层递进式问答 → 大纲/人物档案/文风基准规划 → 逐章创作（3000-5000 字/章、章末悬念钩子、去 AI 味润色）→ 自动校验修复（最多 3 轮）；
  - 中断续写（`02-写作计划.json` 断点检测）与三种写作模式（串行 / 子 Agent 并行 / Agent Teams）；
  - 拆书知识库联动：Phase 0 检测 → 问答推荐 → 规划注入（情绪曲线/危机递进/人设搭配/金手指边界）→ 每章写前回查爽点与钩子写法；无知识库时独立工作；
  - 大纲模板章节规划表新增「爽点设计」列；对接契约见 `skills/xieshu/references/flows/kb-integration.md`；
  - 移除原项目第三方 API 推广内容，输出目录改为 `./小说/`；
- README 重写为全闭环叙事，新增「拆 → 写 闭环」章节与致谢。

## 0.1.0 (2026-08-28)

首个开源版本。

- 拆书技能 `chaishu`：五大维度拆解、粗拆/深度细拆双模式、仿写训练、MD + HTML 双格式报告；
- 入库技能 `chaishu-builder`：拆书精华沉淀到 人设/剧情/爽点/节奏/金手指 知识库；
- `chaishu` CLI（零运行时依赖）：
  - `new` 报告骨架生成；
  - `build` Markdown → 精排版 HTML 渲染（复用技能同款模板）；
  - `validate` 报告完整性校验（必填章节 / 作者目的列 / 占位符 / 范式仿写内化）；
  - `kb add` / `kb stats` 规则化知识库入库与统计（重复自动去重）；
  - `pack` 技能打包（UTF-8 文件名，确定性产出）；
- pytest 测试 21 例；GitHub Actions CI（Ubuntu/Windows × Python 3.9-3.12）；
- MIT License。
