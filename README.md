# AI 学习笔记 全流程体系化完整版

从 4 份真实聊天导出的 **109 个用户回合**中整理而成。许多回合一次包含十余个子问题，因此本项目不按聊天顺序堆叠答案，而是重组为一条完整认知链：

```text
自然语言输入
  → Tokenizer 与 Embedding
  → Transformer 与 Attention
  → 预训练 后训练 微调 对齐
  → KV Cache Prompt Cache 与推理成本
  → RAG Memory Context
  → LLM Harness ReAct MCP Skill Plugin Tool
  → 评测 安全 部署与 AI 产品
```

[English README](./README_EN.md) · [Markdown 正文](./ai-learning-notes.md) · [HTML 可视化版](./ai-learning-notes.html) · [Word 版](./ai-learning-notes.docx)

## 本次完整版改进

- 将原先遗漏的《AI术语认知》前 22 个回合补回，覆盖从术语分类、AI 产品经理能力，到缓存计费、LoRA、上下文工程和工程控制。
- 按 4 个源文件建立 **109 回合覆盖索引**，每个回合都映射到正文章节；图片回合不虚构无法从导出文件恢复的视觉细节。
- 纠正几个关键混淆：KV Cache ≠ Prompt Cache；token embedding ≠ RAG embedding；LLM ≠ Agent；RLHF ≠ PPO；微调 ≠ 对齐。
- 增补残差连接、归一化、因果掩码、FFN、多头注意力、LoRA 两矩阵、RM、PPO/DPO/ORPO/KTO/GRPO、AdamW、混合精度、ZeRO 与多卡并行。
- 增加离线训练线、在线推理线、Agent 执行线三条端到端流程图。
- 将未经官方材料支持的参数量、价格、盈利状态和代际性能数字改为核验框架，避免把推测写成事实。

## 内容结构

| 模块 | 核心内容 |
|---|---|
| 0 知识体系总览 | 全局思维导图与学习顺序 |
| 1 大模型基础 | 参数文件、Tokenizer、Embedding、Transformer、Q/K/V、FFN、残差、归一化、因果掩码、BERT、多模态 |
| 2 训练与对齐 | 预训练/后训练/微调/对齐、SFT、RLHF、PPO、DPO、ORPO、KTO、GRPO、RLVR、LoRA/PEFT、优化器与多卡 |
| 3 Agent 体系 | LLM、Harness、MCP、Skill、Plugin、Tool、ReAct、RAG、Memory、Context、KV Cache、Prompt Cache、WorkBuddy 案例 |
| 4 算力与硬件 | 算力、显存、带宽、GPU、CUDA、NCCL、Ollama、Apple 统一内存、多卡训练 |
| 5 模型生态 | 通用/垂类、开放权重、云与芯片产业链、Qwen、Gemini、Claude、豆包与时效核验 |
| 6 AI 产品经理 | 评测、标注、能力矩阵、面试补课、Computer Use、文本风格与富文本渲染 |
| 7 集中九问 | 从零构建 Agent、评测、模型迭代、Attention/QKV 与无框架编排速查 |
| 8 完整链路 | 离线训练、在线问答、Agent 执行、0.1B 实验和 Mac 的现实边界 |
| 9 工程与安全 | Markdown/JSON/Schema、状态机、异常、死锁、红队、上下文工程与时效信息核验 |

## 文件说明

```text
.
├── README.md
├── README_EN.md
├── ai-learning-notes.md
├── ai-learning-notes.html
├── ai-learning-notes.docx
├── build_html.py
├── build_docx.py
├── fonts/                     # Word 中文字体与 OFL 许可证
└── diagrams/
```

- `ai-learning-notes.md`：内容源文件，含 Mermaid 图与 109 回合覆盖索引。
- `ai-learning-notes.html`：适合浏览器阅读，带目录导航和 Mermaid 渲染。
- `ai-learning-notes.docx`：适合离线阅读、打印和批注，图表以图片嵌入。
- `build_html.py` / `build_docx.py`：可重复生成交付格式的脚本。
- `fonts/`：用于跨平台 Word 渲染的 Noto Sans SC 可变字体及 SIL Open Font License。
- `diagrams/`：Word 版使用的高清图表。

## 推荐阅读路径

第一次阅读按模块 1 → 2 → 3 → 8；理解“模型怎么工作、怎么训练、怎么变成 Agent”。随后读模块 4 → 5 → 6 → 9，补齐硬件、行业、产品和工程治理。遇到具体术语时可直接搜索正文，或从末尾覆盖索引反查原问题。

## 五个最重要的纠偏

1. **输入向量化不是 RAG 向量化**：LLM 输入是一串 token embedding；RAG 还会把文档 chunk 编成检索向量。
2. **Q/K/V 不是用户问题、知识库键和值**：它们是每层隐藏状态经 `Wq/Wk/Wv` 投影得到的张量。
3. **KV Cache 不等于跨请求缓存计费**：前者服务自回归解码，后者是服务商的 Prompt/Prefix Cache 产品机制。
4. **RLHF 不等于 PPO**：RLHF 是反馈来源和流程，PPO 是可选优化算法；DPO 可绕过独立 RM/PPO。
5. **Agent 不等于 LLM**：Agent 还需要 Harness、状态、工具、权限、验证和失败恢复。

## 覆盖度

| 原始文件 | 用户回合 |
|---|---:|
| AI学习荟萃.txt | 24 |
| AI术语认知.txt | 31 |
| WorkBuddy走红原因.txt | 25 |
| 大模型训练全流程任务完成指南.txt | 29 |
| **合计** | **109** |

第一份文件的第 1 回合是旅游减贫论文评析，不属于 AI 学习主题，但仍在覆盖索引中保留并标注范围；三个图片 JSON 回合也保留来源位置，不根据缺失像素臆造内容。

## 时效与准确性

模型名称、参数量、上下文长度、价格、许可证、显卡售价和产品能力都会变化。正文把稳定原理和时效事实分开；后者优先引用官方模型页、技术报告、API 文档和模型卡。项目校订日期为 **2026-10-07**。

## 使用与构建

直接下载三种交付格式即可阅读。若要重新生成 HTML 与 DOCX，请先查看脚本中的依赖与路径设置；Word 交付物应在生成后重新渲染并逐页检查。

## License

笔记正文采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)；引用的第三方名称、文档与商标归各自权利人所有。
