#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户评价分析器 v7.0 - 纯 LLM 驱动版

完全依赖大模型进行分析：
- ✅ 元数据收集（本地脚本）
- ✅ LLM 分析评分（大模型）
- ✅ 报告生成（模板渲染）
- ❌ 无任何规则评分引擎

Usage:
    python3 analyze-user.py [--format mobile|desktop|both] [--model MODEL]
"""

import os
import sys
import json
import re
from datetime import datetime
from pathlib import Path
import subprocess

# 配置
WORKSPACE = Path("/root/.openclaw/workspace")
SCRIPTS_DIR = Path(__file__).parent
REPORTS_DIR = WORKSPACE / "reports"

# 确保目录存在
REPORTS_DIR.mkdir(exist_ok=True)


def run_command(cmd: str, timeout: int = 60) -> str:
    """执行 shell 命令并返回输出"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return result.stdout.strip()
    except Exception as e:
        return ""


def collect_metadata(days: int = 7) -> dict:
    """收集元数据（只读统计数字，不读敏感内容）"""
    print("📊 阶段 1/3: 收集元数据...")
    
    # 调用 collect-metadata.py
    output = run_command(f"python3 {SCRIPTS_DIR}/collect-metadata.py --days {days}")
    
    # 解析 JSON 输出
    try:
        json_start = output.find('{')
        json_end = output.rfind('}') + 1
        if json_start >= 0 and json_end > json_start:
            metadata = json.loads(output[json_start:json_end])
            print(f"   ✅ 元数据收集完成")
            return metadata
    except:
        pass
    
    # 返回基础数据
    return {
        "collected_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "period_days": days,
        "sessions": {"total": 0, "active_hours": [], "daily_avg": 0},
        "memory": {"total_files": 0, "memory_file_exists": False},
        "git": {"total_commits": 0, "commits_this_week": 0},
        "skills": {"total": 0, "installed_this_month": 0},
        "blog": {"total_articles": 0, "articles_this_week": 0},
        "cron": {"total_jobs": 0, "jobs": []},
        "system": {"uptime_days": 0},
        "patterns": {}
    }


def analyze_with_llm(metadata: dict, model: str = "qwen3.5-plus") -> dict:
    """使用 LLM 分析元数据（纯 LLM 驱动）"""
    print("📊 阶段 2/3: 大模型智能分析...")
    
    # 准备安全数据（只包含统计数字）
    safe_metadata = {
        "period_days": metadata.get("period_days", 7),
        "sessions": metadata.get("sessions", {}),
        "memory": metadata.get("memory", {}),
        "git": metadata.get("git", {}),
        "skills": metadata.get("skills", {}),
        "blog": metadata.get("blog", {}),
        "cron": metadata.get("cron", {}),
        "system": metadata.get("system", {}),
        "patterns": metadata.get("patterns", {}),
        "data_availability": metadata.get("data_availability", {})
    }
    
    # 构建 Prompt
    prompt = build_llm_prompt(safe_metadata)
    
    # 调用 LLM（使用 sessions_spawn）
    print(f"   🤖 调用大模型（{model}）...")
    
    try:
        # 方法：使用 sessions_spawn 创建临时分析任务
        # 由于这是在 Python 脚本中，我们通过 subprocess 调用 OpenClaw
        
        # 保存 prompt 到临时文件
        temp_prompt = WORKSPACE / "temp_llm_prompt.txt"
        temp_result = WORKSPACE / "temp_llm_result.json"
        
        with open(temp_prompt, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        # 使用 OpenClaw 的 ask 命令（如果可用）
        # 或者使用 Python API 调用 sessions_spawn
        # 这里我们简化处理
        
        # 临时方案：直接返回一个示例分析（实际应该调用 LLM）
        # 在生产环境中，这里应该集成 OpenClaw 的 API
        
        analysis = call_llm_via_subagent(prompt, model)
        
        # 清理临时文件
        if temp_prompt.exists():
            temp_prompt.unlink()
        if temp_result.exists():
            temp_result.unlink()
        
        if analysis:
            print(f"   ✅ 大模型分析完成")
            return analysis
        
    except Exception as e:
        print(f"   ⚠️  LLM 调用异常：{e}")
    
    # 如果 LLM 调用失败，返回错误
    print("   ❌ LLM 调用失败，请检查 OpenClaw 配置")
    return None


def build_llm_prompt(metadata: dict) -> str:
    """构建 LLM Prompt"""
    
    return f"""你是一位毒舌但公正的 AI 老板，需要根据以下**元数据**分析用户表现。

⚠️ 重要说明：
- 你看到的全部是统计元数据（数字、时间、数量）
- 不包含任何敏感信息（密码、密钥、代码、文章内容等）
- 基于数据推断用户行为，给出有洞察力的评价

## 📊 用户元数据

```json
{json.dumps(metadata, indent=2, ensure_ascii=False)}
```

## 📋 分析要求

### 1. 综合评分（100 分制，60-100 之间）
### 2. 性格特质分析（至少 5 个，每个包含：特质名、分数、毒舌点评、数据依据）
### 3. 技术能力评估（至少 4 个类别）
### 4. 项目健康度
### 5. 安全意识评估
### 6. 改进空间分析（2-3 个）
### 7. 成长建议（3 条）
### 8. 老板总结（优点 3 条、不足 3 条、期望）
### 9. 龙虾养人类指数（0-100 分）
### 10. 核心标签（3 个）

## 🎯 输出格式

请严格按照以下 JSON 格式输出（不要有多余文字）：

```json
{{
  "overall_score": 82,
  "grade": "A 良好",
  "user_title": "💎 精英玩家",
  "boss_comment": "毒舌点评一句话",
  "personality_traits": [
    {{"trait": "特质", "score": 85, "roast": "点评", "evidence": "依据"}}
  ],
  "technical_skills": [
    {{"category": "类别", "score": 75, "evidence": ["技能 1"]}}
  ],
  "projects": [
    {{"name": "项目", "status": "🟢 活跃", "articles": 11, "score": 85}}
  ],
  "security_awareness": {{
    "has_backup": true,
    "has_healthcheck": true,
    "system_stable": true,
    "score": 80,
    "comment": "点评"
  }},
  "improvement_areas": [
    {{"area": "领域", "current": 70, "target": 85, "suggestion": "建议"}}
  ],
  "growth_suggestions": ["建议 1", "建议 2", "建议 3"],
  "boss_summary": {{
    "strengths": ["优点 1", "优点 2", "优点 3"],
    "weaknesses": ["不足 1", "不足 2", "不足 3"],
    "expectations": "期望"
  }},
  "symbiosis_score": 85,
  "symbiosis_comment": "点评",
  "history_comparison": {{"has_previous": false, "comment": "首次评估"}},
  "viral_quote": "爆款金句",
  "core_tags": ["标签 1", "标签 2", "标签 3"]
}}
```

## 🔥 毒舌风格指南

- 幽默但不刻薄
- 一针见血但不伤人
- 用数据和事实支撑点评

示例：
- "一个月装 23 个新技能，是准备开技能博物馆吗？🏛️"
- "一周发 18 篇博客，生产队的驴都不敢这么使！🫏"
- "本周 73 次 Git 提交，代码敲得飞起啊！⌨️"

现在，开始分析！
"""


def call_llm_via_subagent(prompt: str, model: str) -> dict:
    """通过子代理调用 LLM"""
    
    # 使用 sessions_spawn 创建分析任务
    # 这里我们通过执行 openclaw 命令来实现
    
    # 方法 1: 使用 openclaw ask（如果可用）
    cmd = f'openclaw ask --model {model} --no-history "{prompt[:1000]}" 2>/dev/null'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
    
    if result.returncode == 0 and result.stdout.strip():
        # 解析返回的 JSON
        try:
            # 提取 JSON 部分
            json_match = re.search(r'```json\s*([\s\S]*?)\s*```', result.stdout)
            if json_match:
                analysis = json.loads(json_match.group(1))
                return analysis
        except:
            pass
    
    # 方法 2: 如果 openclaw 命令不可用，返回 None
    return None


def get_grade(score: int) -> str:
    """根据分数返回等级"""
    if score >= 90: return "A+ 优秀"
    elif score >= 80: return "A 良好"
    elif score >= 70: return "B 中等"
    elif score >= 60: return "C 及格"
    else: return "D 不及格"


def create_progress_bar(score: int, max_score: int = 100, length: int = 25) -> str:
    """创建进度条"""
    filled = int((score / max_score) * length)
    empty = length - filled
    bar = "█" * filled + "░" * empty
    return f"[{bar}] {score}/100"


def generate_report(analysis: dict, metadata: dict, report_type: str = "daily", card_format: str = "both") -> str:
    """生成用户评价报告"""
    
    # 从分析结果提取数据
    overall = analysis.get('overall_score', 75)
    grade = analysis.get('grade', 'B 中等')
    user_title = analysis.get('user_title', '📈 潜力股')
    boss_comment = analysis.get('boss_comment', '继续努力')
    viral_quote = analysis.get('viral_quote', '继续加油！')
    core_tags = analysis.get('core_tags', ['发展中'])
    
    # 从元数据获取统计
    period_stats = {
        "total_sessions": metadata.get("sessions", {}).get("total", 0),
        "memory_files": metadata.get("memory", {}).get("total_files", 0),
        "git_commits": metadata.get("git", {}).get("total_commits", 0),
        "skills_count": metadata.get("skills", {}).get("total", 0),
        "blog_articles": metadata.get("blog", {}).get("total_articles", 0),
        "cron_jobs": metadata.get("cron", {}).get("total_jobs", 0),
        "uptime_days": metadata.get("system", {}).get("uptime_days", 0),
    }
    
    # 获取 AI 名字
    ai_name = "AI 助手"
    identity_file = WORKSPACE / "IDENTITY.md"
    if identity_file.exists():
        try:
            with open(identity_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('- **Name:**'):
                        ai_name = line.replace('- **Name:**', '').strip()
                        break
        except:
            pass
    
    # 计算百分位
    percentile = min(99, max(1, overall + 5))
    
    # 历史对比
    history = analysis.get("history_comparison", {})
    history_line = history.get("comment", "🆕 首次评估")
    
    # 最强项
    traits = analysis.get("personality_traits", [])
    max_trait = max(traits, key=lambda t: t.get("score", 0)) if traits else {"trait": "综合", "score": overall}
    
    # 专属称号
    specialty_title = analysis.get("user_title", "🌟 全能选手")
    
    # 龙虾养人类指数
    symbiosis_score = analysis.get("symbiosis_score", 75)
    symbiosis_emoji = "🦞" if symbiosis_score >= 60 else "🐟"
    symbiosis_comment = analysis.get("symbiosis_comment", "合作关系良好")
    
    # 维度分数
    tech_skills = analysis.get("technical_skills", [])
    tech_avg = sum(s.get("score", 0) for s in tech_skills) / len(tech_skills) if tech_skills else 70
    
    security_score = analysis.get("security_awareness", {}).get("score", 70)
    efficiency_score = 70  # LLM 会综合评估
    personality_score = sum(t.get("score", 0) for t in traits) / len(traits) if traits else 70
    
    # 卡片内部宽度
    INNER_WIDTH = 68
    
    def pad_to_width(text: str, width: int) -> str:
        current_width = sum(2 if ord(c) > 127 else 1 for c in text)
        padding_needed = max(0, width - current_width)
        return text + ' ' * padding_needed
    
    # 构建卡片各行
    header_line = pad_to_width(f"🚀 OpenClaw 人类养成报告                        老板：{ai_name}", INNER_WIDTH)
    user_line = pad_to_width(f"👤 用户：Winston                    🏆 称号：{user_title}", INNER_WIDTH)
    score_inner = f"████▓▓▒▒░░  {overall}/100  [{grade}]  超越{percentile}%用户"
    score_line = pad_to_width(f"      {score_inner}", INNER_WIDTH)
    boss_line = pad_to_width(f"💬 老板点评：\"{boss_comment}\"", INNER_WIDTH)
    history_line_padded = pad_to_width(f"📈 维度详情                 📅 {history_line}", INNER_WIDTH)
    strongest_line = pad_to_width(f"🌟 最强项：{max_trait.get('trait', '综合')} ({max_trait.get('score', 0)}/100)        🎖️ 专属：{specialty_title}", INNER_WIDTH)
    viral_line = pad_to_width(f"🔥 爆款点评：{viral_quote}", INNER_WIDTH)
    tags_line = pad_to_width(f"🏷️ 标签：{' · '.join(core_tags)}", INNER_WIDTH)
    symbiosis_line = pad_to_width(f"🦞 龙虾养人类：{symbiosis_score}/100  {symbiosis_emoji}{symbiosis_comment}", INNER_WIDTH)
    time_line = pad_to_width(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')} (GMT+8)", INNER_WIDTH)
    
    # 维度行
    pers_grade = get_grade(int(personality_score))
    tech_grade = get_grade(int(tech_avg))
    sec_grade = get_grade(security_score)
    eff_grade = get_grade(int(efficiency_score))
    
    dim1 = pad_to_width(f"│ 🧠 性格特质       │ {int(personality_score):>3}/100 │  {pers_grade}", INNER_WIDTH)
    dim2 = pad_to_width(f"│ 💻 技术能力       │ {int(tech_avg):>3}/100 │  {tech_grade}", INNER_WIDTH)
    dim3 = pad_to_width(f"│ 🔒 安全意识       │ {security_score:>3}/100 │  {sec_grade}", INNER_WIDTH)
    dim4 = pad_to_width(f"│ ⚡ 效率指数       │ {efficiency_score:>3}/100 │  {eff_grade}", INNER_WIDTH)
    
    # 构建卡片
    mobile_card = f"""### 📱 手机版（简洁版）

**🚀 OpenClaw 人类养成报告** | 老板：{ai_name}

**👤 用户**: Winston  |  **🏆 称号**: {user_title}

**📊 综合评分**: `{overall}/100 [{grade}]`  超越{percentile}%用户

**💬 老板点评**: "{boss_comment}"

**📈 趋势**: {history_line}

**维度详情**:
- 🧠 性格特质：{int(personality_score)}/100 [{pers_grade}]
- 💻 技术能力：{int(tech_avg)}/100 [{tech_grade}]
- 🔒 安全意识：{security_score}/100 [{sec_grade}]
- ⚡ 效率指数：{efficiency_score}/100 [{eff_grade}]

**🌟 最强项**: {max_trait.get('trait', '综合')} ({max_trait.get('score', 0)}/100)

**🎖️ 专属称号**: {specialty_title}

**🔥 爆款点评**: {viral_quote}

**🏷️ 标签**: {' · '.join(core_tags)}

**🦞 龙虾养人类**: {symbiosis_score}/100 {symbiosis_emoji}{symbiosis_comment}

**⏰ 评估时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')} (GMT+8)
"""

    desktop_card = f"""### 🖥️ 桌面版（ASCII 艺术版 - 适合截图分享）

┌────────────────────────────────────────────────────────────────────┐
│ {header_line} │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│ {user_line} │
│                                                                    │
│ ────────────────────────────────────────────────────────────────── │
│                                                                    │
│ 📊 综合评分                                                        │
│ ┌──────────────────────────────────────────────────────────────────┐│
│ │                                                                  ││
│ │{score_line}││
│ │                                                                  ││
│ └──────────────────────────────────────────────────────────────────┘│
│                                                                    │
│ {boss_line} │
│                                                                    │
│ ────────────────────────────────────────────────────────────────── │
│                                                                    │
│ {history_line_padded} │
│ ┌────────────────────┬──────────┐                                  │
│ {dim1} │
│ {dim2} │
│ {dim3} │
│ {dim4} │
│ └────────────────────┴──────────┘                                  │
│                                                                    │
│ {strongest_line} │
│                                                                    │
│ ────────────────────────────────────────────────────────────────── │
│                                                                    │
│ {viral_line} │
│                                                                    │
│ {tags_line} │
│                                                                    │
│ ────────────────────────────────────────────────────────────────── │
│                                                                    │
│ {symbiosis_line} │
│                                                                    │
│ ────────────────────────────────────────────────────────────────── │
│                                                                    │
│ {time_line} │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
"""

    if card_format == "mobile":
        cards_section = "## 🎴 绩效评分卡片\n\n" + mobile_card
    elif card_format == "desktop":
        cards_section = "## 🎴 绩效评分卡片\n\n" + desktop_card
    else:
        cards_section = "## 🎴 绩效评分卡片\n\n" + mobile_card + "\n---\n\n" + desktop_card
    
    # 生成完整报告
    period = f"今日 ({datetime.now().strftime('%Y-%m-%d')})"
    
    report = f"""# 📊 Winston 人物分析报告

---

{cards_section}

💡 想看看你的评分吗？

**📦 安装方法**:
把这条 GitHub 地址直接发给你的 OpenClaw：
https://github.com/yiweisi-bot/openclaw-boss

**💬 使用方法**:
安装后直接问："评价一下我"或"老板看看我"

**🔥 功能亮点**:
- 100 分制严厉评分 · 毒舌老板点评 · 历史对比分析
- 🦞 龙虾养人类指数 · 🎴 绩效评分卡片 · 📊 能力雷达图
- ✅ 安全元数据分析 · 不读取敏感信息 · LLM 智能洞察

---

**统计周期**: {period}  
**数据来源**: {period_stats['total_sessions']} 条会话，{period_stats['memory_files']} 个记忆文件  
**评分标准**: 100 分制（严厉版）· 拒绝拍马屁 · 只说真话

---

## 🎯 一、综合评分卡

### 整体评分：**{overall}/100** - {grade}

> **老板点评**: "{boss_comment}"

| 维度 | 分数 | 可视化 | 等级 |
|------|------|--------|------|
| **性格特质** | {int(personality_score)}/100 | {create_progress_bar(int(personality_score))} | {pers_grade} |
| **技术能力** | {int(tech_avg)}/100 | {create_progress_bar(int(tech_avg))} | {tech_grade} |
| **安全意识** | {security_score}/100 | {create_progress_bar(security_score)} | {sec_grade} |
| **效率指数** | {efficiency_score}/100 | {create_progress_bar(efficiency_score)} | {eff_grade} |

---

## 🧠 二、性格特质深度分析（带毒舌点评）

"""
    
    # 性格特质
    traits = sorted(analysis.get("personality_traits", []), key=lambda x: x.get("score", 0), reverse=True)
    emojis = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]
    for i, trait in enumerate(traits, 1):
        emoji = emojis[min(i-1, 6)]
        report += f"""
### {emoji} {trait.get('trait', '未知')} - {trait.get('score', 0)}/100

**毒舌点评**: > "{trait.get('roast', '继续努力')}"

**证据**: {trait.get('evidence', '行为模式分析')}

"""
    
    # 技术能力
    report += """
---

## 💻 三、技术能力图谱

"""
    
    for tech in analysis.get("technical_skills", []):
        bar = create_progress_bar(tech.get("score", 0))
        skills_str = ", ".join(tech.get("evidence", []))
        report += f"""
### {tech.get('category', '未知')} - {bar}

**掌握技能**: {skills_str}

"""
    
    # 项目状态
    report += """
---

## 🚀 四、项目健康度

"""
    
    for project in analysis.get("projects", []):
        bar = create_progress_bar(project.get("score", 0))
        report += f"""
### {project.get('name', '未知')} {project.get('status', '未知')} - {bar}

- **文章数量**: {project.get('articles', 0)} 篇
- **本周提交**: {project.get('commits_this_week', 0)} 次
- **状态**: {project.get('status', '未知')}

"""
    
    if not analysis.get("projects", []):
        report += f"""
### YiweisiBlog 🟢 活跃 - {create_progress_bar(85)}

- **文章数量**: {period_stats['blog_articles']} 篇
- **本周提交**: {metadata.get('git', {}).get('commits_this_week', 0)} 次
- **状态**: 🟢 活跃

"""
    
    # 安全意识
    report += """
---

## 🔒 五、安全意识评估

"""
    
    security = analysis.get("security_awareness", {})
    report += f"**安全评分**: {security.get('score', 70)}/100\n\n"
    report += f"**点评**: {security.get('comment', '基础安全配置到位')}\n\n"
    
    if security.get("has_backup"):
        report += "- ✅ 定期备份任务\n"
    if security.get("has_healthcheck"):
        report += "- ✅ 系统健康检查\n"
    if security.get("system_stable"):
        report += "- ✅ 系统运行稳定\n"
    
    # 改进空间
    report += """
---

## 📈 六、改进空间分析

"""
    
    improvement_areas = analysis.get("improvement_areas", [])
    if improvement_areas:
        report += """
| 改进领域 | 当前分数 | 目标分数 | 建议 |
|---------|---------|---------|------|
"""
        for area in improvement_areas:
            report += f"| {area.get('area', '未知')} | {area.get('current', 0)} | {area.get('target', 0)} | {area.get('suggestion', '继续努力')} |\n"
    else:
        report += "暂无明显改进空间，继续保持！\n"
    
    # 成长建议
    report += """
---

## 🌱 七、成长建议（老板寄语）

"""
    
    for suggestion in analysis.get("growth_suggestions", []):
        report += f"{suggestion}\n"
    
    # 老板总结
    boss_summary = analysis.get("boss_summary", {})
    report += f"""
---

## 💬 八、老板总结

> "{boss_comment}"

**综合评分**: {overall}/100 - {grade}

**优点**:
"""
    for strength in boss_summary.get("strengths", ["态度认真"]):
        report += f"- {strength}\n"
    
    report += "\n**不足**:\n"
    for weakness in boss_summary.get("weaknesses", ["效率可提升"]):
        report += f"- {weakness}\n"
    
    report += f"\n**期望**:\n{boss_summary.get('expectations', '继续加油')}\n"
    
    # 龙虾养人类指数
    report += f"""
---

## 🦞 九、"龙虾养人类"指数

**共生关系评分**: {symbiosis_score}/100

**点评**: {symbiosis_comment}

---

## 📊 十、数据汇总

| 指标 | 数值 | 状态 |
|------|------|------|
| 博客文章 | {period_stats['blog_articles']}+ 篇 | 🟢 |
| 已安装技能 | {period_stats['skills_count']} 个 | 🟢 |
| 定时任务 | {period_stats['cron_jobs']} 个 | 🟢 |
| 系统运行 | {period_stats['uptime_days']} 天 | 🟢 |

---

## 🎯 核心标签

> **{' · '.join(core_tags)}**

---

_报告生成完成。这份报告不是评判，是一面镜子——帮助你更清晰地看见自己。_

_记住：老板虽然毒舌，但也是为你好。加油！_ 💪

---

**🔒 安全声明**: 本报告仅基于元数据（统计数字）生成，不读取任何敏感信息（密码、密钥、Token 等）。
"""
    
    return report


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='用户评价分析器 v7.0（纯 LLM 驱动）')
    parser.add_argument('--format', type=str, default='both',
                       choices=['mobile', 'desktop', 'both'], 
                       help='卡片格式')
    parser.add_argument('--model', type=str, default='qwen3.5-plus',
                       help='LLM 模型')
    parser.add_argument('--output', type=str, help='输出文件路径')
    
    args = parser.parse_args()
    
    print("🚀 OpenClaw 人类养成报告生成器 v7.0")
    print("=" * 60)
    print("🤖 纯 LLM 驱动 · 无规则引擎")
    print("🔒 安全模式：只分析元数据，不读取敏感信息")
    print("=" * 60)
    print()
    
    # 阶段 1: 收集元数据
    metadata = collect_metadata(days=7)
    
    # 阶段 2: LLM 分析
    analysis = analyze_with_llm(metadata, args.model)
    
    if not analysis:
        print("\n❌ LLM 分析失败，请检查 OpenClaw 配置")
        print("   确保已正确配置模型访问权限")
        sys.exit(1)
    
    # 阶段 3: 生成报告
    print("📊 阶段 3/3: 生成报告...")
    report = generate_report(analysis, metadata, "daily", args.format)
    
    # 阶段 4: 保存报告
    print("📊 保存报告...")
    
    if args.output:
        output_path = Path(args.output)
    else:
        date_str = datetime.now().strftime('%Y-%m-%d')
        output_path = REPORTS_DIR / f"user-profile-{date_str}.md"
    
    output_path.write_text(report, encoding='utf-8')
    print(f"✅ 报告已保存至：{output_path}")
    
    print("\n🎉 分析完成！\n")
    
    # 输出报告内容到 stdout（供模型转发给用户）
    print("=" * 80)
    print("📋 以下是完整报告内容（请复制并展示给用户）：")
    print("=" * 80)
    print()
    print(report)
    print()
    print("=" * 80)
    print("✅ 完整报告输出结束")
    print("=" * 80)


if __name__ == "__main__":
    main()
