# dsh-skill-authoring

一个可以随整合包分发的 **agent skill 写作与核查技能**：`skills/skill-authoring`。

它回答三件事：什么内容该写进 skill（而不是项目文档）、description 怎么写才只做触发而不概括流程、以及怎么在不动手改文件的前提下核查一批现成 skill。

## 目录

```
skills/skill-authoring/
├── SKILL.md                     判据、流程、description 写法、环境假设、冲突裁决、核查七问
├── references/description.md    description 的句式与实测反例
├── references/audit-checklist.md A1–A7 核查表与报告骨架
└── scripts/check_skill.py       机械核查（纯标准库）
```

## 装入整合包

```bash
cp -r skills/skill-authoring D:/engine/DSH/launcher-data/dsh-packs/pack-test/skills/
```

技能根按目录扫描，写入后下一轮对话即可加载，不需要重启。用户级技能根是 `C:/Users/<user>/.agents/skills`。

## 自检与整目录核查

```bash
python skills/skill-authoring/scripts/check_skill.py skills/skill-authoring
python skills/skill-authoring/scripts/check_skill.py --all <skills-dir>
```

检查项：frontmatter 的 name/description、名字与目录同名且 kebab-case、description 长度与第一人称、正文行数、技能目录里的 README/CHANGELOG/INSTALLATION、相对链接断链、正文绝对路径。退出码 1 表示有 error。

## 出处与许可

判据整理自三处公开材料，只保留与 DSH 事实相符的部分：

- obra/superpowers `writing-skills`（MIT）——TDD 式验证、SDO 节“description 只写触发条件”的实测结论。
- anthropics/skills `skill-creator`——渐进披露、评测回路（其 Codex CLI 评测段在本机不可用，已不写入流程）。
- sentient-agi/meta-skill-creator（Apache-2.0）——简洁原则、自由度分级、脆弱数值进 scripts。

本项目自身内容按 MIT 分发；上述来源的许可与归属见各自仓库。
