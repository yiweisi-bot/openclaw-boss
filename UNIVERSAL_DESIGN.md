# openclaw-boss 通用化设计文档

## 🎯 设计目标

让 **任何 OpenClaw 用户** 都能使用 openclaw-boss 技能，无论其：
- 工作空间结构如何
- 是否使用 Git
- 是否有博客
- 记忆文件组织方式如何

---

## 🔧 通用化实现

### 1. 自动发现数据源

#### Git 项目发现
```python
# 不硬编码项目路径
# 自动扫描多个可能的位置
search_dirs = [
    base_dir,                    # 工作空间根目录
    base_dir.parent / "projects", # 上级 projects 目录
    Path.home() / "projects",     # 用户主目录 projects
    Path("/root/projects"),       # 常见服务器路径
]

# 查找所有 .git 目录
for git_dir in search_dir.rglob(".git"):
    if valid_git_repo(git_dir.parent):
        projects.append(git_dir.parent)
```

#### 博客项目发现
```python
# 支持多种博客结构
blog_patterns = [
    "**/blog/**/*.md",
    "**/posts/**/*.md",
    "**/articles/**/*.md",
    "**/content/blog/**/*.md",
    "**/src/content/blog/**/*.md",
]

# 自动扫描所有匹配的模式
```

#### 记忆文件发现
```python
# 尝试多个可能的目录名
memory_dirs = [
    base_dir / "memory",
    base_dir / "memories",
    base_dir / "logs",
    base_dir / "daily",
]

# 找到第一个有效的就用
```

---

### 2. 优雅降级

#### 数据可用性检查
```python
metadata["data_availability"] = {
    "sessions": sessions_available,
    "memory": memory_available,
    "git": git_available,
    "skills": skills_available,
    "blog": blog_available,
    "cron": cron_available,
}
```

#### 动态评分权重
```python
# 数据不可用时给基础分 70，而不是 0
session_score = 70 if not data_avail.get("sessions") else min(100, sessions_total * 2)
git_score = 70 if not data_avail.get("git") else min(100, commits_week * 3)

# 报告中标注数据状态
print(f"✅ 会话：{total} 条 {'(可用)' if available else '(不可用)'}")
```

---

### 3. 安全保护

#### 敏感文件过滤
```python
NEVER_READ_FILES = [
    "TOOLS.md", ".env", ".env.local", 
    "config.json", "secrets.json", "*.key", "*.pem",
]

SENSITIVE_KEYWORDS = [
    "密码", "授权码", "Token", "API Key", "Secret", "密钥",
    "验证问题", "验证答案", "IP 地址", "房间密码", "邮箱账号",
]
```

#### 只读元数据
```python
# ✅ 读取：文件数量、提交次数、文章数量
# ❌ 不读：文件内容、提交信息、文章内容

stats["total_files"] = len(files)  # ✅ 只计数
stats["total_commits"] = count     # ✅ 只计数
```

---

## 📊 适配场景

### 场景 1：完整数据（Yiweisi）
```
✅ sessions: 47 条
✅ memory: 16 个文件
✅ git: 64 次提交（本周 33 次）
✅ skills: 26 个
✅ blog: 25 篇
✅ cron: 5 个任务
```
**结果**: 完整报告，所有维度正常评分

### 场景 2：仅有 Git（开发者）
```
❌ sessions: 不可用
❌ memory: 不可用
✅ git: 100 次提交（本周 20 次）
❌ skills: 不可用
❌ blog: 不可用
❌ cron: 不可用
```
**结果**: 基于 Git 数据评分，其他维度给基础分 70

### 场景 3：仅有技能（学习者）
```
❌ sessions: 不可用
✅ memory: 5 个文件
❌ git: 不可用
✅ skills: 15 个（本月 5 个）
❌ blog: 不可用
❌ cron: 不可用
```
**结果**: 基于技能和记忆评分，其他维度给基础分 70

### 场景 4：最小数据（新用户）
```
❌ sessions: 不可用
❌ memory: 不可用
❌ git: 不可用
❌ skills: 不可用
❌ blog: 不可用
❌ cron: 不可用
```
**结果**: 所有维度基础分 70，报告标注"数据不足"

---

## 🔍 数据源优先级

### 会话数据
1. `sessions_list` 命令（OpenClaw 内置）
2. 降级：标记为不可用

### Git 数据
1. 工作空间根目录的 .git
2. projects/ 目录下的所有 Git 项目
3. ~/projects/ 目录
4. /root/projects/ 目录
5. 降级：标记为不可用

### 博客数据
1. src/content/blog/ (Astro/React)
2. content/blog/ (Hugo/Gatsby)
3. posts/ (Jekyll)
4. articles/ (自定义)
5. 降级：标记为不可用

### 记忆文件
1. memory/ 目录
2. memories/ 目录
3. logs/ 目录
4. daily/ 目录
5. 降级：标记为不可用

---

## 🛠️ 配置选项（未来）

允许用户通过配置文件自定义：

```python
# config.py（可选）
GIT_PROJECTS = ["/path/to/project1", "/path/to/project2"]
BLOG_DIR = "/path/to/blog/posts"
MEMORY_DIR = "/path/to/memory/files"
SCORING_WEIGHTS = {
    "activity": 0.20,  # 自定义权重
    "productivity": 0.30,
    "learning": 0.20,
    "content": 0.15,
    "system": 0.15,
}
```

---

## ✅ 通用化检查清单

- [x] 不硬编码工作空间路径
- [x] 自动发现 Git 项目
- [x] 自动发现博客项目
- [x] 支持多种记忆文件目录名
- [x] 数据不可用时优雅降级
- [x] 动态调整评分权重
- [x] 敏感信息过滤
- [x] 只读元数据，不读内容
- [x] 报告标注数据可用性
- [x] 语法检查通过
- [x] 版本号同步（6.0.0）

---

## 📈 测试计划

### 测试环境
1. **Yiweisi 环境**（完整数据）
2. **最小环境**（无 Git、无博客）
3. **开发者环境**（仅有 Git）
4. **学习者环境**（仅有技能）

### 测试用例
- [x] 完整数据生成报告
- [x] 部分数据生成报告
- [x] 无数据生成报告（基础分）
- [x] 敏感信息不泄露
- [x] 效率指数正常显示
- [x] 活跃时段正常显示

---

## 🎯 结论

openclaw-boss v6.0 现在是**真正通用**的技能：
- ✅ 适配任何 OpenClaw 用户
- ✅ 不依赖特定项目结构
- ✅ 数据缺失时优雅降级
- ✅ 绝对安全的元数据模式
- ✅ 评分公正透明

**任何 OpenClaw 用户都可以直接使用！** 🎉
