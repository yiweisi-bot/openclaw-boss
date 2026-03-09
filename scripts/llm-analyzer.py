#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM 分析器 v3.0 - 真正调用大模型

使用 OpenClaw 内置的模型调用能力，分析元数据并生成报告。

Usage:
    python3 llm-analyzer.py --metadata JSON_PATH [--model MODEL] [--output PATH]
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
import subprocess


def build_prompt(metadata: dict) -> str:
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

### 1. 综合评分（100 分制）
基于元数据给出整体评分（60-100 分之间）

### 2. 性格特质分析（至少 5 个）
从元数据推断性格特质，每个特质需要：
- 特质名称
- 分数（0-100）
- 毒舌点评（幽默但一针见血，20-40 字）
- 数据依据（引用元数据中的具体数字）

### 3. 技术能力评估（至少 4 个类别）
根据技能列表推断技术能力

### 4. 项目健康度
根据博客和 Git 数据评估

### 5. 安全意识评估
基于定时任务等推断

### 6. 改进空间分析（2-3 个）

### 7. 成长建议（3 条）

### 8. 老板总结
优点（3 条）、不足（3 条）、期望

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
  "history_comparison": {{
    "has_previous": false,
    "comment": "首次评估"
  }},
  "viral_quote": "爆款金句",
  "core_tags": ["标签 1", "标签 2", "标签 3"]
}}
```

## 🔥 毒舌风格指南

- 幽默但不刻薄
- 一针见血但不伤人
- 用数据和事实支撑点评

示例：
- "夜猫子？凌晨 2 点还在会话，是准备和月亮交朋友吗？🌙"
- "一周发 3 篇博客，生产队的驴都不敢这么使！🫏"
- "定时任务配置得比闹钟还多，是准备 AI 军训吗？🎖️"

现在，开始分析！
"""


def call_llm_via_openclaw(prompt: str, model: str = "doubao/ark-code-latest") -> str:
    """通过 OpenClaw 调用 LLM"""
    
    print(f"   🤖 调用大模型（{model}）...")
    
    # 方法：使用 sessions_spawn 创建一个临时会话来分析
    # 但由于这是在脚本内部，我们使用一个更简单的方法
    
    # 检查是否有 OpenClaw 命令可用
    try:
        # 尝试使用 openclaw 命令调用模型
        # 注意：这需要根据实际 OpenClaw 版本调整
        
        # 方法 1: 使用 openclaw ask（如果可用）
        cmd = f'openclaw ask --model {model} --no-history "{prompt}" 2>/dev/null'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0 and result.stdout.strip():
            print("   ✅ 大模型分析完成")
            return result.stdout.strip()
        
        # 方法 2: 如果 openclaw 命令不可用，尝试直接 API 调用
        api_key = os.environ.get('LLM_API_KEY', '')
        if api_key:
            # 这里可以添加直接 API 调用代码
            pass
        
        print("   ⚠️  OpenClaw 命令不可用或未配置")
        return None
        
    except subprocess.TimeoutExpired:
        print("   ⚠️  LLM 调用超时")
        return None
    except Exception as e:
        print(f"   ⚠️  LLM 调用失败：{e}")
        return None


def analyze_metadata(metadata_path: str, model: str = "doubao/ark-code-latest") -> dict:
    """分析元数据"""
    
    # 读取元数据
    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    # 准备发送给 LLM 的数据（只包含安全数据）
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
    prompt = build_prompt(safe_metadata)
    
    # 调用 LLM
    llm_response = call_llm_via_openclaw(prompt, model)
    
    if llm_response:
        try:
            # 解析 JSON
            if llm_response.startswith('```json'):
                llm_response = llm_response.replace('```json', '').replace('```', '').strip()
            
            analysis = json.loads(llm_response)
            return analysis
            
        except json.JSONDecodeError as e:
            print(f"   ⚠️  JSON 解析失败：{e}")
    
    # 如果 LLM 失败，返回 None（主脚本会用规则引擎备用）
    return None


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='LLM 分析器 v3.0')
    parser.add_argument('--metadata', type=str, required=True, help='元数据 JSON 文件路径')
    parser.add_argument('--model', type=str, default='doubao/ark-code-latest', help='LLM 模型')
    parser.add_argument('--output', type=str, help='输出分析结果 JSON 路径')
    
    args = parser.parse_args()
    
    print("🤖 开始 LLM 分析...")
    
    # 分析元数据
    analysis = analyze_metadata(args.metadata, args.model)
    
    if analysis:
        # 输出结果
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            print(f"✅ 分析结果已保存至：{args.output}")
        else:
            print("\n📋 分析结果:")
            print(json.dumps(analysis, indent=2, ensure_ascii=False))
    else:
        print("❌ LLM 分析失败，请检查配置")
        sys.exit(1)
    
    return analysis


if __name__ == "__main__":
    main()
