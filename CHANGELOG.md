# Changelog

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
