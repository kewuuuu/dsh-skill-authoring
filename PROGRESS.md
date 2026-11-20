# PROGRESS

## 2026-11-20 立项：skill-authoring

- 读了三份同类材料（obra/superpowers、anthropics/skills、sentient-agi/meta-skill-creator）与两份移植向材料，确定只吸收与 DSH 事实相符的部分：description 只写触发条件（有实测反例支撑）、体积与渐进披露、脚本优先、缺能力写前置。
- 舍弃：anthropics skill-creator 的评测回路（依赖本机不存在的 Codex CLI）、mayurrathi 合集（Azure 专用 + 多为副本）。
- 产出 `skills/skill-authoring/`：SKILL.md 98 行、两份 references、一个纯标准库校验脚本。
- 决策：脚本里不能硬编码本机绝对路径（属于一次性事实），只用相对路径与参数；W8 检查就是为此存在的自检项。
- 决策：布局用 `skills/<name>/`，因为校验要求 name 与目录同名，而仓库根不能叫 skill-authoring。
- 装入 `dsh-packs/pack-test/skills/` 后，会话技能目录立即出现该条目（随包加载验证通过）。
- 用它对整合包 10 个 skill 做机械核查：0 error / 17 warn；人读项（叙事化、环境假设、触发词覆盖）另出报告，见 `docs/audit-2026-11-20.md`。
