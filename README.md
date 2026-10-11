# AI Learning Notes

[Read the interactive HTML](https://ai-learning-notes-psi.vercel.app/) · [AI Product Manager Playbook](https://ai-learning-notes-psi.vercel.app/ai-product-manager-playbook.html) · [中文说明](./README_ZH.md)

This repository presents a structured learning path from large-language-model fundamentals to production AI systems. The material is organized by conceptual dependency and end-to-end execution flow.

It now includes a second, linked handbook that translates technical principles into product metrics, optimization decisions, trade-offs, evaluation plans, portfolio evidence, and interview answers for AI product managers. Use the **AI 产品经理手册** button on the website homepage to open it.

```text
Natural-language input
  → Tokenization and embeddings
  → Transformer and attention
  → Pre-training, post-training, fine-tuning, and alignment
  → Inference caches, cost, and latency
  → RAG, memory, and context engineering
  → LLM, harness, ReAct, MCP, skills, plugins, and tools
  → Evaluation, safety, deployment, and AI product engineering
```

## Knowledge Structure

| Module | Scope |
|---|---|
| 0. Knowledge map | Overall concept map and recommended learning order |
| 1. LLM fundamentals | Parameters, model files, tokenization, embeddings, Transformer, attention, Q/K/V, FFN, residual connections, normalization, causal masking, BERT, and multimodality |
| 2. Training and alignment | Pre-training, post-training, SFT, RLHF, PPO, DPO, ORPO, KTO, GRPO, RLVR, LoRA/PEFT, optimization, distributed training, and evaluation |
| 3. Agent systems | LLM, harness, MCP, skills, plugins, tools, ReAct, RAG, memory, context, KV cache, prompt cache, orchestration, and reliable execution |
| 4. Compute and hardware | Compute, memory, bandwidth, GPU, CUDA, NCCL, local inference, Apple unified memory, and multi-GPU training |
| 5. Model ecosystem | General and vertical models, open weights, model families, infrastructure layers, commercialization, and time-sensitive fact checking |
| 6. AI product and interaction engineering | Evaluation, annotation, system productization, AI writing style, Computer Use, and rich-text rendering |
| 7. Principle quick reference | Nine high-frequency questions covering Agent construction, evaluation, model iteration, attention, Q/K/V, and framework-independent orchestration |
| 8. End-to-end execution paths | Offline training, online inference, Agent execution, small-model experiments, and realistic local-hardware boundaries |
| 9. Engineering, safety, and context | Markdown, JSON, JSON Schema, state machines, exception handling, concurrency, red teaming, context engineering, and source verification |

## Reading Paths

- **Core path:** Modules 1 → 2 → 3 → 8.
- **Engineering path:** Modules 3 → 8 → 9.
- **Infrastructure path:** Modules 1 → 2 → 4.
- **Product path:** Modules 3 → 5 → 6 → 9.

## Formats

- `ai-learning-notes.md`: canonical text with Mermaid diagrams.
- `index.html` / `ai-learning-notes.html`: interactive browser edition with navigation and rendered diagrams.
- `ai-learning-notes.docx`: offline, printable edition with embedded diagrams.
- `ai-product-manager-playbook.md`: canonical AI product manager handbook.
- `ai-product-manager-playbook.html`: interactive browser edition of the handbook.
- `build_html.py`: dependency-free generator for both HTML editions; run `python3 build_html.py` after editing either Markdown source.
