# AI Learning Notes Full Systematic Edition

This repository reorganizes **109 user turns from four exported AI-learning conversations** into one coherent learning path. Many turns contain multiple subquestions, so the notes are structured by conceptual dependency rather than chat chronology:

```text
Natural-language input
  → Tokenization and embeddings
  → Transformer and attention
  → Pre-training post-training fine-tuning and alignment
  → KV cache prompt cache and inference cost
  → RAG memory and context
  → LLM harness ReAct MCP skills plugins and tools
  → Evaluation safety deployment and AI product work
```

[中文 README](./README.md) · [Markdown notes](./ai-learning-notes.md) · [Visual HTML](./ai-learning-notes.html) · [Word edition](./ai-learning-notes.docx)

## What changed in this edition

- Restored 22 previously omitted turns from `AI术语认知.txt`, including model alignment, cache billing, LoRA, context engineering, and implementation controls.
- Added a source-by-source **109-turn coverage index**. Every turn maps to one or more sections; image-only exports are retained without inventing unavailable visual details.
- Corrected major conceptual conflations: KV cache vs prompt cache, token embeddings vs RAG embeddings, LLM vs agent, RLHF vs PPO, and fine-tuning vs alignment.
- Expanded residual connections, normalization, causal masks, FFNs, multi-head attention, LoRA matrices, reward models, PPO/DPO/ORPO/KTO/GRPO, AdamW, mixed precision, ZeRO, and distributed training.
- Added three end-to-end diagrams for offline training, online inference, and agent execution.
- Replaced unsupported parameter, pricing, profitability, and model-generation claims with a reproducible verification framework.

## Structure

| Module | Main coverage |
|---|---|
| 0 Knowledge map | Global map and reading order |
| 1 LLM fundamentals | Weight files, tokenization, embeddings, Transformer, Q/K/V, FFN, residuals, normalization, causal masks, BERT, multimodality |
| 2 Training and alignment | Pre/post-training, fine-tuning, alignment, SFT, RLHF, PPO, DPO, ORPO, KTO, GRPO, RLVR, LoRA/PEFT, optimizers, multi-GPU training |
| 3 Agent systems | LLM, harness, MCP, skill, plugin, tool, ReAct, RAG, memory, context, KV cache, prompt cache, WorkBuddy case study |
| 4 Compute and hardware | Compute, VRAM, bandwidth, GPU, CUDA, NCCL, Ollama, Apple unified memory, distributed training |
| 5 Model ecosystem | General vs vertical models, open weights, cloud/chip stack, Qwen, Gemini, Claude, Doubao, and freshness checks |
| 6 AI product management | Evaluation, annotation, capability matrix, interview gaps, Computer Use, style, and rich-text rendering |
| 7 Nine deep questions | Agent construction, benchmarks, model iteration, attention/QKV, and orchestration without a framework |
| 8 End-to-end flows | Offline training, online inference, agent execution, a 0.1B experiment, and realistic Mac limits |
| 9 Engineering and safety | Markdown/JSON/Schema, state machines, exceptions, deadlocks, red teaming, context engineering, freshness verification |

## Files

```text
.
├── README.md
├── README_EN.md
├── ai-learning-notes.md
├── ai-learning-notes.html
├── ai-learning-notes.docx
├── build_html.py
├── build_docx.py
├── fonts/                     # CJK font and OFL license for Word rendering
└── diagrams/
```

- `ai-learning-notes.md` is the source of truth, with Mermaid diagrams and the 109-turn coverage index.
- `ai-learning-notes.html` is optimized for browser reading with navigation and Mermaid rendering.
- `ai-learning-notes.docx` is designed for offline reading, printing, and annotation.
- The two build scripts regenerate the derived formats.
- `fonts/` contains the Noto Sans SC variable font and its SIL Open Font License for reproducible CJK rendering.

## Recommended reading path

Read Modules 1 → 2 → 3 → 8 first to understand how a model works, how it is trained, and how it becomes an agent. Continue with Modules 4 → 5 → 6 → 9 for hardware, industry, product, and governance. Use full-text search or the final coverage index for individual questions.

## Five essential corrections

1. **Token vectorization is not RAG vectorization**: an LLM consumes a sequence of token embeddings; RAG separately embeds document chunks for retrieval.
2. **Q/K/V are not the user's question, a database key, and a stored value**: they are tensors projected from hidden states with learned matrices.
3. **KV cache is not cross-request cached-input billing**: KV cache accelerates autoregressive decoding, while prompt/prefix caching is an API product mechanism.
4. **RLHF is not PPO**: RLHF describes a feedback source and pipeline; PPO is one possible optimizer, while DPO can avoid a separate reward model and PPO loop.
5. **An agent is not just an LLM**: it also needs a harness, state, tools, permissions, verification, and recovery logic.

## Coverage

| Source file | User turns |
|---|---:|
| AI学习荟萃.txt | 24 |
| AI术语认知.txt | 31 |
| WorkBuddy走红原因.txt | 25 |
| 大模型训练全流程任务完成指南.txt | 29 |
| **Total** | **109** |

The first source contains one tourism-paper review outside the AI scope; it remains listed and explicitly marked. Image-JSON turns are also preserved without fabricating missing visual content.

## Freshness and accuracy

Model names, parameter counts, context windows, prices, licenses, GPU pricing, and product capabilities change. Stable principles are separated from time-sensitive facts, which should be verified against official model pages, technical reports, API documentation, and model cards. This edition was reviewed on **2026-10-07**.

## License

The original notes are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Third-party names, documentation, and trademarks remain the property of their respective owners.
