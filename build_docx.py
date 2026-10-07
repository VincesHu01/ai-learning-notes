#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build ai-learning-notes.docx: parse markdown, render diagrams to PNG, assemble a styled DOCX."""
import os, re, html
from PIL import Image, ImageDraw, ImageFont

BASE = "/Users/vinces/WorkBuddy/2026-10-07-00-05-01/ai-learning-notes"
SRC = os.path.join(BASE, "ai-learning-notes.md")
DIG = os.path.join(BASE, "diagrams")
OUT = os.path.join(BASE, "ai-learning-notes.docx")
os.makedirs(DIG, exist_ok=True)

FONT_PATH = "/System/Library/Fonts/STHeiti Light.ttc"
F = ImageFont.truetype(FONT_PATH, 15)
FB = ImageFont.truetype(FONT_PATH, 16)
FT = ImageFont.truetype(FONT_PATH, 20)

# ---------- text utils ----------
def text_w(s, font):
    return max(font.getlength(s), 1)

def wrap(s, font, maxw):
    out = []
    for para in s.split('\n'):
        if text_w(para, font) <= maxw:
            out.append(para); continue
        cur = ''
        for ch in para:
            if text_w(cur + ch, font) > maxw and cur:
                out.append(cur); cur = ch
            else:
                cur += ch
        if cur: out.append(cur)
    return out

def draw_box(d, cx, cy, text, w=200, h=None, fill="#2563eb", fg="#ffffff", font=F, radius=10):
    lines = wrap(text, font, w - 20)
    lh = font.size + 6
    if h is None:
        h = max(40, len(lines) * lh + 14)
    x0, y0 = cx - w//2, cy - h//2
    d.rounded_rectangle([x0, y0, x0+w, y0+h], radius=radius, fill=fill, outline="#1f2937")
    ty = cy - (len(lines)*lh)//2
    for ln in lines:
        d.text((cx - text_w(ln, font)//2, ty), ln, fill=fg, font=font)
        ty += lh
    return w, h

def arrow(d, p1, p2, label=None, color="#374151"):
    # trim to border boxes handled by caller; here draw straight with arrowhead
    import math
    x1,y1,x2,y2 = *p1, *p2
    d.line([x1,y1,x2,y2], fill=color, width=2)
    ang = math.atan2(y2-y1, x2-x1)
    L = 9
    for da in (math.radians(150), math.radians(210)):
        ex = x2 + L*math.cos(ang+da); ey = y2 + L*math.sin(ang+da)
        d.line([x2,y2,ex,ey], fill=color, width=2)
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        lw = text_w(label, F)
        d.rectangle([mx-lw/2-3, my-9, mx+lw/2+3, my+9], fill="#ffffff")
        d.text((mx-lw/2, my-8), label, fill=color, font=F)

def border_pt(box, target):
    # box = (cx,cy,w,h); return point on box border toward target
    cx,cy,w,h = box
    tx,ty = target
    dx, dy = tx-cx, ty-cy
    if dx == 0 and dy == 0: return (cx,cy)
    # scale to border
    hw, hh = w/2, h/2
    sx = hw/abs(dx) if dx else float('inf')
    sy = hh/abs(dy) if dy else float('inf')
    s = min(sx, sy)
    return (cx + dx*s, cy + dy*s)

# ---------- flowchart renderer ----------
def arrow_poly(d, pts, label=None, color="#374151"):
    import math
    # polyline with arrowhead at the end, label placed near 2nd point
    for a, b in zip(pts, pts[1:]):
        d.line([a[0], a[1], b[0], b[1]], fill=color, width=2)
    x2, y2 = pts[-1]; x1, y1 = pts[-2]
    ang = math.atan2(y2-y1, x2-x1)
    L = 9
    for da in (math.radians(150), math.radians(210)):
        ex = x2 + L*math.cos(ang+da); ey = y2 + L*math.sin(ang+da)
        d.line([x2, y2, ex, ey], fill=color, width=2)
    if label:
        lx, ly = pts[1]
        lw = text_w(label, F)
        d.rectangle([lx-lw/2-3, ly-9, lx+lw/2+3, ly+9], fill="#ffffff")
        d.text((lx-lw/2, ly-8), label, fill=color, font=F)

def render_flow(nodes, edges, title, fname, w=1100, h=820):
    img = Image.new("RGB", (w, h), "#ffffff")
    d = ImageDraw.Draw(img)
    d.text((20, 12), title, fill="#0f172a", font=FT)
    pos = {}
    for nid, label, cx, cy, *rest in nodes:
        fill = rest[0] if rest else "#2563eb"
        bw, bh = draw_box(d, cx, cy+40, label, fill=fill)
        pos[nid] = (cx, cy+40, bw, bh)
    for e in edges:
        s, t = e[0], e[1]
        lab = e[2] if len(e) > 2 else None
        style = e[3] if len(e) > 3 else None
        sb = pos[s]; tb = pos[t]
        if style in ("right", "left"):
            sgn = 1 if style == "right" else -1
            p1 = (sb[0] + sgn*sb[2]//2, sb[1])          # side border of src
            p2 = (tb[0] + sgn*tb[2]//2, tb[1])          # side border of dst
            if sgn > 0:
                midx = max(sb[0] + sb[2]//2, tb[0] + tb[2]//2) + 55
            else:
                midx = min(sb[0] - sb[2]//2, tb[0] - tb[2]//2) - 55
            pts = [p1, (midx, p1[1]), (midx, p2[1]), p2]
            arrow_poly(d, pts, lab)
        elif style == "bottom":
            p1 = (sb[0], sb[1] + sb[3]//2)              # bottom border of src
            p2 = (tb[0], tb[1] + tb[3]//2)              # bottom border of dst
            midy = max(sb[1] + sb[3]//2, tb[1] + tb[3]//2) + 55
            pts = [p1, (p1[0], midy), (p2[0], midy), p2]
            arrow_poly(d, pts, lab)
        else:
            p1 = border_pt(sb, (tb[0], tb[1]))
            p2 = border_pt(tb, (sb[0], sb[1]))
            arrow(d, p1, p2, lab)
    img.save(fname)
    return fname

# ---------- mindmap renderer (horizontal tree) ----------
def render_mind(root, branches, title, fname, w=1100, h=None):
    # compute needed height: leaves stack
    nrows = sum(max(1, len(b[1])) for b in branches)
    ROW = 36
    h = 100 + nrows * ROW + 40
    img = Image.new("RGB", (w, h), "#ffffff")
    d = ImageDraw.Draw(img)
    d.text((20, 12), title, fill="#0f172a", font=FT)
    y = 70
    rx, ry = 160, h/2
    draw_box(d, rx, ry, root, w=170, fill="#0f172a")
    branch_colors = ["#2563eb","#0891b2","#7c3aed","#db2777","#ea580c","#16a34a","#ca8a04"]
    for bi, (blabel, leaves) in enumerate(branches):
        color = branch_colors[bi % len(branch_colors)]
        nleaf = max(1, len(leaves))
        by = y + ROW*nleaf/2
        draw_box(d, 440, by, blabel, w=170, fill=color)
        arrow(d, (rx+85, ry), (440-85, by))
        if not leaves:
            y += ROW; continue
        ly = y
        for leaf in leaves:
            draw_box(d, 760, ly+ROW/2, leaf, w=300, h=28, fill="#e2e8f0", fg="#0f172a",
                     font=ImageFont.truetype(FONT_PATH, 13))
            arrow(d, (440+85, by), (760-150, ly+ROW/2))
            ly += ROW
        y += ROW*nleaf
    img.save(fname)
    return fname

# ================= DIAGRAM SPECS (in mermaid block order) =================
DIAGRAMS = [
 ("flow", "图1 · 知识体系总览（思维导图）",
   None, None,  # placeholder; actual overview is mindmap handled below
 ),
]
# We will instead build explicit list:
def D_overview():
    return render_mind(
        "AI 学习笔记",
        [("大模型基础", ["参数/文件格式","Tokenizer","Transformer/Attention","预训练vs推理","训练全流程 0.1B","MoE 稀疏","开源协议"]),
         ("训练与对齐", ["预训练/后训练","SFT/RLHF/DPO/GRPO","RLVR/AgentRL","Scaling Law","评测 lm-eval"]),
         ("Agent 体系", ["Agent=LLM+Harness+MCP","Harness 项目经理","MCP 工具协议","ReAct 循环","RAG 检索增强","Skill vs Plugin","LangChain 编排"]),
         ("算力与硬件", ["算力/显存/带宽","分布式训练","CUDA 生态","Ollama 本地","GPU vs Mac 内存","RTX / Mac Studio"]),
         ("大模型生态", ["GPT 家族 5.5/6","Qwen / 豆包 Seed","Gemini / Claude","MiMo","垂类 vs 通用","开放权重四成本","商业化"]),
         ("AI 产品与工程", ["评测与标注","系统产品化","上下文工程","Computer Use","富文本渲染"])],
        "图1 · 知识体系总览（思维导图）",
        os.path.join(DIG, "d1_overview.png"), w=1180, h=900)

def D_tokenizer():
    nodes=[("A","原始文本",90,210,"#64748b"),("B","按字节/字符切分",330,210),
           ("C","统计相邻对频率",560,210),("D","合并最高频对→新子词",800,210),
           ("E","重复至词表大小",1030,210),("F","BPE 词表+编码表",1230,210,"#0891b2"),
           ("G","文本 ↔ token id 互转",1430,210,"#16a34a")]
    edges=[("A","B"),("B","C"),("C","D"),("D","E"),("E","F"),("F","G")]
    return render_flow(nodes,edges,"图2 · Tokenizer 与 BPE 分词流程",os.path.join(DIG,"d2_tokenizer.png"),w=1560,h=320)

def D_transformer():
    nodes=[("A","输入 token 序列",430,60,"#64748b"),("E","Embedding 嵌入",430,150),
           ("Q","Q/K/V 线性投影",430,240),("At","Attention: softmax(Q·Kᵀ/√d)·V",470,340,"#7c3aed"),
           ("N","Add & Norm",430,440),("F","前馈神经网络 FFN",430,530),
           ("N2","Add & Norm",430,620),("O","输出表示→预测下一 token",430,710,"#16a34a")]
    edges=[("A","E"),("E","Q"),("Q","At"),("At","N"),("N","F"),("F","N2"),("N2","O")]
    return render_flow(nodes,edges,"图3 · Transformer 与注意力机制",os.path.join(DIG,"d3_transformer.png"),w=900,h=800)

def D_pipeline():
    nodes=[("S0","原始语料 raw dump",430,55,"#64748b"),("S1","清洗语料",430,140),
           ("S2","手写 BPE Tokenizer",430,225),("S3","Transformer 基座 + Triton/FlexAttention",470,320,"#0891b2"),
           ("S4","多卡预训练 + Scaling Law",430,415),("S5","对照 SFT / DPO / RLVR",430,500,"#7c3aed"),
           ("S6","lm-eval-harness 评测",430,585),("S7","可验证环境 + Harness",430,670,"#db2777"),
           ("S8","长程 Agent + self-judge",430,755,"#16a34a")]
    edges=[("S0","S1"),("S1","S2"),("S2","S3"),("S3","S4"),("S4","S5"),("S5","S6"),("S6","S7"),("S7","S8")]
    return render_flow(nodes,edges,"图4 · 0.1B 模型从零训练全流程",os.path.join(DIG,"d4_pipeline.png"),w=900,h=840)

def D_align():
    nodes=[("Base","基座模型\n(可能接着乱编)",400,55,"#64748b"),("SFT","SFT 监督微调",400,150,"#2563eb"),
           ("RLHF","RLHF (PPO+RM)",180,255),("DPO","DPO 直接偏好优化",620,255,"#0891b2"),
           ("RLAIF","RLAIF (AI反馈)",180,355,"#0891b2"),
           ("RLVR","RLVR 可验证奖励",400,255,"#7c3aed"),
           ("GRPO","GRPO",250,400,"#7c3aed"),("ORPO","ORPO",400,400,"#7c3aed"),
           ("ARL","AgentRL",550,400,"#7c3aed"),("RRL","Reasoning RL",700,400,"#7c3aed")]
    edges=[("Base","SFT"),("SFT","RLHF"),("SFT","DPO"),("SFT","RLVR"),("RLHF","RLAIF"),
           ("RLVR","GRPO"),("RLVR","ORPO"),("RLVR","ARL"),("RLVR","RRL")]
    return render_flow(nodes,edges,"图5 · 对齐算法谱系 (SFT→RLHF/DPO→RLVR…)",os.path.join(DIG,"d5_align.png"),w=920,h=470)

def D_agent():
    nodes=[("U","用户任务",400,55,"#64748b"),("M","记忆模块检索历史",400,145),
           ("C","打包: 新输入+记忆 → 上下文",400,235),("L","LLM 大脑思考",400,325,"#2563eb"),
           ("H","Harness 调度层",400,415,"#7c3aed"),("P","MCP 工具池\nrag/代码/文件/API",400,505,"#db2777"),
           ("D","任务结束?",400,610,"#ca8a04"),("R","返回结果给用户",400,710,"#16a34a")]
    edges=[("U","M"),("M","C"),("C","L"),("L","H"),("H","P"),
           ("P","L","Observation","right"),
           ("D","R"),("D","L","否(循环)","left")]
    return render_flow(nodes,edges,"图6 · Agent 运行链路 (ReAct 循环)",os.path.join(DIG,"d6_agent.png"),w=820,h=800)

def D_react():
    nodes=[("T","Thought 思考\n该调什么工具",160,210,"#2563eb"),
           ("A","Action 行动\n调用工具",470,210,"#7c3aed"),
           ("O","Observation 观察\n拿到结果",780,210,"#db2777")]
    edges=[("T","A"),("A","O"),("O","T","loop","bottom")]
    return render_flow(nodes,edges,"图7 · ReAct 最小循环",os.path.join(DIG,"d7_react.png"),w=960,h=340)

def D_rag():
    nodes=[("Q1","用户问题",200,90,"#64748b"),("R1","向量库检索相关片段",200,200,"#0891b2"),
           ("C1","拼进 prompt 上下文",200,310,"#0891b2"),("L1","LLM 生成回答",200,420,"#16a34a"),
           ("Q2","用户任务",640,90,"#64748b"),("H","Harness 调度层",640,200,"#7c3aed"),
           ("T","rag_local / rag_web",640,310,"#db2777"),("O","Observation 原文片段",640,420,"#db2777")]
    edges=[("Q1","R1"),("R1","C1"),("C1","L1"),("Q2","H"),("H","T","MCP 调用"),("T","O")]
    return render_flow(nodes,edges,"图8 · RAG：静态向量库 vs 动态 MCP 工具",os.path.join(DIG,"d8_rag.png"),w=860,h=500)

def D_hw():
    nodes=[("C","算力 TFLOPS\n算得快不快",200,150,"#2563eb"),
           ("V","显存 VRAM\n仓库够不够大",470,150,"#0891b2"),
           ("B","带宽\n仓库大门多宽",740,150,"#7c3aed"),
           ("T","三大件共同决定\n大模型能否跑、跑多快",470,330,"#16a34a")]
    edges=[("C","T"),("V","T"),("B","T")]
    return render_flow(nodes,edges,"图9 · 算力 / 显存 / 带宽 三大件",os.path.join(DIG,"d9_hw.png"),w=940,h=420)

def D_eco():
    return render_mind(
        "大模型生态",
        [("OpenAI", ["通用与推理模型","Agent 与工具能力"]),
         ("阿里巴巴", ["Qwen 开放权重系列","多尺寸与多模态"]),
         ("字节跳动", ["豆包及 Seed 系列","内容与办公生态"]),
         ("Google", ["Gemini API 型号","Gemma 开放模型"]),
         ("Anthropic", ["Opus/Sonnet/Haiku","Fable / Mythos 等代际"]),
         ("小米", ["MiMo 系列"]),
         ("其他", ["DeepSeek / Kimi / Grok","智谱 / 元宝 / 千问"])],
        "图10 · 大模型生态地图",
        os.path.join(DIG, "d10_eco.png"), w=1180, h=820)

def D_training_line():
    nodes=[("A","合法数据采集",150,180,"#64748b"),("B","清洗 去重 过滤 配比",390,180),
           ("C","Tokenizer 与编码",650,180),("D","预训练 Transformer",900,180,"#0891b2"),
           ("E","SFT 与偏好对齐",1150,180,"#7c3aed"),("F","评测 量化 部署",1400,180,"#16a34a")]
    edges=[("A","B"),("B","C"),("C","D"),("D","E"),("E","F")]
    return render_flow(nodes,edges,"图11 · 离线训练线",os.path.join(DIG,"d11_training.png"),w=1550,h=300)

def D_inference_line():
    nodes=[("U","用户输入与规则",430,40,"#64748b"),("C","记忆 RAG 与上下文",430,125),
           ("T","Tokenizer 与 Embedding",430,210),("X","多层 Transformer",430,295,"#2563eb"),
           ("A","Attention FFN Norm 残差",430,380,"#7c3aed"),("O","下一个 token 分布",430,465),
           ("K","追加 KV Cache 并循环",430,550,"#0891b2"),("Z","解码为最终输出",430,635,"#16a34a")]
    edges=[("U","C"),("C","T"),("T","X"),("X","A"),("A","O"),("O","K"),("K","Z")]
    return render_flow(nodes,edges,"图12 · 在线推理线",os.path.join(DIG,"d12_inference.png"),w=900,h=720)

def D_agent_full():
    nodes=[("U","用户目标与权限",430,40,"#64748b"),("C","上下文工程",430,125),
           ("L","LLM 规划下一步",430,210,"#2563eb"),("J","JSON Schema 工具调用",430,295),
           ("H","Harness 校验与调度",430,380,"#7c3aed"),("P","MCP API Plugin Tool",430,465,"#db2777"),
           ("V","外部验证或 self judge",430,550,"#ca8a04"),("A","交付或请求用户确认",430,650,"#16a34a")]
    edges=[("U","C"),("C","L"),("L","J"),("J","H"),("H","P"),("P","V"),("V","A"),("V","C","重试","right")]
    return render_flow(nodes,edges,"图13 · Agent 执行线",os.path.join(DIG,"d13_agent_full.png"),w=900,h=740)

DIAG_BUILDERS = [D_overview, D_tokenizer, D_transformer, D_pipeline, D_align,
                 D_agent, D_react, D_rag, D_hw, D_eco,
                 D_training_line, D_inference_line, D_agent_full]
DIAG_ALTS = [
    'AI 学习笔记知识体系总览思维导图',
    'Tokenizer 与 BPE 分词流程图',
    'Transformer 与注意力机制流程图',
    '0.1B 模型从零训练全流程图',
    'SFT、RLHF、DPO、RLVR 等对齐算法谱系图',
    'Agent 的 ReAct 运行链路图',
    'ReAct 思考、行动、观察循环图',
    '本地向量库 RAG 与动态 MCP 检索对比图',
    '算力、显存与带宽关系图',
    '大模型厂商与模型生态地图',
    '大模型离线训练线流程图',
    '大模型在线推理线流程图',
    'Agent 在线执行线流程图',
]

# ================= MARKDOWN -> DOCX =================
import docx
from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement

CJK_FONT = 'Noto Sans SC Thin'

def esc_inline(t):
    # returns list of (text, bold, code)
    # process **bold** and `code`
    t = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', t)
    res = []
    i = 0
    buf = ''
    mode = 0  # 0 normal,1 bold,2 code
    while i < len(t):
        if t[i:i+2] == '**' and mode != 2:
            if buf: res.append((buf, mode==1, False)); buf=''
            mode = 1 - mode if mode in (0,1) else 0
            i += 2; continue
        if t[i] == '`' and mode != 1:
            if buf: res.append((buf, False, mode==2)); buf=''
            mode = 2 if mode==0 else 0
            i += 1; continue
        buf += t[i]; i += 1
    if buf: res.append((buf, mode==1, mode==2))
    return res

doc = Document()
# base style
st = doc.styles['Normal']
st.font.name = CJK_FONT
st.font.size = Pt(10.5)
for font_attr in ('w:ascii', 'w:hAnsi', 'w:eastAsia', 'w:cs'):
    st.element.rPr.rFonts.set(__import__('docx').oxml.ns.qn(font_attr), CJK_FONT)
st.element.rPr.set(__import__('docx').oxml.ns.qn('w:hint'), 'eastAsia')

for section in doc.sections:
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.75)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

for style_name in ['Title', 'Heading 1', 'Heading 2', 'Heading 3', 'Heading 4']:
    style = doc.styles[style_name]
    style.font.name = CJK_FONT
    style.font.color.rgb = RGBColor(0, 0, 0)
    for font_attr in ('w:ascii', 'w:hAnsi', 'w:eastAsia', 'w:cs'):
        style.element.rPr.rFonts.set(__import__('docx').oxml.ns.qn(font_attr), CJK_FONT)
    style.element.rPr.set(__import__('docx').oxml.ns.qn('w:hint'), 'eastAsia')

title_ppr = doc.styles['Title'].element.get_or_add_pPr()
title_border = title_ppr.find(__import__('docx').oxml.ns.qn('w:pBdr'))
if title_border is not None:
    title_ppr.remove(title_border)

doc.core_properties.title = 'AI 学习笔记 全流程体系化完整版'
doc.core_properties.subject = '大模型 训练 对齐 Agent RAG 缓存 算力与 AI 产品学习笔记'

# Title
h = doc.add_paragraph(style='Title')
h.add_run('AI 学习笔记 全流程体系化完整版')
sub = doc.add_paragraph('从大模型基础到 Agent 工程  含思维导图与流程图')
sub.runs[0].italic = True
sub.runs[0].font.color.rgb = RGBColor(0x55,0x55,0x55)

# parse
lines = open(SRC, encoding='utf-8').read().split('\n')
i = 0; N = len(lines)
in_code=False; code_buf=[]; code_lang=''
diag_idx = 0
in_table=False; tbl_buf=[]
img_w = Inches(6.3)

def flush_table():
    global in_table, tbl_buf
    if not tbl_buf: in_table=False; return
    data = [r for r in tbl_buf if not re.match(r'^\s*\|?[\s:\-|]+\|?\s*$', r)]
    tbl_buf=[]
    if not data:
        in_table=False; return
    rows=[ [c.strip() for c in r.strip().strip('|').split('|')] for r in data]
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    t.style = 'Light Grid Accent 1'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for ri, row in enumerate(rows):
        tr_pr = t.rows[ri]._tr.get_or_add_trPr()
        tr_pr.append(OxmlElement('w:cantSplit'))
        if ri == 0:
            tr_pr.append(OxmlElement('w:tblHeader'))
        for ci, cell in enumerate(row):
            p = t.cell(ri,ci).paragraphs[0]
            for (txt,bold,code) in esc_inline(cell):
                r = p.add_run(txt)
                if bold: r.bold=True
    in_table=False

while i < N:
    line = lines[i]
    if line.strip().startswith('```'):
        if not in_code:
            in_code=True; code_lang=line.strip()[3:].strip(); code_buf=[]
        else:
            in_code=False
            if code_lang=='mermaid':
                if diag_idx < len(DIAG_BUILDERS):
                    fn = DIAG_BUILDERS[diag_idx]()
                    diag_idx += 1
                    doc.add_picture(fn, width=img_w)
                    doc_pr = doc.inline_shapes[-1]._inline.docPr
                    doc_pr.set('descr', DIAG_ALTS[diag_idx - 1])
                    doc_pr.set('title', DIAG_ALTS[diag_idx - 1])
                    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                cp = doc.add_paragraph()
                cr = cp.add_run('\n'.join(code_buf)); cr.font.name='Courier New'; cr.font.size=Pt(9)
                cp.style = doc.styles['Normal']
            code_lang=''; code_buf=[]
        i+=1; continue
    if in_code:
        code_buf.append(line); i+=1; continue
    if line.strip().startswith('|') and '|' in line.strip()[1:]:
        if not in_table: in_table=True; tbl_buf=[]
        tbl_buf.append(line); i+=1; continue
    else:
        if in_table: flush_table()
    m=re.match(r'^(#{1,4})\s+(.*)$',line)
    if m:
        lvl=len(m.group(1)); txt=m.group(2).strip()
        if lvl==1 and txt == 'AI 学习笔记 全流程体系化完整版':
            i+=1; continue
        if lvl==1: hp = doc.add_heading(txt, level=1)
        elif lvl==2: hp = doc.add_heading(txt, level=2)
        elif lvl==3: hp = doc.add_heading(txt, level=3)
        else: hp = doc.add_heading(txt, level=4)
        hp.paragraph_format.keep_with_next = True
        i+=1; continue
    if line.startswith('>'):
        buf=[]
        while i<N and lines[i].startswith('>'):
            buf.append(re.sub(r'^>\s?','',lines[i])); i+=1
        p=doc.add_paragraph()
        for (txt,bold,code) in esc_inline(' '.join(buf)):
            r=p.add_run(txt)
            if bold: r.bold=True
            r.italic=True
            r.font.color.rgb = RGBColor(0x40,0x40,0x40)
        continue
    if re.match(r'^\s*[-*]\s+',line):
        buf=[]
        while i<N and re.match(r'^\s*[-*]\s+',lines[i]):
            buf.append(re.sub(r'^\s*[-*]\s+','',lines[i])); i+=1
        for item in buf:
            p=doc.add_paragraph(style='List Bullet')
            for (txt,bold,code) in esc_inline(item):
                r=p.add_run(txt); 
                if bold: r.bold=True
        continue
    if not line.strip():
        i+=1; continue
    if re.match(r'^\s*---+\s*$', line):
        i+=1; continue
    p=doc.add_paragraph()
    for (txt,bold,code) in esc_inline(line):
        r=p.add_run(txt)
        if bold: r.bold=True
        if code:
            r.font.name='Courier New'; r.font.size=Pt(9.5)
    i+=1
if in_table: flush_table()

def apply_cjk_font_to_run(run):
    run.font.name = CJK_FONT
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.get_or_add_rFonts()
    for font_attr in ('w:ascii', 'w:hAnsi', 'w:eastAsia', 'w:cs'):
        rfonts.set(__import__('docx').oxml.ns.qn(font_attr), CJK_FONT)
    rpr.set(__import__('docx').oxml.ns.qn('w:hint'), 'eastAsia')

for paragraph in doc.paragraphs:
    for run in paragraph.runs:
        apply_cjk_font_to_run(run)
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    apply_cjk_font_to_run(run)

doc.save(OUT)
print("WROTE", OUT, "diagrams rendered:", diag_idx)
