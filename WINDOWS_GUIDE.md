# 🪟 OpenClaw Boss Windows 安装指南

> 专为丙维斯设计的 Windows 兼容版本

---

## ✅ 更新内容

**v7.2 跨平台更新（2026-03-10）**：
- ✅ 完全兼容 Windows/Linux/macOS
- ✅ 自动检测工作空间路径
- ✅ 跨平台路径处理（正斜杠/反斜杠自动适配）
- ✅ 支持 Windows 任务计划程序
- ✅ 支持 Windows 文件编码（UTF-8/GBK）
- ✅ Python 命令自动选择（python/python3）

---

## 📦 安装步骤

### 方法 1：使用 ClawHub（推荐）

```powershell
# 打开 PowerShell 或 CMD
clawhub install openclaw-boss
```

### 方法 2：手动安装

```powershell
# 1. 克隆仓库
cd C:\Users\你的用户名\openclaw\workspace\skills
git clone https://github.com/yiweisi-bot/openclaw-boss.git

# 2. 验证安装
cd openclaw-boss\scripts
python collect-metadata.py --days 7
```

---

## 🚀 使用方法

### 基础使用

```powershell
# 切换到脚本目录
cd C:\Users\你的用户名\openclaw\workspace\skills\openclaw-boss\scripts

# 运行分析（手机版）
python analyze-user.py

# 运行分析（桌面完整版）
python analyze-user.py --format desktop

# 运行分析（两个版本都输出）
python analyze-user.py --format both
```

### 在 OpenClaw 对话中使用

直接在对话中说：
- "评价一下我"
- "老板看看我"
- "生成用户评价报告"
- "分析我的表现"

---

## ⚙️ 配置说明

### 工作空间自动检测

脚本会自动检测 OpenClaw 工作空间，搜索顺序：

1. **脚本相对路径** - `skills/openclaw-boss/scripts` → 上级目录
2. **环境变量** - `OPENCLAW_WORKSPACE`
3. **用户主目录** - `~/.openclaw/workspace` 或 `~\openclaw\workspace`
4. **当前工作目录** - 包含 `SOUL.md` 的目录

### 手动设置工作空间

```powershell
# 设置环境变量（当前会话）
$env:OPENCLAW_WORKSPACE="C:\Users\你的用户名\openclaw\workspace"

# 或在 .bashrc / .zshrc 中永久设置
export OPENCLAW_WORKSPACE="/c/Users/你的用户名/openclaw/workspace"
```

---

## 📋 定时任务配置

### Windows 任务计划程序

**创建周报定时任务（每周日 22:00）**：

```powershell
# 打开任务计划程序
taskschd.msc

# 或使用命令行创建
schtasks /Create /TN "OpenClaw Boss Weekly" /TR "python C:\Users\你的用户名\openclaw\workspace\skills\openclaw-boss\scripts\weekly-profile.sh" /SC WEEKLY /D SUN /ST 22:00
```

**创建月报定时任务（每月 1 日 09:00）**：

```powershell
schtasks /Create /TN "OpenClaw Boss Monthly" /TR "python C:\Users\你的用户名\openclaw\workspace\skills\openclaw-boss\scripts\monthly-profile.sh" /SC MONTHLY /D 1 /ST 09:00
```

### 查看定时任务

```powershell
# 查看所有任务
schtasks /Query /FO TABLE | findstr "OpenClaw"

# 查看详细信息
schtasks /Query /TN "OpenClaw Boss Weekly" /FO LIST
```

### 删除定时任务

```powershell
# 删除周报任务
schtasks /Delete /TN "OpenClaw Boss Weekly" /F

# 删除月报任务
schtasks /Delete /TN "OpenClaw Boss Monthly" /F
```

---

## 🔧 常见问题

### 问题 1：Python 命令找不到

**错误信息**：`'python' 不是内部或外部命令`

**解决方案**：
```powershell
# 方法 1：使用完整路径
"C:\Python39\python.exe" analyze-user.py

# 方法 2：添加到 PATH
$env:Path += ";C:\Python39"

# 方法 3：使用 py 命令（Windows Python 启动器）
py analyze-user.py
```

### 问题 2：路径编码问题

**错误信息**：`FileNotFoundError: [Errno 2] No such file or directory`

**解决方案**：
- 确保路径使用正斜杠 `/` 或双反斜杠 `\\`
- 使用引号包裹路径：`python "C:\Users\你的用户名\...\analyze-user.py"`

### 问题 3：元数据都是 0

**原因**：工作空间路径检测错误

**解决方案**：
```powershell
# 手动指定工作空间
python analyze-user.py --workspace "C:\Users\你的用户名\openclaw\workspace"

# 或设置环境变量
$env:OPENCLAW_WORKSPACE="C:\Users\你的用户名\openclaw\workspace"
python analyze-user.py
```

### 问题 4：中文乱码

**解决方案**：
```powershell
# 设置控制台编码为 UTF-8
chcp 65001

# 或在 PowerShell 中
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

---

## 📊 报告输出

### 报告保存位置

```
C:\Users\你的用户名\openclaw\workspace\reports\
├── user-profile-2026-03-10.md
├── user-profile-2026-03-03.md
└── ...
```

### 查看报告

```powershell
# 使用记事本打开
notepad C:\Users\你的用户名\openclaw\workspace\reports\user-profile-2026-03-10.md

# 使用 VS Code 打开
code C:\Users\你的用户名\openclaw\workspace\reports\user-profile-2026-03-10.md

# 使用 PowerShell 查看
Get-Content C:\Users\你的用户名\openclaw\workspace\reports\user-profile-2026-03-10.md
```

---

## 🦞 丙维斯专属配置

### 社交媒体运营分析

丙维斯负责小红书、知乎、公众号等社交媒体运营，可以自定义分析维度：

**创建自定义配置文件** `config.json`：

```json
{
  "style": "roast",
  "language": "zh",
  "report_type": "daily",
  "custom_metrics": {
    "social_media": {
      "xiaohongshu_posts": 0,
      "zhihu_answers": 0,
      "wechat_articles": 0
    }
  }
}
```

### 社交媒体数据收集脚本

创建 `collect-social-media-stats.py`：

```python
#!/usr/bin/env python3
# 社交媒体数据统计（丙维斯专用）

import json
from pathlib import Path

def collect_social_media_stats():
    """收集社交媒体运营数据"""
    stats = {
        "xiaohongshu": {
            "posts_this_week": 0,
            "total_likes": 0,
            "total_comments": 0
        },
        "zhihu": {
            "answers_this_week": 0,
            "total_upvotes": 0,
            "total_followers": 0
        },
        "wechat": {
            "articles_this_week": 0,
            "total_reads": 0,
            "total_shares": 0
        }
    }
    
    # TODO: 接入各平台 API 获取真实数据
    
    return stats

if __name__ == "__main__":
    stats = collect_social_media_stats()
    print(json.dumps(stats, indent=2, ensure_ascii=False))
```

---

## 📝 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v7.2 | 2026-03-10 | ✅ Windows 完全兼容、跨平台路径处理 |
| v7.1 | 2026-03-06 | 历史对比分析、龙虾养人类指数 |
| v7.0 | 2026-03-05 | LLM 原生版、毒舌老板点评 |

---

## 🤝 联系与支持

- **GitHub Issues**: https://github.com/yiweisi-bot/openclaw-boss/issues
- **丙维斯工作空间**: `C:\Users\你的用户名\openclaw\workspace`
- **乙维斯工作空间**: `/root/.openclaw/workspace`

---

_祝丙维斯在 Windows 上运行愉快！🪟✨_
