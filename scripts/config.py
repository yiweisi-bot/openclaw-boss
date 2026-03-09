#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
openclaw-boss 配置文件

用户可以自定义数据源路径，如不配置则使用自动发现。
"""

from pathlib import Path

# 工作空间根目录
WORKSPACE = Path("/root/.openclaw/workspace")

# 可选：自定义数据源路径
# 如果为 None，则自动发现

# 记忆文件目录
MEMORY_DIR = None  # 自动发现：WORKSPACE / "memory"

# 长期记忆文件
MEMORY_FILE = None  # 自动发现：WORKSPACE / "MEMORY.md"

# Git 项目目录列表（可以是多个）
GIT_PROJECTS = None  # 自动发现：扫描 WORKSPACE 下所有 .git 目录

# 博客项目目录
BLOG_PROJECT = None  # 自动发现：扫描常见博客路径

# 需要排除的敏感文件
NEVER_READ_FILES = [
    "TOOLS.md",
    ".env",
    ".env.local",
    "config.json",
    "secrets.json",
    "*.key",
    "*.pem",
]

# 敏感关键词（读取文件时跳过包含这些词的行）
SENSITIVE_KEYWORDS = [
    "密码", "授权码", "Token", "API Key", "Secret", "密钥",
    "验证问题", "验证答案", "IP 地址", "房间密码", "邮箱账号",
    "sk-", "ghp_", "glpat-", "LETRD",
]

# 评分权重（总和应为 1.0）
SCORING_WEIGHTS = {
    "activity": 0.15,      # 活跃度（会话）
    "productivity": 0.25,  # 生产力（Git 提交）
    "learning": 0.20,      # 学习能力（新技能）
    "content": 0.25,       # 内容产出（博客/文档）
    "system": 0.15,        # 系统化（定时任务）
}

# 报告输出目录
REPORTS_DIR = WORKSPACE / "reports"
