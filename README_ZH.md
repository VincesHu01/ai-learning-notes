# AI 学习笔记

[在线阅读 HTML](./index.html) · [English](./README.md) · [Markdown 正文](./ai-learning-notes.md) · [Word 版](./ai-learning-notes.docx)

本仓库是一套从大语言模型基础原理延伸到生产级 AI 系统的体系化学习笔记，内容按照知识依赖关系与端到端运行流程组织。

```text
自然语言输入
  → Tokenizer 与 Embedding
  → Transformer 与 Attention
  → 预训练、后训练、微调与对齐
  → 推理缓存、成本与延迟
  → RAG、Memory 与上下文工程
  → LLM、Harness、ReAct、MCP、Skill、Plugin 与 Tool
  → 评测、安全、部署与 AI 产品工程
```

## 知识结构

| 模块 | 内容范围 |
|---|---|
| 0. 知识体系总览 | 全局概念图与推荐学习顺序 |
| 1. 大模型基础 | 参数、模型文件、Tokenizer、Embedding、Transformer、Attention、Q/K/V、FFN、残差连接、归一化、因果掩码、BERT 与多模态 |
| 2. 训练与对齐 | 预训练、后训练、SFT、RLHF、PPO、DPO、ORPO、KTO、GRPO、RLVR、LoRA/PEFT、优化、多卡训练与评测 |
| 3. Agent 体系 | LLM、Harness、MCP、Skill、Plugin、Tool、ReAct、RAG、Memory、Context、KV Cache、Prompt Cache、编排与可靠执行 |
| 4. 算力与硬件 | 算力、内存、带宽、GPU、CUDA、NCCL、本地推理、Apple 统一内存与多卡训练 |
| 5. 模型生态 | 通用与垂类模型、开放权重、模型家族、基础设施、商业化与时效事实核验 |
| 6. AI 产品与交互工程 | 评测、标注、系统产品化、AI 文风、Computer Use 与富文本渲染 |
| 7. 关键原理速查 | 从零构建 Agent、评测、模型迭代、Attention、Q/K/V 和无框架编排等九个高频问题 |
| 8. 端到端完整链路 | 离线训练、在线推理、Agent 执行、小模型实验与本地硬件边界 |
| 9. 工程、安全与上下文 | Markdown、JSON、JSON Schema、状态机、异常、并发、红队、上下文工程与来源核验 |

## 推荐阅读路径

- **核心路径：** 模块 1 → 2 → 3 → 8。
- **工程路径：** 模块 3 → 8 → 9。
- **基础设施路径：** 模块 1 → 2 → 4。
- **产品路径：** 模块 3 → 5 → 6 → 9。

## 文件格式

- `ai-learning-notes.md`：包含 Mermaid 图表的正文源文件。
- `index.html` / `ai-learning-notes.html`：带目录导航和渲染图表的浏览器版本。
- `ai-learning-notes.docx`：内嵌图表、适合离线阅读与打印的版本。
