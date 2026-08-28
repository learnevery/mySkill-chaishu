# 第二阶段：规划 + 二次确认

> **前置条件**：本阶段使用 Phase 1 Layer 3 用户确认的小说标题。标题信息从对话上下文中获取，用于命名项目目录、写入大纲文件头和写作计划 JSON。

执行以下步骤：

1. **创建项目文件夹**：`./小说/{YYYYMMDD-HHmmss}-{Layer 3 确认的标题}/`（相对当前工作目录，使用用户在 Layer 3 选定的小说标题）
2. **生成人物档案**：创建 `00-人物档案.md`，使用 [character-template.md](../guides/character-template.md) 模板，参考 [character-building.md](../guides/character-building.md) 创建主角、反派、配角档案。**人物档案必须详细**：每个角色的性格核心、致命缺陷、说话风格/口头禅、恐惧/弱项、背景故事都要具体到可以直接指导写作的程度
   - **知识库联动**（如有）：主角与配角的搭配逻辑参考 `人设.md` 中的「人设搭配逻辑」条目（如"高冷主角+话痨配角"的反差结构）；反派的压迫力来源参考库内同类拆解。**只借鉴搭配结构，人物的具体身份、姓名、背景必须全新**
3. **生成大纲**：创建 `01-大纲.md`，使用 [outline-template.md](../guides/outline-template.md) 模板，参考 [plot-structures.md](../guides/plot-structures.md) 填入完整的章节规划。**大纲必须以人物驱动情节** 参照 `00-人物档案.md`，确保情节服务于人物成长弧线
   - **知识库联动**（如有，注入规则详见 [kb-integration.md](kb-integration.md)）：
     - 情绪曲线与高潮密度参照 `节奏.md` 中的曲线模板（铺垫-高潮-回落-再铺垫的节奏和比例）
     - 危机递进链参考 `剧情.md` 中同赛道的危机递进设计
     - 金手指的边界、使用代价、升级频率参考 `金手指.md` 条目，确保金手指驱动剧情而不是让剧情失效
     - **章节规划表的「爽点设计」列从 `爽点.md` 的有效爽点清单选型，「悬念钩子」列优先选 `范式.md` 中该赛道高频钩子类型**；每章的爽点铺垫→释放比例参照库内拆解结论
   - **合规**：所有取自知识库的仅是机制和范式（骨架），章节的具体事件、情节链必须为本书原创
3.5. **生成文风基准**：创建 `03-文风基准.md`，包含四部分：
   - **文风指纹**：对话占比目标（默认 35%-45%）、句子节奏（短句为主、动作段≤10字）、段落呼吸、叙述距离、描写倾向，基于 Layer 2 已有的基调/风格参考/目标读者生成
   - **基准段落**：2 段体现目标文风的正文范例（各 500-800 字）。用户在问答中提供过喜欢的作品片段则直接采用
   - **负面清单**：引用 [chapter-guide.md](../guides/chapter-guide.md)「AI 写作痕迹清除」条目
   - **本书校准段落**：（初始为空，第 1 章完成后由 Phase 3 回填）
4. **生成写作计划**：创建 `02-写作计划.json`，基于大纲内容填充，结构如下：
   ```json
   {
     "version": 1,
     "novelName": "[小说名称]",
     "projectPath": "./小说/{timestamp}-[小说名称]",
     "totalChapters": [章节数],
     "minWordsPerChapter": 3000,
     "createdAt": "[ISO时间]",
     "updatedAt": "[ISO时间]",
     "status": "planning",
     "writingMode": "[serial|subagent-parallel|agent-teams]",
     "chapters": [
       {
         "chapterNumber": 1,
         "title": "[章节标题]",
         "filePath": "第01章-[章节标题].md",
         "status": "pending",
         "wordCount": null,
         "wordCountPass": null,
         "retryCount": 0
       }
     ]
   }
   ```

完成后，执行以下两步：

**1. 展示规划摘要并请求确认**

向用户展示规划摘要（小说名称、总章数、目标字数、主要人物、文风基准来源）并请求确认。

**2. 写作模式选择**（用户确认规划后）

使用 `AskUserQuestion` 询问：

```
Question: 选择写作模式
Options:
- 逐章串行（主 Agent 自己逐章写，全程无中断，适合短中篇）
- 子Agent并行（分批派生子 Agent 并行写作，大纲驱动连贯性，适合中长篇）
- Agent Teams（多 Agent 协作模式，Agent 间可通讯，需手动开启）
```

用户选择后：
- 更新 `02-写作计划.json` 的 `writingMode` 字段
- 更新 `status` 为 `"in_progress"`
- 进入第三阶段：疯狂创作 → 详见 [phase3-writing.md](phase3-writing.md)
