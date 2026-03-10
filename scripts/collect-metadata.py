#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
元数据收集器 v2.1 - 通用安全版

通用化设计：
- ✅ 自动发现数据源（不硬编码路径）
- ✅ 优雅降级（数据缺失不影响报告）
- ✅ 动态适配（根据可用数据调整）
- ✅ 不读取任何敏感内容

Usage:
    python3 collect-metadata.py [--days N] [--output PATH]
"""

import os
import sys
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
import subprocess

# 配置
SCRIPTS_DIR = Path(__file__).parent
WORKSPACE = SCRIPTS_DIR.parent.parent.parent  # skills/openclaw-boss → workspace

# ⚠️ 敏感文件列表（完全不读取）
NEVER_READ_FILES = [
    "TOOLS.md", ".env", ".env.local", "config.json", "secrets.json",
]

# ⚠️ 敏感行关键词（读到也跳过）
SENSITIVE_KEYWORDS = [
    "密码", "授权码", "Token", "API Key", "Secret", "密钥",
    "验证问题", "验证答案", "IP 地址", "房间密码", "邮箱账号",
    "sk-", "ghp_", "glpat-", "LETRD",
]


def run_command(cmd: str, timeout: int = 30) -> str:
    """执行 shell 命令并返回输出"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=timeout
        )
        return result.stdout.strip()
    except Exception as e:
        return ""


def safe_read_file(path: Path) -> str:
    """安全读取文件，跳过敏感行"""
    if path.name in NEVER_READ_FILES:
        return ""
    
    if not path.exists():
        return ""
    
    try:
        content = []
        for line in path.read_text(encoding='utf-8').splitlines():
            if any(kw in line for kw in SENSITIVE_KEYWORDS):
                continue
            content.append(line)
        return "\n".join(content)
    except:
        return ""


def auto_discover_git_projects(base_dir: Path) -> list:
    """自动发现 Git 项目"""
    projects = []
    
    # 扫描常见项目目录
    search_dirs = [
        base_dir,
        base_dir.parent / "projects",
        Path.home() / "projects",
        Path("/root/projects"),
    ]
    
    for search_dir in search_dirs:
        if not search_dir.exists():
            continue
        
        # 查找所有 .git 目录
        for git_dir in search_dir.rglob(".git"):
            if git_dir.is_dir():
                project_dir = git_dir.parent
                # 验证是有效的 Git 仓库
                output = run_command(f"cd {project_dir} && git rev-parse --is-inside-work-tree 2>/dev/null")
                if "true" in output:
                    projects.append(project_dir)
    
    # 去重
    unique_projects = []
    seen = set()
    for p in projects:
        p_str = str(p.resolve())
        if p_str not in seen:
            seen.add(p_str)
            unique_projects.append(p)
    
    return unique_projects[:10]  # 最多 10 个项目


def auto_discover_blog_projects(base_dir: Path) -> list:
    """自动发现博客项目"""
    blog_patterns = [
        "**/blog/**/*.md",
        "**/posts/**/*.md",
        "**/articles/**/*.md",
        "**/content/blog/**/*.md",
        "**/src/content/blog/**/*.md",
    ]
    
    blogs = []
    for pattern in blog_patterns:
        for md_file in base_dir.glob(pattern):
            blog_dir = md_file.parent
            if blog_dir not in blogs:
                blogs.append(blog_dir)
    
    # 也扫描常见项目目录
    search_dirs = [
        base_dir.parent / "projects",
        Path.home() / "projects",
        Path("/root/projects"),
    ]
    
    for search_dir in search_dirs:
        if search_dir.exists():
            for pattern in blog_patterns:
                for md_file in search_dir.glob(pattern):
                    blog_dir = md_file.parent
                    if blog_dir not in blogs:
                        blogs.append(blog_dir)
    
    return blogs[:5]  # 最多 5 个博客


def get_sessions_stats(days: int = 7) -> dict:
    """获取会话统计（通用）"""
    stats = {
        "total": 0,
        "active_hours": [],
        "daily_avg": 0,
        "available": False
    }
    
    try:
        # 尝试调用 sessions_list
        output = run_command(f"sessions_list --limit 100 --messageLimit 1 2>/dev/null")
        if not output:
            return stats
        
        sessions = json.loads(output) if output.startswith('[') else []
        if not sessions:
            return stats
        
        stats["available"] = True
        stats["total"] = len(sessions)
        
        # 分析时间分布
        hours = []
        daily_counts = {}
        for s in sessions:
            created = s.get("createdAt", "")
            if created:
                try:
                    dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                    hours.append(dt.hour)
                    day_key = dt.strftime('%Y-%m-%d')
                    daily_counts[day_key] = daily_counts.get(day_key, 0) + 1
                except:
                    pass
        
        # 计算活跃时段
        hour_counts = {}
        for h in hours:
            hour_counts[h] = hour_counts.get(h, 0) + 1
        
        active_hours = sorted(hour_counts.keys(), key=lambda h: hour_counts.get(h, 0), reverse=True)[:5]
        stats["active_hours"] = active_hours
        stats["daily_avg"] = sum(daily_counts.values()) / max(1, len(daily_counts))
        
    except Exception as e:
        pass  # 优雅降级
    
    return stats


def get_memory_stats(base_dir: Path) -> dict:
    """获取记忆文件统计（通用）"""
    stats = {
        "total_files": 0,
        "memory_file_exists": False,
        "oldest_file": None,
        "newest_file": None,
        "total_size_kb": 0,
        "available": False
    }
    
    # 检查长期记忆文件
    memory_file = base_dir / "MEMORY.md"
    if memory_file.exists():
        stats["memory_file_exists"] = True
        stats["available"] = True
        stats["total_size_kb"] += memory_file.stat().st_size // 1024
    
    # 扫描记忆目录（尝试多个可能的目录名）
    memory_dirs = [
        base_dir / "memory",
        base_dir / "memories",
        base_dir / "logs",
        base_dir / "daily",
    ]
    
    for mem_dir in memory_dirs:
        if mem_dir.exists() and mem_dir.is_dir():
            files = sorted(mem_dir.glob("*.md"))
            if files:
                stats["total_files"] = len(files)
                stats["available"] = True
                stats["oldest_file"] = files[0].name
                stats["newest_file"] = files[-1].name
                stats["total_size_kb"] += sum(f.stat().st_size // 1024 for f in files)
                break  # 找到第一个就用
    
    return stats


def get_git_stats(base_dir: Path) -> dict:
    """获取 Git 提交统计（通用）"""
    stats = {
        "total_commits": 0,
        "commits_this_week": 0,
        "commits_this_month": 0,
        "repos": [],
        "available": False
    }
    
    # 自动发现 Git 项目
    projects = auto_discover_git_projects(base_dir)
    
    # 排除列表：不统计大型开源项目/fork 仓库
    EXCLUDE_PATTERNS = [
        "clawdbot",
        "moltbot",
        "node_modules",
        ".cache",
        "temp_git",
    ]
    
    for proj_dir in projects:
        try:
            # 跳过排除的项目
            if any(pattern in proj_dir.name.lower() for pattern in EXCLUDE_PATTERNS):
                continue
            
            # 总提交数（只统计活跃仓库：本周或本月有提交）
            week_commits = run_command(f"cd {proj_dir} && git log --since='1 week ago' --oneline 2>/dev/null | wc -l")
            month_commits = run_command(f"cd {proj_dir} && git log --since='1 month ago' --oneline 2>/dev/null | wc -l")
            
            week_count = int(week_commits) if week_commits and week_commits.isdigit() else 0
            month_count = int(month_commits) if month_commits and month_commits.isdigit() else 0
            
            # 只统计活跃仓库（本周或本月有提交）
            if week_count > 0 or month_count > 0:
                stats["commits_this_week"] += week_count
                stats["commits_this_month"] += month_count
                
                # 计算总提交（只算活跃仓库）
                total = run_command(f"cd {proj_dir} && git rev-list --count HEAD 2>/dev/null")
                if total and total.isdigit():
                    stats["total_commits"] += int(total)
                    stats["available"] = True
                
                stats["repos"].append(proj_dir.name)
        except:
            pass
    
    return stats


def get_skills_stats(base_dir: Path) -> dict:
    """获取已安装技能统计（通用）"""
    stats = {
        "total": 0,
        "skills": [],
        "installed_this_month": 0,
        "available": False
    }
    
    # 尝试多个可能的技能目录
    skills_dirs = [
        base_dir / "skills",
        base_dir.parent / "skills",
        Path("/root/.openclaw/skills"),
    ]
    
    for skills_dir in skills_dirs:
        if skills_dir.exists() and skills_dir.is_dir():
            skills = [d.name for d in skills_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
            if skills:
                stats["total"] = len(skills)
                stats["skills"] = skills[:20]  # 最多 20 个
                stats["available"] = True
                
                # 检查最近安装
                now = datetime.now()
                for skill_dir in skills_dir.iterdir():
                    if skill_dir.is_dir() and not skill_dir.name.startswith('.'):
                        try:
                            mtime = datetime.fromtimestamp(skill_dir.stat().st_mtime)
                            if (now - mtime).days <= 30:
                                stats["installed_this_month"] += 1
                        except:
                            pass
                break
    
    return stats


def get_blog_stats(base_dir: Path) -> dict:
    """获取博客统计（通用）"""
    stats = {
        "total_articles": 0,
        "articles_this_week": 0,
        "articles_this_month": 0,
        "last_publish": None,
        "available": False
    }
    
    # 自动发现博客项目
    blogs = auto_discover_blog_projects(base_dir)
    
    now = datetime.now()
    latest_mtime = None
    
    for blog_dir in blogs:
        if not blog_dir.exists():
            continue
        
        articles = list(blog_dir.glob("*.md"))
        stats["total_articles"] += len(articles)
        
        if articles:
            stats["available"] = True
        
        for article in articles:
            try:
                mtime = datetime.fromtimestamp(article.stat().st_mtime)
                if (now - mtime).days <= 7:
                    stats["articles_this_week"] += 1
                if (now - mtime).days <= 30:
                    stats["articles_this_month"] += 1
                if latest_mtime is None or mtime > latest_mtime:
                    latest_mtime = mtime
            except:
                pass
    
    if latest_mtime:
        stats["last_publish"] = latest_mtime.strftime('%Y-%m-%d')
    
    return stats


def get_cron_stats() -> dict:
    """获取定时任务统计（通用）"""
    stats = {
        "total_jobs": 0,
        "jobs": [],
        "available": False
    }
    
    try:
        output = run_command("crontab -l 2>/dev/null")
        if output:
            for line in output.splitlines():
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if any(kw in line for kw in SENSITIVE_KEYWORDS):
                    continue
                stats["total_jobs"] += 1
                stats["available"] = True
                
                # 简化描述
                if "heartbeat" in line.lower():
                    stats["jobs"].append("心跳任务")
                elif "backup" in line.lower():
                    stats["jobs"].append("备份任务")
                elif "sync" in line.lower():
                    stats["jobs"].append("同步任务")
                elif "check" in line.lower() or "scan" in line.lower():
                    stats["jobs"].append("检查任务")
                else:
                    stats["jobs"].append("定时任务")
    except:
        pass
    
    return stats


def get_system_stats() -> dict:
    """获取系统运行统计（通用）"""
    stats = {
        "uptime_days": 0,
        "python_version": "",
        "node_version": "",
        "os_info": ""
    }
    
    try:
        # 运行时间
        uptime_output = run_command("uptime -p 2>/dev/null")
        if uptime_output:
            match = re.search(r'(\d+) days?', uptime_output)
            if match:
                stats["uptime_days"] = int(match.group(1))
        
        # 版本信息
        stats["python_version"] = run_command("python3 --version 2>/dev/null").replace("Python ", "")
        stats["node_version"] = run_command("node --version 2>/dev/null").replace("v", "")
        stats["os_info"] = run_command("uname -s 2>/dev/null")
        
    except:
        pass
    
    return stats


def analyze_patterns(metadata: dict) -> dict:
    """基于元数据分析行为模式（通用）"""
    patterns = {}
    
    # 活跃时段分析
    active_hours = metadata.get("sessions", {}).get("active_hours", [])
    if active_hours:
        if any(h >= 23 or h <= 2 for h in active_hours):
            patterns["work_habit"] = "夜猫子"
        elif any(h >= 5 and h <= 7 for h in active_hours):
            patterns["work_habit"] = "早起鸟"
        else:
            patterns["work_habit"] = "正常作息"
    else:
        patterns["work_habit"] = "未知"
    
    # 工作强度分析
    daily_avg = metadata.get("sessions", {}).get("daily_avg", 0)
    if daily_avg >= 50:
        patterns["intensity"] = "高强度"
    elif daily_avg >= 20:
        patterns["intensity"] = "中等强度"
    else:
        patterns["intensity"] = "轻度使用"
    
    # 技能活跃度
    skills_month = metadata.get("skills", {}).get("installed_this_month", 0)
    if skills_month >= 3:
        patterns["learning"] = "积极探索"
    elif skills_month >= 1:
        patterns["learning"] = "稳定学习"
    else:
        patterns["learning"] = "保守使用"
    
    # 内容生产力
    blog_week = metadata.get("blog", {}).get("articles_this_week", 0)
    if blog_week >= 3:
        patterns["productivity"] = "高产"
    elif blog_week >= 1:
        patterns["productivity"] = "稳定输出"
    else:
        patterns["productivity"] = "偶尔创作"
    
    # Git 活跃度
    git_week = metadata.get("git", {}).get("commits_this_week", 0)
    if git_week >= 10:
        patterns["coding"] = "密集开发"
    elif git_week >= 5:
        patterns["coding"] = "活跃开发"
    elif git_week >= 1:
        patterns["coding"] = "偶尔提交"
    else:
        patterns["coding"] = "近期无提交"
    
    return patterns


def collect_all(base_dir: Path = None, days: int = 7) -> dict:
    """收集所有元数据（通用入口）"""
    if base_dir is None:
        base_dir = WORKSPACE
    
    print("📊 开始收集元数据...")
    print(f"   工作空间：{base_dir}")
    
    metadata = {
        "collected_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "period_days": days,
        "workspace": str(base_dir),
        "sessions": get_sessions_stats(days),
        "memory": get_memory_stats(base_dir),
        "git": get_git_stats(base_dir),
        "skills": get_skills_stats(base_dir),
        "blog": get_blog_stats(base_dir),
        "cron": get_cron_stats(),
        "system": get_system_stats(),
    }
    
    # 分析行为模式
    metadata["patterns"] = analyze_patterns(metadata)
    
    # 数据可用性总结
    metadata["data_availability"] = {
        "sessions": metadata["sessions"]["available"],
        "memory": metadata["memory"]["available"],
        "git": metadata["git"]["available"],
        "skills": metadata["skills"]["available"],
        "blog": metadata["blog"]["available"],
        "cron": metadata["cron"]["available"],
    }
    
    # 打印摘要
    print(f"   ✅ 会话：{metadata['sessions']['total']} 条 {'(可用)' if metadata['sessions']['available'] else '(不可用)'}")
    print(f"   ✅ 记忆：{metadata['memory']['total_files']} 个文件 {'(可用)' if metadata['memory']['available'] else '(不可用)'}")
    print(f"   ✅ Git: {metadata['git']['total_commits']} 次提交 {'(可用)' if metadata['git']['available'] else '(不可用)'}")
    print(f"   ✅ 技能：{metadata['skills']['total']} 个 {'(可用)' if metadata['skills']['available'] else '(不可用)'}")
    print(f"   ✅ 博客：{metadata['blog']['total_articles']} 篇 {'(可用)' if metadata['blog']['available'] else '(不可用)'}")
    print(f"   ✅ Cron: {metadata['cron']['total_jobs']} 个任务 {'(可用)' if metadata['cron']['available'] else '(不可用)'}")
    
    return metadata


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='元数据收集器 v2.1（通用安全版）')
    parser.add_argument('--days', type=int, default=7, help='统计最近 N 天')
    parser.add_argument('--output', type=str, help='输出 JSON 文件路径')
    parser.add_argument('--workspace', type=str, help='工作空间目录（可选）')
    
    args = parser.parse_args()
    
    base_dir = Path(args.workspace) if args.workspace else WORKSPACE
    
    metadata = collect_all(base_dir, args.days)
    
    # 输出 JSON
    json_output = json.dumps(metadata, indent=2, ensure_ascii=False)
    
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(json_output, encoding='utf-8')
        print(f"✅ 元数据已保存至：{output_path}")
    else:
        print("\n📋 元数据 JSON:")
        print(json_output)
    
    return metadata


if __name__ == "__main__":
    main()
