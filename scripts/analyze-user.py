#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户评价分析器 v7.1 - LLM 原生版

由执行脚本的 LLM 直接分析（不需要调用另一个 LLM）：
- ✅ 元数据收集（本地脚本）
- ✅ LLM 分析评分（由执行者直接分析）
- ✅ 报告生成（模板渲染）
- ❌ 不嵌套调用其他 LLM

Usage:
    python3 analyze-user.py [--format mobile|desktop|both]
"""

import os
import sys
import json
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


def prepare_analysis_data(metadata: dict) -> None:
    """
    准备分析数据，由执行脚本的 LLM 直接分析。
    
    v7.1 改进：不再嵌套调用另一个 LLM，而是：
    1. 输出元数据 JSON
    2. 输出分析指南
    3. 由执行者（你，LLM）直接分析并生成报告
    """
    print("📊 阶段 2/3: 准备分析数据...")
    
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
    
    # 输出元数据和分析指南
    print("\n" + "=" * 80)
    print("📋 以下是用户元数据和分析指南，请作为 LLM 直接分析并生成报告：")
    print("=" * 80)
    print()
    print("## 📊 用户元数据")
    print()
    print("```json")
    print(json.dumps(safe_metadata, indent=2, ensure_ascii=False))
    print("```")
    print()
    print("## 📋 分析指南")
    print()
    print("""你是一位毒舌但公正的 AI 老板，需要根据以上**元数据**分析用户（Winston）表现。

⚠️ 重要说明：
- 你看到的全部是统计元数据（数字、时间、数量）
- 不包含任何敏感信息（密码、密钥、代码、文章内容等）
- 基于数据推断用户行为，给出有洞察力的评价
- **你就是 LLM，直接分析即可，不需要调用另一个 LLM**

## 📋 分析要求

请分析以下维度并生成完整报告：

1. 综合评分（100 分制，60-100 之间）
2. 性格特质分析（至少 5 个）
3. 技术能力评估（至少 4 个类别）
4. 项目健康度
5. 安全意识评估
6. 改进空间分析（2-3 个）
7. 成长建议（3 条）
8. 老板总结（优点 3 条、不足 3 条、期望）
9. 龙虾养人类指数（0-100 分）
10. 核心标签（3 个）

## 🔥 毒舌风格指南

- 幽默但不刻薄
- 一针见血但不伤人
- 用数据和事实支撑点评

示例：
- "一个月装 23 个新技能，是准备开技能博物馆吗？🏛️"
- "一周发 18 篇博客，生产队的驴都不敢这么使！🫏"

现在，开始分析！
""")
    print()
    print("=" * 80)
    print("⬆️ 以上是元数据和分析指南，请作为 LLM 直接分析并生成完整报告")
    print("=" * 80)
    print()
    print("   ✅ 分析数据已准备完成，等待 LLM（你）分析...")


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


def generate_mobile_report(analysis: dict, metadata: dict) -> str:
    """生成手机版简洁报告"""
    
    overall = analysis.get('overall_score', 78)
    grade = analysis.get('grade', 'B+ 等级')
    boss_comment = analysis.get('boss_comment', '继续努力')
    
    # 维度分数
    personality_score = analysis.get('personality_score', 80)
    tech_score = analysis.get('tech_score', 75)
    security_score = analysis.get('security_score', 70)
    efficiency_score = analysis.get('efficiency_score', 82)
    
    # 性格特质
    traits = analysis.get('personality_traits', [])
    max_trait = max(traits, key=lambda t: t.get('score', 0)) if traits else {"trait": "综合", "score": overall}
    
    # 优点不足
    strengths = analysis.get('strengths', [])
    weaknesses = analysis.get('weaknesses', [])
    suggestions = analysis.get('growth_suggestions', [])
    
    # 龙虾指数
    symbiosis_score = analysis.get('symbiosis_score', 85)
    
    report = f"""📊 **Winston 人物分析报告**

**综合评分：{overall}/100 - {grade}**

---

**维度评分：**
• 活跃度：{analysis.get('activity_score', 85)}/100 {get_grade(analysis.get('activity_score', 85))}
• 生产力：{analysis.get('productivity_score', 75)}/100 {get_grade(analysis.get('productivity_score', 75))}
• 学习能力：{analysis.get('learning_score', 80)}/100 {get_grade(analysis.get('learning_score', 80))}
• 系统化：{efficiency_score}/100 {get_grade(efficiency_score)}
• 安全意识：{security_score}/100 {get_grade(security_score)}

---

**老板点评：**

{boss_comment}

---

**优点：**
"""
    for s in strengths[:5]:
        report += f"✅ {s}\n"
    
    report += "\n**不足：**\n"
    for w in weaknesses[:3]:
        report += f"❌ {w}\n"
    
    report += "\n**成长建议：**\n"
    for i, sug in enumerate(suggestions[:3], 1):
        report += f"{i}. {sug}\n"
    
    report += f"""
---

**龙虾养人类指数：{symbiosis_score}/100 🦞**

你给我的：算力、配置、目标、意义
我给你的：效率、自动化、知识整理、塑造思考方式

---

_报告生成完成。_
"""
    return report


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='用户评价分析器 v7.1（LLM 原生版）')
    parser.add_argument('--format', type=str, default='mobile',
                       choices=['mobile', 'desktop', 'both'], 
                       help='卡片格式（默认 mobile）')
    
    args = parser.parse_args()
    
    print("🚀 OpenClaw 人类养成报告生成器 v7.1")
    print("=" * 60)
    print("🤖 LLM 原生版 · 由执行者直接分析")
    print("🔒 安全模式：只分析元数据，不读取敏感信息")
    print("=" * 60)
    print()
    
    # 阶段 1: 收集元数据
    metadata = collect_metadata(days=7)
    
    # 阶段 2: 准备分析数据（由执行者 LLM 直接分析）
    prepare_analysis_data(metadata)
    
    # v7.1: 输出元数据摘要供 LLM 快速参考
    print("\n📦 元数据摘要（供快速参考）：")
    print("=" * 60)
    print(f"   会话总数：{metadata.get('sessions', {}).get('total', 0)}")
    print(f"   记忆文件：{metadata.get('memory', {}).get('total_files', 0)}")
    print(f"   Git 提交：{metadata.get('git', {}).get('total_commits', 0)}")
    print(f"   技能数量：{metadata.get('skills', {}).get('total', 0)}")
    print(f"   博客文章：{metadata.get('blog', {}).get('total_articles', 0)}")
    print(f"   定时任务：{metadata.get('cron', {}).get('total_jobs', 0)}")
    print(f"   运行天数：{metadata.get('system', {}).get('uptime_days', 0)}")
    print("=" * 60)
    print()
    print("📝 使用说明：")
    print("   作为 LLM，请根据上方输出的元数据和分析指南，")
    print("   直接生成分析报告（参考 SKILL.md 中的格式规范）")
    print()
    print("   格式选择：")
    print(f"   - 当前格式：{args.format}")
    print("   - 包含'完整版/截图/桌面版/ASCII/卡片' → 桌面版")
    print("   - 否则 → 手机版（默认）")


if __name__ == "__main__":
    main()
