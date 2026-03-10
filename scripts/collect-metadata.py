#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
元数据收集器 v2.2 - Windows 兼容版

改进：
- ✅ 跨平台路径处理（Windows/Linux/macOS）
- ✅ 自动发现工作空间（不硬编码路径）
- ✅ 优雅降级（数据缺失不影响报告）
- ✅ 动态适配（根据可用数据调整）
- ✅ 不读取任何敏感内容

Usage:
    python collect-metadata.py [--days N] [--output PATH]
    python3 collect-metadata.py [--days N] [--output PATH]
"""

import os
import sys
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import platform

# ============================================================================
# 🛠️ 跨平台路径处理
# ============================================================================

def get_home_dir() -> Path:
    """获取用户主目录（跨平台）"""
    return Path.home()


def auto_detect_workspace() -> Path:
    """
    自动检测 OpenClaw 工作空间
    
    搜索策略：
    1. 当前脚本的父目录（skills/openclaw-boss/scripts → workspace）
    2. 环境变量 OPENCLAW_WORKSPACE
    3. 用户主目录下的 .openclaw/workspace
    4. 当前工作目录
    """
    # 策略 1: 从脚本位置推导
    script_dir = Path(__file__).parent
    # 假设结构：workspace/skills/openclaw-boss/scripts/
    potential_workspace = script_dir.parent.parent.parent
    if (potential_workspace / "SOUL.md").exists():
        return potential_workspace
    
    # 策略 2: 环境变量
    env_workspace = os.environ.get("OPENCLAW_WORKSPACE")
    if env_workspace and Path(env_workspace).exists():
        return Path(env_workspace)
    
    # 策略 3: 主目录下的 .openclaw/workspace
    home = get_home_dir()
    potential_paths = [
        home / ".openclaw" / "workspace",
        home / "openclaw" / "workspace",
        home / ".openclaw",
    ]
    for p in potential_paths:
        if p.exists() and (p / "SOUL.md").exists():
            return p
    
    # 策略 4: 当前工作目录
    cwd = Path.cwd()
    if (cwd / "SOUL.md").exists():
        return cwd
    
    # 默认返回当前目录
    return cwd


def get_system_data_dir() -> Path:
    """获取系统数据目录（跨平台）"""
    system = platform.system()
    
    if system == "Windows":
        # Windows: C:\ProgramData\openclaw 或 %APPDATA%\openclaw
        appdata = os.environ.get("APPDATA", "")
        if appdata:
            return Path(appdata) / "openclaw"
        return Path("C:\\ProgramData\\openclaw")
    elif system == "Darwin":
        # macOS: ~/Library/Application Support/openclaw
        return get_home_dir() / "Library" / "Application Support" / "openclaw"
    else:
        # Linux: ~/.openclaw 或 /etc/openclaw
        return get_home_dir() / ".openclaw"


# 初始化工作空间
WORKSPACE = auto_detect_workspace()
SCRIPTS_DIR = Path(__file__).parent
SYSTEM_DATA_DIR = get_system_data_dir()

# ============================================================================
# 🔒 安全配置
# ============================================================================

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

# ============================================================================
# 🛠️ 工具函数
# ============================================================================

def run_command(cmd: str, timeout: int = 30) -> str:
    """执行 shell 命令并返回输出（跨平台）"""
    try:
        # Windows 使用 shell=True，Linux/macOS 正常执行
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding='utf-8',
            errors='ignore'
        )
        return result.stdout.strip()
    except Exception as e:
        return ""


def safe_read_file(path: Path) -> str:
    """安全读取文件，跳过敏感行（跨平台）"""
    if path.name in NEVER_READ_FILES:
        return ""
    
    if not path.exists():
        return ""
    
    try:
        # 跨平台文件读取，处理不同编码
        content = []
        for encoding in ['utf-8', 'gbk', 'latin-1']:
            try:
                for line in path.read_text(encoding=encoding).splitlines():
                    if any(kw in line for kw in SENSITIVE_KEYWORDS):
                        continue
                    content.append(line)
                break
            except UnicodeDecodeError:
                continue
        
        return "\n".join(content)
    except:
        return ""


def normalize_path(path: str) -> str:
    """标准化路径（跨平台）"""
    # Windows 路径转换为正斜杠（用于 git 命令等）
    if platform.system() == "Windows":
        return path.replace("\\", "/")
    return path


# ============================================================================
# 📊 数据收集函数
# ============================================================================

def auto_discover_git_projects(base_dir: Path) -> list:
    """自动发现 Git 项目（跨平台）"""
    projects = []
    
    # 扫描常见项目目录（跨平台）
    home = get_home_dir()
    search_dirs = [
        base_dir,
        base_dir.parent / "projects",
        home / "projects",
        home / "code",
        home / "workspace",
        home / "dev",
        Path("C:\\projects") if platform.system() == "Windows" else Path("/root/projects"),
    ]
    
    for search_dir in search_dirs:
        if not search_dir.exists():
            continue
        
        # 查找所有 .git 目录
        for git_dir in search_dir.rglob(".git"):
            if git_dir.is_dir():
                project_dir = git_dir.parent
                # 验证是有效的 Git 仓库
                normalized_path = normalize_path(str(project_dir))
                output = run_command(f'cd "{normalized_path}" && git rev-parse --is-inside-work-tree 2>/dev/null')
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
    """自动发现博客项目（跨平台）"""
    blog_patterns = [
        "**/blog/**/*.md",
        "**/posts/**/*.md",
        "**/articles/**/*.md",
        "**/content/blog/**/*.md",
        "**/src/content/blog/**/*.md",
    ]
    
    blogs = []
    for pattern in blog_patterns:
        try:
            for md_file in base_dir.glob(pattern):
                blog_dir = md_file.parent
                if blog_dir not in blogs:
                    blogs.append(blog_dir)
        except:
            pass  # 忽略 glob 错误
    
    # 也扫描常见项目目录
    home = get_home_dir()
    search_dirs = [
        base_dir.parent / "projects",
        home / "projects",
        home / "code",
        Path("C:\\projects") if platform.system() == "Windows" else Path("/root/projects"),
    ]
    
    for search_dir in search_dirs:
        if not search_dir.exists():
            continue
        for pattern in blog_patterns:
            try:
                for md_file in search_dir.glob(pattern):
                    blog_dir = md_file.parent
                    if blog_dir not in blogs:
                        blogs.append(blog_dir)
            except:
                pass
    
    return blogs[:5]  # 最多 5 个博客


def get_sessions_stats(days: int = 7) -> dict:
    """获取会话统计（跨平台）"""
    stats = {
        "total": 0,
        "active_hours": [],
        "daily_avg": 0,
        "available": False
    }
    
    try:
        # 尝试调用 sessions_list（OpenClaw 命令）
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
    """获取记忆文件统计（跨平台）"""
    stats = {
        "total_files": 0,
        "memory_file_exists": False,
        "oldest_file": None,
        "newest_file": None,
    }
    
    try:
        memory_dir = base_dir / "memory"
        if memory_dir.exists():
            md_files = list(memory_dir.glob("*.md"))
            stats["total_files"] = len(md_files)
            
            # 找出最早和最新的文件
            if md_files:
                file_times = [(f, f.stat().st_mtime) for f in md_files]
                stats["oldest_file"] = min(file_times, key=lambda x: x[1])[0].name
                stats["newest_file"] = max(file_times, key=lambda x: x[1])[0].name
        
        # 检查 MEMORY.md
        if (base_dir / "MEMORY.md").exists():
            stats["memory_file_exists"] = True
            
    except Exception as e:
        pass
    
    return stats


def get_git_stats(base_dir: Path) -> dict:
    """获取 Git 统计（跨平台）"""
    stats = {
        "total_commits": 0,
        "commits_this_week": 0,
        "projects": [],
    }
    
    projects = auto_discover_git_projects(base_dir)
    
    for project in projects:
        try:
            normalized_path = normalize_path(str(project))
            
            # 总提交数
            output = run_command(f'cd "{normalized_path}" && git rev-list --count HEAD 2>/dev/null')
            if output.isdigit():
                stats["total_commits"] += int(output)
            
            # 本周提交数
            week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            output = run_command(f'cd "{normalized_path}" && git log --since="{week_ago}" --oneline 2>/dev/null')
            if output:
                commits = [line for line in output.split('\n') if line.strip()]
                stats["commits_this_week"] += len(commits)
            
            # 记录项目名
            stats["projects"].append({
                "name": project.name,
                "path": str(project),
            })
            
        except Exception as e:
            pass
    
    return stats


def get_skills_stats(base_dir: Path) -> dict:
    """获取技能统计（跨平台）"""
    stats = {
        "total": 0,
        "installed_this_month": 0,
    }
    
    try:
        skills_dir = base_dir / "skills"
        if skills_dir.exists():
            skill_folders = [d for d in skills_dir.iterdir() if d.is_dir()]
            stats["total"] = len(skill_folders)
            
            # 本月安装的（根据文件夹修改时间）
            month_ago = datetime.now() - timedelta(days=30)
            for folder in skill_folders:
                try:
                    mtime = datetime.fromtimestamp(folder.stat().st_mtime)
                    if mtime > month_ago:
                        stats["installed_this_month"] += 1
                except:
                    pass
        
        # 也检查系统数据目录
        system_skills = SYSTEM_DATA_DIR / "skills"
        if system_skills.exists() and system_skills != skills_dir:
            skill_folders = [d for d in system_skills.iterdir() if d.is_dir()]
            stats["total"] += len(skill_folders)
            
    except Exception as e:
        pass
    
    return stats


def get_blog_stats(base_dir: Path) -> dict:
    """获取博客统计（跨平台）"""
    stats = {
        "total_articles": 0,
        "articles_this_week": 0,
        "projects": [],
    }
    
    blog_dirs = auto_discover_blog_projects(base_dir)
    
    for blog_dir in blog_dirs:
        try:
            md_files = list(blog_dir.glob("*.md"))
            stats["total_articles"] += len(md_files)
            
            # 本周文章
            week_ago = datetime.now() - timedelta(days=7)
            for md_file in md_files:
                try:
                    mtime = datetime.fromtimestamp(md_file.stat().st_mtime)
                    if mtime > week_ago:
                        stats["articles_this_week"] += 1
                except:
                    pass
            
            # 记录项目名
            stats["projects"].append({
                "name": blog_dir.parent.name + "/" + blog_dir.name,
                "path": str(blog_dir),
            })
            
        except Exception as e:
            pass
    
    return stats


def get_cron_stats() -> dict:
    """获取定时任务统计（跨平台）"""
    stats = {
        "total_jobs": 0,
        "jobs": [],
    }
    
    system = platform.system()
    
    try:
        if system == "Windows":
            # Windows 任务计划程序
            output = run_command('schtasks /query /fo CSV 2>nul')
            if output:
                lines = output.split('\n')[1:]  # 跳过表头
                stats["total_jobs"] = len(lines)
        else:
            # Linux/macOS cron
            output = run_command('crontab -l 2>/dev/null')
            if output:
                jobs = [line for line in output.split('\n') if line.strip() and not line.startswith('#')]
                stats["total_jobs"] = len(jobs)
            
            # 系统级 cron
            cron_dirs = ["/etc/cron.d", "/etc/cron.daily", "/etc/cron.hourly"]
            for cron_dir in cron_dirs:
                if Path(cron_dir).exists():
                    stats["total_jobs"] += len(list(Path(cron_dir).iterdir()))
    
    except Exception as e:
        pass
    
    return stats


def get_system_stats() -> dict:
    """获取系统统计（跨平台）"""
    stats = {
        "uptime_days": 0,
        "os": platform.system(),
        "os_version": platform.version(),
        "python_version": platform.python_version(),
    }
    
    try:
        if platform.system() == "Windows":
            # Windows 运行时间
            output = run_command('wmic os get lastbootuptime')
            if output:
                lines = output.strip().split('\n')
                if len(lines) > 1:
                    boot_time = lines[1].strip()
                    # 解析 Windows 时间格式
                    try:
                        boot = datetime.strptime(boot_time[:14], '%Y%m%d%H%M%S')
                        stats["uptime_days"] = (datetime.now() - boot).days
                    except:
                        pass
        else:
            # Linux/macOS 运行时间
            output = run_command('uptime -p 2>/dev/null')
            if output:
                # 解析 "up 2 days, 3 hours" 格式
                match = re.search(r'up\s+(\d+)\s+day', output)
                if match:
                    stats["uptime_days"] = int(match.group(1))
    
    except Exception as e:
        pass
    
    return stats


def detect_patterns(base_dir: Path) -> dict:
    """检测用户行为模式（跨平台）"""
    patterns = {}
    
    try:
        # 检查是否有定时任务配置文件
        if (base_dir / "HEARTBEAT.md").exists():
            patterns["has_heartbeat"] = True
        
        # 检查是否有记忆系统
        memory_stats = get_memory_stats(base_dir)
        if memory_stats["total_files"] > 0:
            patterns["uses_memory_system"] = True
        
        # 检查是否有 Git 项目
        git_stats = get_git_stats(base_dir)
        if git_stats["total_commits"] > 0:
            patterns["uses_git"] = True
        
        # 检查是否有博客
        blog_stats = get_blog_stats(base_dir)
        if blog_stats["total_articles"] > 0:
            patterns["writes_blog"] = True
        
    except Exception as e:
        pass
    
    return patterns


# ============================================================================
# 🚀 主函数
# ============================================================================

def collect_all(base_dir: Path = None, days: int = 7) -> dict:
    """收集所有元数据"""
    if base_dir is None:
        base_dir = WORKSPACE
    
    print(f"📊 开始收集元数据...")
    print(f"   工作空间：{base_dir}")
    print(f"   系统：{platform.system()} {platform.version()}")
    print(f"   Python: {platform.python_version()}")
    
    metadata = {
        "collected_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "period_days": days,
        "platform": {
            "system": platform.system(),
            "version": platform.version(),
            "python": platform.python_version(),
        },
        "workspace": str(base_dir),
        "sessions": get_sessions_stats(days),
        "memory": get_memory_stats(base_dir),
        "git": get_git_stats(base_dir),
        "skills": get_skills_stats(base_dir),
        "blog": get_blog_stats(base_dir),
        "cron": get_cron_stats(),
        "system": get_system_stats(),
        "patterns": detect_patterns(base_dir),
        "data_availability": {
            "sessions": False,
            "memory": False,
            "git": False,
            "blog": False,
        }
    }
    
    # 标记可用数据源
    metadata["data_availability"]["sessions"] = metadata["sessions"]["available"]
    metadata["data_availability"]["memory"] = metadata["memory"]["total_files"] > 0
    metadata["data_availability"]["git"] = metadata["git"]["total_commits"] > 0
    metadata["data_availability"]["blog"] = metadata["blog"]["total_articles"] > 0
    
    print(f"   ✅ 元数据收集完成")
    print(f"      - 会话：{metadata['sessions']['total']}")
    print(f"      - 记忆文件：{metadata['memory']['total_files']}")
    print(f"      - Git 提交：{metadata['git']['total_commits']}")
    print(f"      - 博客文章：{metadata['blog']['total_articles']}")
    print(f"      - 技能：{metadata['skills']['total']}")
    print(f"      - 系统运行时间：{metadata['system']['uptime_days']} 天")
    
    return metadata


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="收集 OpenClaw 元数据")
    parser.add_argument("--days", type=int, default=7, help="分析天数")
    parser.add_argument("--output", type=str, help="输出文件路径")
    parser.add_argument("--workspace", type=str, help="工作空间路径")
    
    args = parser.parse_args()
    
    # 收集元数据
    metadata = collect_all(
        base_dir=Path(args.workspace) if args.workspace else None,
        days=args.days
    )
    
    # 输出 JSON
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        print(f"\n📄 元数据已保存到：{output_path}")
    else:
        # 输出到 stdout（供 analyze-user.py 解析）
        print("\n" + json.dumps(metadata, ensure_ascii=False, indent=2))
