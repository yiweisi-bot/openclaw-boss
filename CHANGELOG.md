# 📝 CHANGELOG - OpenClaw Boss

## v8.0 - LLM 自主检索通用版（2026-03-10）🎯

### 🎉 重大变革

**核心改进**：
- ✅ **通用化设计** - 不预设具体数据源（博客/Git/技能...），适配所有用户场景
- ✅ **LLM 自主检索** - 由 LLM 使用工具（exec/read）自主收集数据，更灵活准确
- ✅ **简化脚本** - Python 脚本只输出分析指南，不收集数据，减少维护成本
- ✅ **多场景支持** - 支持任何创作形式（博客/视频/代码/设计/文章/小红书/播客...）
- ✅ **个性化锐评** - 基于真实检索数据，不要编造或照搬模板

### 📋 为什么需要通用化？

**v7.x 的问题**：
- ❌ 预设用户有博客、Git、技能等特定数据源
- ❌ Python 脚本收集数据，可能遗漏或格式不对
- ❌ 不够灵活，无法适应不同用户的使用场景

**v8.0 的解决方案**：
- ✅ 不预设数据源，让 LLM 自主发现用户有什么
- ✅ LLM 用工具直接检索，更准确灵活
- ✅ 通用提示词，适配所有用户场景

### 🔧 技术实现

**脚本简化**：
```python
# v7.x: 复杂的 Python 数据收集脚本
collect_metadata() → JSON → LLM 分析

# v8.0: 简单的指南输出
print_analysis_guide() → LLM 自主检索 → 生成报告
```

**LLM 检索流程**：
1. 检查工作空间的内容目录（`*/content/*`, `*/posts/*`...）
2. 检查 Git 仓库（`git log --since='7 days ago'`）
3. 检查技能/工具目录
4. 检查记忆/日记文件
5. 检查 cron 任务
6. 根据发现的问题创作锐评

### 🎯 通用化提示词

**创作产出**（任何形式）：
- 博客文章、视频、播客、设计稿、代码、文档、笔记、小红书、推文...

**学习成长**（任何形式）：
- 新技能、课程、书籍、教程、文章收藏、笔记...

**项目进展**（任何形式）：
- 代码项目、创意项目、学习项目、副业、爱好...

**效率与自动化**：
- 定时任务、脚本、工作流、模板...

**持续性与习惯**：
- 记忆文件、日记、打卡、习惯追踪...

### 📊 锐评创作指南

**公式**：`[真实数据] + [有趣比喻] + [emoji]`

**通用化示例**：
- "一周创作 20 篇内容，生产队的驴都不敢这么使！🫏"（不指定博客/视频）
- "同时搞 5 个项目，是准备开公司吗？💼"（不指定代码/创意）
- "凌晨 3 点还在肝，是在用生命创作吗？💀"（不指定写作/编程）
- "一周学 10 个新技能，准备开技能博物馆吗？🏛️"（通用学习）

⚠️ **重要提醒**：
- 不要照搬示例！示例只是教风格！
- 数据必须来自你的检索！不要编造！
- 锐评要个性化，针对这个用户的真实行为！

---

## v7.4 - 锐评出圈版（2026-03-10）🔥

### 🎉 新增功能

- ✅ **锐评合集前置** - 把最有趣的评论放到报告开头，吸引眼球
- ✅ **金句爆点设计** - 每份报告必须有 5-8 条能出圈的锐评金句
- ✅ **分类展示** - 用 emoji 分类锐评（💀最拼、🫏生产力、🏛️学习、🐷安全等）
- ✅ **数据支撑** - 每句锐评都有真实数据支撑，不是空洞吐槽
- ✅ **三段式设计** - 开头爆点金句 → 中间毒舌点评 → 结尾温暖鼓励

### 🔥 锐评风格升级

**核心原则**：
- 不是温和建议，是尖锐吐槽
- 不是官方点评，是朋友互怼
- 不是 AI 生成，是真人毒舌
- 不是拍马屁，是扎心真相

**爆点金句公式**：
```
[具体行为] + [夸张比喻] + [emoji]

示例：
"一周写 18 篇博客" + "生产队的驴都不敢这么使" + "🫏"
"一个月装 23 个技能" + "准备开技能博物馆" + "🏛️"
"凌晨 3 点写代码" + "用生命 coding" + "💀"
```

**锐评模板库**：
- 生产力类："生产队的驴都不敢这么使"🫏
- 学习类："准备开技能博物馆"🏛️
- 安全类："在服务器里养电子宠物"🐷
- 效率类："用头发换代码"💀
- 创意类："想法很多，落地的有几个"💡

### 📋 报告结构调整

**新增第二部分**：
- 🔥 本周锐评合集（5-8 条）
- 放在报告开头，紧接绩效卡片之后
- 适合截图分享到社交媒体

**原有部分优化**：
- 每个维度增加毒舌点评
- 老板总结增加温暖鼓励
- 整体风格更尖锐、更有趣

### 📱 传播设计

**适合出圈的元素**：
1. 爆点金句（适合做标题）
2. 数据支撑（增加可信度）
3. emoji 分类（增加趣味性）
4. 尖锐但温暖（让人又爱又恨）
5. ASCII 卡片（可选，适合 TUI 截图）

**传播场景**：
- GitHub 项目 README
- 技术博客文章
- 社交媒体分享
- 技术社区讨论
- 朋友圈炫耀/吐槽

---

## v7.3 - ASCII 卡片可选版（2026-03-10）✨

### 🎉 新增功能

- ✅ **ASCII 卡片可选显示** - 默认不显示，避免钉钉/微信等平台格式错乱
- ✅ **触发关键词控制** - 仅当用户输入包含"ASCII 图"时才显示卡片
- ✅ **跨平台友好** - 纯文本报告适合所有平台阅读

### 🔧 核心改进

#### 1. analyze-user.py v7.3

**新增 `--show-ascii` 参数**：
```bash
# 默认不显示 ASCII 卡片
python3 analyze-user.py --format mobile

# 仅当用户明确需要时显示
python3 analyze-user.py --format desktop --show-ascii
```

**触发逻辑**：
```python
if 用户输入中包含 "ASCII 图":
    显示 ASCII 卡片
else:
    不显示卡片（默认）
```

#### 2. SKILL.md 更新

**版本选择指南**：
- 删除了旧版多个关键词（完整版、截图、桌面版等）
- 简化为单一关键词："ASCII 图"
- 明确说明默认行为和设计理念

**输出格式说明**：
- 更新报告结构，标注卡片为可选
- 更新输出示例，展示两种情况
- 强调跨平台兼容性

### 📋 设计理念

**为什么默认不显示 ASCII 卡片？**
1. **平台兼容性**：ASCII 卡片在 TUI（终端）中显示效果好，但在钉钉、微信、网页等平台会换行错乱
2. **用户体验**：纯文本报告在所有平台都能正常阅读
3. **按需展示**：用户需要截图分享时，主动说"ASCII 图"即可

**触发示例**：
- ✅ "评价一下我" → 纯文本报告（默认）
- ✅ "分析一下我" → 纯文本报告（默认）
- ✅ "评价一下我，要 ASCII 图" → 显示 ASCII 卡片
- ✅ "生成报告，带 ASCII 图" → 显示 ASCII 卡片

---

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
