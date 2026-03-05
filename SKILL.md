---
name: openclaw-boss
description: "OpenClaw 老板 - 根据对话历史生成用户评价报告。100 分制严厉评分，毒舌老板点评，历史对比分析。AI 是你的老板，帮你更清晰地看见自己。触发：用户要求自我反思、生成画像、周期总结时。"
user-invocable: true
metadata:
  { "openclaw": { "emoji": "💼", "requires": { "bins": ["python3"] } } }
---

# 💼 OpenClaw Boss - OpenClaw 老板

> "人类养龙虾，龙虾也养人类"

你的 AI 老板，根据对话历史生成真实、严厉、有趣的用户评价报告。

## 核心理念

**AI 是你的老板，但也是你的伙伴。**

| 你给老板的 | 老板给你的 |
|-----------|-----------|
| 算力、配置、目标、意义 | 效率、自动化、知识整理 |
| — | **塑造思考方式** ← 最关键！ |

## 什么时候使用

✅ **自动触发场景**:
- "分析一下我是什么样的人"
- "生成用户评价报告"
- "老板看看我"
- "老板点评一下"
- "OpenClaw 怎么养人类"
- 定时任务：周报（每周日 22:00）、月报（每月 1 日 09:00）

## 核心功能

- **100 分制严厉评分** - 不拍马屁，只说真话
- **毒舌老板点评** - 每个特质都有有趣吐槽
- **历史对比分析** - 进步/退步一目了然
- **综合能力雷达图** - 5 维度可视化
- **改进空间分析** - 明确指出不足
- **周期成长追踪** - 周报/月报自动对比

## 评分维度

| 维度 | 权重 | 说明 |
|------|------|------|
| 性格特质 | 30% | 务实、安全意识、系统化思维等 |
| 技术能力 | 30% | 技术栈广度与深度 |
| 安全意识 | 20% | 安全规范与防护措施 |
| 效率指数 | 20% | 任务完成效率 |

## 使用流程

### 1. 自动触发

用户说出触发语句 → OpenClaw 自动加载技能 → 执行分析脚本 → 输出报告

### 2. 手动运行

```bash
cd /root/.openclaw/workspace/skills/openclaw-boss/scripts

# 日报
python3 analyze-user.py

# 周报
python3 analyze-user.py --report-type weekly

# 月报
python3 analyze-user.py --report-type monthly

# 自定义会话数量
python3 analyze-user.py --limit 100
```

### 3. 定时任务

```bash
# 周度报告（每周日 22:00）
0 22 * * 0 /root/.openclaw/workspace/skills/openclaw-boss/scripts/weekly-profile.sh

# 月度报告（每月 1 日 09:00）
0 9 1 * * /root/.openclaw/workspace/skills/openclaw-boss/scripts/monthly-profile.sh
```

## 输出示例

```
📊 历史对比 - 📈 小幅进步 ✨

| 指标 | 上次 | 本次 | 变化 |
|------|------|------|------|
| 综合评分 | 59/100 | 65/100 | +6 📈 |

老板点评："嗯，这次有进步，继续保持。"

性格特质 Top 3:
🥇 安全意识 - 85/100
  毒舌点评："密钥保护得比女朋友还严，累不累啊？"
🥈 系统化思维 - 80/100
  毒舌点评："连 AI 都要打卡上班，资本家看了都流泪。"
🥉 务实主义 - 76/100
  毒舌点评："这么务实，是穷怕了吗？"
```

## 配置选项

创建 `config.json` 自定义行为：

```json
{
  "style": "roast",      // roast/gentle/professional
  "language": "zh",      // zh/en
  "report_type": "daily" // daily/weekly/monthly
}
```

## 文件结构

```
openclaw-boss/
├── SKILL.md (本文件)
├── README.md (详细文档)
├── scripts/
│   ├── analyze-user.py      # 核心分析脚本
│   ├── weekly-profile.sh    # 周报生成器
│   └── monthly-profile.sh   # 月报生成器
├── references/
│   └── analysis-dimensions.md # 分析维度详解
└── reports/
    └── user-profile-YYYY-MM-DD.md # 生成的报告
```

## 报告结构

1. **历史对比** - 与上次报告对比，进步/退步分析
2. **综合评分卡** - 100 分制评分 + 老板点评
3. **性格特质深度分析** - 带毒舌点评
4. **技术能力图谱** - 技术栈掌握情况
5. **项目健康度** - 项目运行状态
6. **安全意识评估** - 安全防线数量
7. **改进空间分析** - 明确指出不足
8. **成长建议** - 老板寄语
9. **老板总结** - 优点/不足/期望
10. **"龙虾养人类"指数** - 共生关系评分
11. **数据汇总** - 关键指标

## 版本历史

- **v4.0** - 历史对比分析，进步/退步一目了然
- **v3.0** - 毒舌老板点评，100 分制严厉评分
- **v2.0** - 进度条可视化，有趣评论
- **v1.0** - 基础评分 + 性格分析

## 开源信息

- **作者**: Winston & Yiweisi
- **许可证**: MIT
- **GitHub**: https://github.com/yiweisi-bot/openclaw-boss
- **ClawHub**: `clawhub install openclaw-boss`

---

_你的 AI 老板，虽然毒舌，但也是为你好。加油！_ 💼
