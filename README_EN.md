# AI Learning Notes — A Systematic Compilation

> A structured study note distilled from **87 real AI-learning questions** (78 from Doubao + 9 from Qianwen). Plain-language explanations that keep the professional terminology, illustrated with **10 mind maps & flowcharts**, with a per-question index so that **no question is left uncovered**.

[中文 README](./README.md) | 📄 [Notes (Markdown)](./ai-learning-notes.md) | 🌐 [HTML Version](./ai-learning-notes.html) | 📝 [Word Version](./ai-learning-notes.docx)

---

## 📖 What Is This

This is an AI study note that "grew out of real conversations". The source material is the complete transcript of my own AI-learning conversations on Doubao and Qianwen. Rather than copying a textbook, it re-organizes every knowledge point a real learner stumbled upon while asking follow-up questions into a systematic reference — one you can review end-to-end, or consult question by question.

**Three highlights:**

1. **Systematic** — 87 scattered questions re-organized into 7 modules: Fundamentals → Training → Agents → Hardware → Ecosystem → Product → Deep Principles, following the cognitive path "what a model is → how it's built → how it's used → how it ships".
2. **Visual** — 10 diagrams (rendered as Mermaid): a knowledge-map mind map, the full 0.1B training pipeline, the Agent runtime loop, the ReAct cycle, RAG in two modes, attention mechanics, the alignment-algorithm family tree, the compute/VRAM/bandwidth trio, and an LLM-ecosystem map.
3. **Indexable** — A "Question Coverage Index" at the end maps all 87 original questions to their sections, so you can verify that nothing was skipped.

---

## 🗂 Structure

| Module | Coverage |
|---|---|
| **1 · LLM Fundamentals** | Parameters & file formats (GGUF/Safetensors/quantization), Tokenizer & BPE, Transformer & Attention (Q/K/V), pre-training vs inference, the full 0.1B from-scratch pipeline, MoE sparse models, open-source licenses (MIT/Apache/GPL) |
| **2 · Training & Alignment** | Pre-training vs post-training, the SFT/RLHF/DPO/GRPO/RLVR/RLAIF/ORPO/AgentRL family, Scaling Laws, evaluation (lm-eval-harness, MMLU, SWE-bench, AA Index), fine-tuning workflow |
| **3 · Agent Architecture** | Agent = LLM + Harness + MCP + Skill + Memory; the Harness as "project manager"; MCP as the "USB-C of AI"; the ReAct loop; RAG in three forms (local / web / as-an-MCP-tool); Skill vs Plugin; LangChain/AutoGen; memory & context; KV-Cache explained simply |
| **4 · Compute & Hardware** | Compute / VRAM / bandwidth; how chips train LLMs; the CUDA ecosystem (cuBLAS/cuDNN/NCCL); Ollama local inference; Windows VRAM vs macOS unified memory; RTX GPUs vs Mac Studio; how big labs actually train (Linux + A800/H800) |
| **5 · LLM Ecosystem** | The GPT family (5.5/5.6 → 6 Astra's six upgrades); Qwen, Doubao Seed, Gemini, Claude, MiMo; vertical vs general models (Meituan's "Wen Xiao Tuan"); the four costs open weights change; the chip/cloud/vendor value chain; Doubao's business economics |
| **6 · AI PM Perspective** | Knowledge-gap assessment (45%) and a study checklist; evaluation & annotation; Muse/Qmuse/Hive; end-to-end / DevRel / side projects; interview material for 9 Chinese internet companies; why outputs feel "AI-flavored"; how Computer Use works |
| **7 · Deep Principles (Qianwen ×9)** | Training an Agent from scratch; international eval standards; why models iterate so fast; the essence of attention; QKV in pre-training vs inference; product rendering; orchestration without LangChain |

---

## 📁 Files

```
.
├── README.md                  # This file (Chinese)
├── README_EN.md               # English README
├── ai-learning-notes.md       # The notes (Markdown with embedded Mermaid, rendered natively on GitHub)
├── ai-learning-notes.html     # Interactive version (dark theme, TOC navigation, live Mermaid)
├── ai-learning-notes.docx     # Word version (10 diagrams embedded as images, print-ready)
└── diagrams/                  # 10 standalone high-resolution PNGs
    ├── d1_overview.png        # Knowledge map (mind map)
    ├── d2_tokenizer.png       # Tokenizer / BPE pipeline
    ├── d3_transformer.png     # Transformer & attention
    ├── d4_pipeline.png        # 0.1B from-scratch training pipeline
    ├── d5_align.png           # Alignment algorithm family tree
    ├── d6_agent.png           # Agent runtime loop (ReAct)
    ├── d7_react.png           # Minimal ReAct cycle
    ├── d8_rag.png             # RAG: static vs dynamic MCP tool
    ├── d9_hw.png              # Compute / VRAM / bandwidth trio
    └── d10_eco.png            # LLM ecosystem map
```

**Which format to use:**

- **Everyday reading / GitHub browsing** → `ai-learning-notes.md` (Mermaid renders natively)
- **Systematic review / presenting** → `ai-learning-notes.html` (dark theme + sidebar TOC + live diagrams)
- **Printing / annotating / archiving** → `ai-learning-notes.docx` (diagrams embedded, fully offline)

---

## 🚀 Quick Start

```bash
git clone https://github.com/VincesHu01/ai-learning-notes.git
cd ai-learning-notes

# Open the HTML version in a browser
open ai-learning-notes.html

# Or read the Markdown in VS Code / Typora (with a Mermaid extension)
```

> The HTML version loads Mermaid from the jsDelivr CDN and needs internet access; offline it falls back to showing diagram source code. The Word version works fully offline.

---

## 📊 Coverage

- **Doubao · 3 conversations · 78 questions** → all covered (1 non-AI academic question explicitly marked as out of scope)
- **Qianwen share page · 9 deep questions** → all covered
- Every question is mapped to a section number in the final "Question Coverage Index" — coverage can be verified question by question.

---

## 🧭 Suggested Reading Path

If you are also learning AI, read the modules in order:

```
Fundamentals (what it is)
   → Training & Alignment (how it's built)
      → Agents (how it's used)
         → Compute & Hardware (what it runs on)
            → Ecosystem (who's in the game)
               → AI PM perspective (how it becomes a product)
                  → Deep principles (back to first principles)
```

---

## 📌 Cheat-Sheet (excerpted from the notes)

- **Agent = LLM (brain) + Harness (hands & feet) + MCP (interface) + Skill (methods) + Memory**
- **Training = redoing problem sets and revising your notes; inference = solving new problems with the finished notes, notes unchanged**
- **SFT copies worked examples; RLHF asks a teacher to grade; DPO is told "A is better than B"; RLVR solves problems with verifiable answers**
- **Compute decides how fast, VRAM decides whether it runs at all, bandwidth decides how much compute is wasted across GPUs**
- **RAG doesn't eliminate hallucination, it reduces it — and it can be just one MCP tool inside an Agent's toolbox**

---

## 📄 License

Content licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): free to share and adapt with attribution.

---

*Compiled from real AI-learning conversations · October 2026*
