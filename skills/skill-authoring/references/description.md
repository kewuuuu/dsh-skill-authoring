# description：唯一触发面

读者只看得到 `name + description`，正文要等它主动加载。所以 description 的任务只有一个：回答“现在要不要读这份技能”。

## 句式

```
description: 用于 <做什么>。当用户说“<触发句 1>”“<触发句 2>”“<触发句 3>”时使用。
```

如有明确前置（必须先读到 A 才能用 B），把它写成一句限制，而不是塞进触发词里。

## 只写触发条件，不概括流程

实测结论（obra/superpowers `writing-skills` 的 SDO 节）：描述里概括了工作流，模型会照描述做，正文变成没人读的文档。

```yaml
# ❌ 概括了流程
description: Use when executing plans - dispatches subagent per task with code review between tasks

# ❌ 过程细节太多
description: Use for TDD - write test first, watch it fail, write minimal code, refactor

# ✅ 只给触发条件
description: Use when executing implementation plans with independent tasks in the current session
```

那次实验里，改回纯触发条件（“Use when executing implementation plans with independent tasks”）之后，模型才去读正文的两段审查流程。

## 具体、第三人称、可被说出口

```yaml
# ❌ 太抽象
description: For async testing

# ❌ 第一人称（会被注入系统提示）
description: I can help you with async tests when they're flaky

# ❌ 技能不限于某技术，却点名了实现细节
description: Use when tests use setTimeout/sleep and are flaky

# ✅ 描述问题与场景
description: Use when tests have race conditions, timing dependencies, or pass/fail inconsistently
```

中文场景同理：把用户真实会说错、会抱怨的形状写进去（“遗物不显示图片”“上传工坊失败”“订阅了没生效”），比只写术语更容易命中。

## 长度

- 一到三句，60–200 字符是常见区间。
- 1024 字符是规格上限，不是目标；超过说明你把流程写进来了。
- 不换行、不加列表：frontmatter 里换行会把 description 变成多行 YAML，注入时形状难控。

## 自测

1. 写出 3 条“应该命中”的用户原话，和 1 条“不该命中”的近邻请求。
2. 只看 description，判断该不该读这份技能；三条都要中，近邻要落空。
3. 做不到就改触发词，不要把正文内容搬进描述。
