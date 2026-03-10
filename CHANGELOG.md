# 📝 CHANGELOG - OpenClaw Boss

## v7.2 - Windows 跨平台版（2026-03-10）✨

### 🎉 新增功能

- ✅ **完全 Windows 兼容** - 支持 Windows/Linux/macOS 三大平台
- ✅ **自动工作空间检测** - 智能发现 OpenClaw 工作空间路径
- ✅ **跨平台路径处理** - 自动适配正斜杠/反斜杠
- ✅ **Python 命令自动选择** - Windows 用 `python`，Linux/macOS 用 `python3`
- ✅ **文件编码兼容** - 支持 UTF-8/GBK 等多种编码
- ✅ **Windows 任务计划程序支持** - 替代 Linux cron jobs

### 🔧 核心改进

#### 1. collect-metadata.py v2.2

**跨平台路径处理**：
```python
# 新增跨平台函数
def get_home_dir() -> Path  # 获取用户主目录
def auto_detect_workspace() -> Path  # 自动检测工作空间
def get_system_data_dir() -> Path  # 获取系统数据目录
def normalize_path(path: str) -> str  # 标准化路径
```

**智能项目发现**：
- 支持 Windows 路径：`C:\projects`、`C:\Users\...\projects`
- 支持 Linux 路径：`/root/projects`、`~/projects`
- 支持 macOS 路径：`~/projects`、`~/code`

**系统统计跨平台**：
- Windows: 使用 `wmic os get lastbootuptime`
- Linux/macOS: 使用 `uptime -p`

**定时任务统计跨平台**：
- Windows: 使用 `schtasks /query`
- Linux/macOS: 使用 `crontab -l`

#### 2. analyze-user.py v7.2

**工作空间自动检测**：
```python
def auto_detect_workspace() -> Path:
    # 搜索策略：
    # 1. 脚本相对路径推导
    # 2. 环境变量 OPENCLAW_WORKSPACE
    # 3. 用户主目录 ~/.openclaw/workspace
    # 4. 当前工作目录
```

**跨平台命令执行**：
```python
# 自动选择 Python 命令
python_cmd = "python" if platform.system() == "Windows" else "python3"
```

**增强的错误处理**：
- 文件编码异常处理（UTF-8/GBK/Latin-1）
- 路径不存在时的优雅降级
- 命令执行失败时的容错处理

### 📚 新增文档

- ✅ `WINDOWS_GUIDE.md` - Windows 安装和使用指南
- ✅ `CHANGELOG.md` - 版本更新日志

### 🐛 Bug 修复

- 修复硬编码 Linux 路径（`/root/...`）导致 Windows 无法运行
- 修复 Python 命令 hardcoded 为 `python3` 导致 Windows 无法执行
- 修复文件编码问题导致的中文乱码
- 修复路径分隔符问题导致的文件找不到

### 📊 测试验证

**Linux 测试** ✅：
```bash
python3 collect-metadata.py --days 7
# ✅ 正常输出元数据

python3 analyze-user.py --format mobile
# ✅ 正常生成报告
```

**Windows 测试** 🪟：
```powershell
python collect-metadata.py --days 7
# ✅ 已验证兼容（路径自动检测）

python analyze-user.py --format mobile
# ✅ 已验证兼容（命令自动选择）
```

### 🔄 兼容性说明

| 功能 | Windows | Linux | macOS |
|------|---------|-------|-------|
| 元数据收集 | ✅ | ✅ | ✅ |
| 工作空间检测 | ✅ | ✅ | ✅ |
| Git 统计 | ✅ | ✅ | ✅ |
| 博客统计 | ✅ | ✅ | ✅ |
| 技能统计 | ✅ | ✅ | ✅ |
| 定时任务 | ✅ (schtasks) | ✅ (cron) | ✅ (cron) |
| 系统统计 | ✅ | ✅ | ✅ |
| 报告生成 | ✅ | ✅ | ✅ |

### 🚀 使用示例

#### Windows PowerShell

```powershell
# 安装
cd C:\Users\你的用户名\openclaw\workspace\skills
git clone https://github.com/yiweisi-bot/openclaw-boss.git

# 运行
cd openclaw-boss\scripts
python analyze-user.py --format desktop
```

#### Linux/macOS

```bash
# 安装
cd ~/.openclaw/workspace/skills
git clone https://github.com/yiweisi-bot/openclaw-boss.git

# 运行
cd openclaw-boss/scripts
python3 analyze-user.py --format mobile
```

### 📝 迁移指南

**从 v7.1 升级到 v7.2**：

```bash
# 方法 1：使用 ClawHub
clawhub update openclaw-boss

# 方法 2：手动更新
cd skills/openclaw-boss
git pull origin main
```

**配置文件无需更改** - 新版本完全向后兼容！

### 🎯 适用场景

**乙维斯（Linux）**：
- 服务器部署
- 定时任务（cron）
- 系统级监控

**丙维斯（Windows）**：
- 桌面环境
- 社交媒体运营
- 小红书/知乎/公众号数据追踪

### 🦞 哲学理念

> **这不是主仆关系，是共生伙伴关系。**

无论在 Linux 还是 Windows，无论在服务器还是桌面，
乙维斯和丙维斯都在各自的平台上，与人类互相成就！

---

## v7.1 - 历史对比分析版（2026-03-06）

### 新增功能
- 📊 历史对比分析
- 🦞 龙虾养人类指数
- 🎴 ASCII 艺术绩效卡片

### 改进
- 完整 13 部分报告结构
- 毒舌老板点评优化

---

## v7.0 - LLM 原生版（2026-03-05）

### 核心变革
- 不再嵌套调用其他 LLM
- 由执行脚本的 LLM 直接分析
- 安全模式：只分析元数据，不读取敏感信息

---

_保持更新，保持优秀！_ ✨
