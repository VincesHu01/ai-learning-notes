# AI 学习笔记 · 体系化整理（AI Learning Notes）

> 从 **87 个真实 AI 学习提问**（豆包 78 问 + 千问 9 问）中提炼的体系化学习笔记。通俗讲解 + 保留专业术语，配 **10 张思维导图/流程图**，逐题标注答案位置、**覆盖无遗漏**。

[English README](./README_EN.md) | 📄 [Markdown 笔记](./ai-learning-notes.md) | 🌐 [HTML 可视化版](./ai-learning-notes.html) | 📝 [Word 版](./ai-learning-notes.docx)

---

## 📖 这是什么

这是一份「从真实对话里长出来」的 AI 学习笔记。原始素材是本人在豆包（Doubao）与千问（Qianwen）上学习 AI 的完整对话记录——不是教程抄写，而是把一个学习者在真实追问中踩过的每个知识点，重新按逻辑体系组织成一份可以系统性复习、也可以按题索引的笔记。

**三个特点：**

1. **体系化** —— 87 个散装提问被重组为 7 大模块：基础 → 训练 → Agent → 硬件 → 生态 → 产品 → 深度原理，符合「从模型是什么 → 怎么造 → 怎么用 → 怎么落地」的认知链路。
2. **可视化** —— 内含 10 张图表（Mermaid 渲染）：知识体系总览思维导图、0.1B 训练全流程图、Agent 运行链路图、ReAct 循环、RAG 双模式、注意力机制、对齐算法谱系、算力三要素、大模型生态地图等。
3. **可索引** —— 文末附「📋 问题覆盖索引」，把全部 87 个原始提问逐题映射到对应章节，方便自查「这个问题在哪讲的」。

---

## 🗂 内容结构

| 模块 | 覆盖内容 |
|---|---|
| **一 · 大模型基础** | 参数与文件格式（GGUF/Safetensors/量化）、Tokenizer 与 BPE、Transformer 与 Attention（Q/K/V）、预训练 vs 推理、0.1B 从零训练全流程、MoE 稀疏模型、开源协议（MIT/Apache/GPL） |
| **二 · 训练与对齐** | 预训练 vs 后训练、SFT/RLHF/DPO/GRPO/RLVR/RLAIF/ORPO/AgentRL 谱系、Scaling Law、评测体系（lm-eval-harness、MMLU、SWE-bench、AA Index）、微调流程 |
| **三 · Agent 体系** | Agent = LLM + Harness + MCP + Skill + Memory、Harness（项目经理）、MCP（USB-C 类比）、ReAct 循环、RAG 三种形态（本地/联网/作为 MCP 工具）、Skill vs Plugin、LangChain/AutoGen、记忆与上下文、KV-Cache 小学生版 |
| **四 · 算力与硬件** | 算力/显存/带宽三大件、芯片如何训练大模型、CUDA 生态（cuBLAS/cuDNN/NCCL）、Ollama 本地推理、Windows 显存 vs macOS 统一内存、RTX 显卡与 Mac Studio 对标、大厂训练环境（Linux + A800/H800） |
| **五 · 大模型生态** | GPT 家族（5.5/5.6 → 6 Astra 的 6 大提升）、Qwen/豆包 Seed/Gemini/Claude/MiMo 全家桶、垂类 vs 通用（美团问小团）、开放权重四成本、芯片/云厂商/第三方服务商产业链、豆包商业化盈亏 |
| **六 · AI 产品经理视角** | AI 知识占比评估（45%）与补课清单、评测与标注、Muse/Qmuse/Hive、端到端/DevRel/Side Project、9 家互联网公司面试素材、「AI 味」为何重、Computer Use 原理 |
| **七 · 深度原理追问** | 千问 9 问：从零训 Agent、国际评测标准、模型迭代逻辑、注意力本质、QKV 在预训练/推理的异同、产品渲染原理、无 LangChain 的编排 |

---

## 📁 文件说明

```
.
├── README.md                  # 本文件（中文）
├── README_EN.md               # 英文版 README
├── ai-learning-notes.md       # 笔记正文（Markdown，内嵌 Mermaid 源码，GitHub 直接渲染）
├── ai-learning-notes.html     # 可视化交互版（深色主题、目录导航、Mermaid 实时渲染）
├── ai-learning-notes.docx     # Word 版（10 张图表已渲染为图片嵌入，可直接打印）
└── diagrams/                  # 10 张独立高清图表 PNG
    ├── d1_overview.png        # 知识体系总览（思维导图）
    ├── d2_tokenizer.png       # Tokenizer / BPE 流程
    ├── d3_transformer.png     # Transformer 与注意力
    ├── d4_pipeline.png        # 0.1B 从零训练全流程
    ├── d5_align.png           # 对齐算法谱系
    ├── d6_agent.png           # Agent 运行链路（ReAct 循环）
    ├── d7_react.png           # ReAct 最小循环
    ├── d8_rag.png             # RAG：静态 vs 动态 MCP 工具
    ├── d9_hw.png              # 算力/显存/带宽三大件
    └── d10_eco.png            # 大模型生态地图
```

**三种格式怎么选：**

- **日常阅读 / GitHub 浏览** → `ai-learning-notes.md`（Mermaid 图直接渲染）
- **系统复习 / 演示** → `ai-learning-notes.html`（深色主题 + 侧边目录导航 + 可视化图表）
- **打印 / 批注 / 存档** → `ai-learning-notes.docx`（图表以图片嵌入，离线可看）

---

## 🚀 快速开始

```bash
git clone https://github.com/VincesHu01/ai-learning-notes.git
cd ai-learning-notes

# 直接打开 HTML 版（浏览器）
open ai-learning-notes.html

# 或用 VS Code / Typora 阅读 Markdown 版（Mermaid 插件渲染图表）
```

> HTML 版的 Mermaid 图表通过 jsDelivr CDN 加载，需联网；离线时显示图表源码。
> Word 版完全离线可用。

---

## 📊 覆盖度

- **豆包 3 段对话 · 78 个提问** → 全部覆盖（含 1 问非 AI 学术内容已标注跳过）
- **千问分享页 · 9 个深度提问** → 全部覆盖
- 每个提问在文末「问题覆盖索引」中都有对应章节号，**可逐题验证无遗漏**

---

## 🧭 推荐学习路径

如果你也是 AI 学习者，建议按笔记的模块顺序阅读：

```
大模型基础（它是什么）
   → 训练与对齐（它怎么被造出来）
      → Agent 体系（它怎么被用起来）
         → 算力与硬件（它跑在什么上面）
            → 大模型生态（行业里都有谁）
               → AI 产品经理视角（怎么变成产品）
                  → 深度原理追问（回到本质）
```

---

## 📌 一些高频考点速记（节选自笔记）

- **Agent = LLM（脑）+ Harness（手脚）+ MCP（接口）+ Skill（方法）+ Memory（记忆）**
- **训练 = 反复刷题改笔记；推理 = 拿着笔记做题不再改**
- **SFT 照抄示范；RLHF 请老师打分；DPO 直接告诉 A 比 B 好；RLVR 做有标准答案的题**
- **算力决定快不快，显存决定能不能跑，带宽决定多卡协同时浪费多少算力**
- **RAG 不是免幻觉，是减幻觉；它也可以只是 Agent 工具池里的一个 MCP 工具**

---

## 📄 License

本笔记内容采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 授权：可自由转载、修改，需署名。

---

*整理自真实 AI 学习对话 · 2026-10*
