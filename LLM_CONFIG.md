# LLM 配置指南

## 🎯 当前状态

openclaw-boss v6.0 支持**LLM 驱动分析**，但需要配置才能启用。

**默认行为**：
- ✅ 优先尝试调用 LLM
- ⚠️ 如果 LLM 不可用，自动降级到规则引擎
- ✅ 保证 100% 可用性

---

## 🔧 启用 LLM 驱动

### 方案 1：使用 OpenClaw 内置模型（推荐）

OpenClaw 已经配置了模型，可以直接使用：

```bash
# 测试模型调用
openclaw ask --model doubao/ark-code-latest "你好"
```

如果这个命令可用，LLM 驱动会自动工作。

### 方案 2：配置 API Key

编辑环境变量：

```bash
# ~/.bashrc 或~/.zshrc
export LLM_API_KEY="your-api-key-here"
export LLM_MODEL="doubao/ark-code-latest"
```

### 方案 3：使用 sessions_spawn（需要 OpenClaw 支持）

在 `analyze-user.py` 中使用：

```python
from openclaw import sessions_spawn

# 创建临时会话进行分析
session = sessions_spawn(
    task=f"分析以下元数据：{metadata}",
    runtime="subagent",
    model="doubao/ark-code-latest"
)
```

---

## 📊 LLM vs 规则引擎对比

| 特性 | LLM 驱动 | 规则引擎 |
|------|---------|---------|
| 评分来源 | 大模型理解 | Python 公式 |
| 点评质量 | ⭐⭐⭐⭐⭐ 有趣、有洞察 | ⭐⭐⭐ 机械、模板化 |
| 响应速度 | 5-15 秒 | <1 秒 |
| 成本 | Token 费用 | 免费 |
| 稳定性 | 依赖 API | 100% 稳定 |
| 透明度 | 黑盒 | 公式可见 |

---

## 🎯 推荐配置

### 开发环境
```bash
# 使用规则引擎（快速、免费）
# 不需要额外配置
```

### 生产环境
```bash
# 使用 LLM 驱动（更好的用户体验）
# 配置 API Key 或使用 OpenClaw 内置模型
```

### 混合模式（推荐）
```python
# 默认使用 LLM
# LLM 失败时自动降级到规则引擎
# 平衡体验和稳定性
```

---

## 🔍 检查 LLM 状态

```bash
# 检查是否能调用 LLM
cd /root/.openclaw/workspace/skills/openclaw-boss/scripts
python3 llm-analyzer.py --metadata test.json

# 查看日志
cat /root/.openclaw/workspace/reports/llm-debug.log
```

---

## 📝 当前限制

由于 OpenClaw 环境的限制：
1. ❌ 不能直接调用外部 API（需要配置）
2. ❌ sessions_spawn 可能不可用（取决于版本）
3. ✅ 规则引擎始终可用（备用方案）

---

## 💡 最佳实践

1. **开发测试**：使用规则引擎（快速）
2. **用户体验**：使用 LLM 驱动（有趣）
3. **生产部署**：混合模式（LLM 优先，规则备用）

---

## 🚀 未来计划

- [ ] 集成 OpenClaw 内置模型调用
- [ ] 支持多种 LLM 提供商
- [ ] 添加 LLM 缓存（减少 Token 消耗）
- [ ] 支持本地模型（Ollama 等）

---

**当前状态**：✅ 规则引擎可用，⚠️ LLM 需要配置
