# 贡献指南

感谢关注 chaishu！这是一个面向网文作者的拆书工具箱，欢迎从以下几个方向贡献：

## 贡献方向

### 1. 方法论与技能

- 补充/修订 [五大维度拆解手册](./skills/chaishu/references/五大维度拆解手册.md) 的检查清单；
- 改进报告模板与 [HTML 输出规范](./skills/chaishu/references/html输出规范.md)；
- 新增赛道专属拆解维度（如女频、悬疑、无限流）。

修改技能源码后请执行 `chaishu pack` 重新打包，保持 zip 与源码同步。

### 2. CLI 代码

```bash
pip install -e ".[dev]"
pytest -q
```

- 新功能请附带测试（`tests/`）；
- 保持零运行时依赖；
- 注意 `src/chaishu/data/report-template.html` 与 `skills/chaishu/assets/report-template.html` 需保持同源同步，改动时两边一起改。

### 3. 提交规范

- PR 描述写清楚改了什么、为什么改；
- 涉及报告内容时，确保不含任何书籍原文摘录（合规红线见 README）。

## 行为准则

友善、就事论事、对事不对人。
