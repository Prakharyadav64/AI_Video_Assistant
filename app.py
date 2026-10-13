from __future__ import annotations

import time

from concurrent.futures import ThreadPoolExecutor

import re

from datetime import datetime

from typing import Any

import streamlit as st

from dotenv import load_dotenv

# Load environment variables before importing project modules.

load_dotenv()

st.set_page_config(

    page_title="Video Intelligence Studio",

    page_icon="🎬",

    layout="wide",

    initial_sidebar_state="expanded",

)

def render_html(html: str) -> None:
    """Render trusted app-owned HTML instead of displaying it as literal text."""
    html_renderer = getattr(st, "html", None)
    if callable(html_renderer):
        html_renderer(html)
    else:
        st.markdown(html, unsafe_allow_html=True)

st.markdown(

    """

    <style>

    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root { --line: rgba(170,184,220,.14); --muted:#9ba5bd; }

    html, body, [class*="css"] { font-family:'Manrope',sans-serif; }

    .stApp {

      background: radial-gradient(ellipse at 10% 0%,rgba(99,102,241,.16),transparent 34%),

      radial-gradient(ellipse at 95% 8%,rgba(34,211,238,.09),transparent 30%),#090b12;

      color:#f3f5ff;

    }

    [data-testid="stHeader"] { background:rgba(9,11,18,.72); }

    [data-testid="stSidebar"] { background:linear-gradient(180deg,#101423,#0c0f18); border-right:1px solid var(--line); }

    .block-container { max-width:1500px; padding-top:1.6rem; padding-bottom:3rem; }

    h1,h2,h3 { letter-spacing:-.04em; }

    .brand-row { display:flex; align-items:center; gap:12px; margin-bottom:1.2rem; }

    .brand-mark { width:44px;height:44px;border-radius:14px;display:flex;align-items:center;justify-content:center;

      background:linear-gradient(135deg,#8b5cf6,#22d3ee);color:#090b12;font-size:22px;font-weight:800; }

    .brand-name { font-size:1.08rem;font-weight:800;color:#f8fafc;line-height:1.2; }

    .brand-sub { color:#9ba5bd;font-size:.72rem;margin-top:4px;letter-spacing:.11em;text-transform:uppercase; }

    .eyebrow { color:#a5b4fc;font-size:.72rem;font-weight:800;letter-spacing:.18em;text-transform:uppercase;margin-bottom:.65rem; }

    .hero { position:relative;overflow:hidden;border:1px solid rgba(167,139,250,.24);border-radius:26px;

      padding:2rem 2.15rem;margin:.2rem 0 1.3rem;

      background:linear-gradient(120deg,rgba(31,37,69,.96),rgba(20,28,47,.92) 58%,rgba(13,44,58,.9));

      box-shadow:0 24px 80px rgba(0,0,0,.18); }

    .hero:after { content:"";position:absolute;width:290px;height:290px;border-radius:50%;right:-80px;top:-130px;

      background:radial-gradient(circle,rgba(103,232,249,.2),rgba(103,232,249,0) 70%); }

    .hero h1 { font-size:clamp(2rem,4vw,3.25rem);line-height:1.06;margin:0 0 .85rem;color:#fff;font-weight:800; }

    .hero p { color:#c5cee3;font-size:1rem;max-width:760px;margin:0; }

    .hero-chips { display:flex;flex-wrap:wrap;gap:8px;margin-top:1.2rem; }

    .chip { border:1px solid rgba(203,213,225,.17);background:rgba(255,255,255,.045);padding:6px 10px;border-radius:999px;color:#dbeafe;font-size:.75rem; }

    .section-head { display:flex;align-items:center;justify-content:space-between;gap:1rem;margin:1.5rem 0 .7rem; }

    .section-head h2 { font-size:1.15rem;margin:0; }

    .section-note { color:var(--muted);font-size:.8rem; }

    .metric-card { padding:1rem 1.1rem;min-height:105px;border-radius:17px;border:1px solid var(--line);

      background:linear-gradient(145deg,rgba(24,30,48,.94),rgba(15,19,31,.94)); }

    .metric-label { color:#9ba5bd;font-size:.76rem;font-weight:700;margin-bottom:.55rem; }

    .metric-value { color:#f8fafc;font-size:1.65rem;font-weight:800;letter-spacing:-.05em; }

    .metric-sub { color:#8b95ad;font-size:.72rem;margin-top:.25rem; }

    .surface { border:1px solid var(--line);background:linear-gradient(145deg,rgba(20,25,40,.96),rgba(14,17,28,.96));

      border-radius:20px;padding:1.2rem 1.35rem;margin:.35rem 0 .8rem; }

    .surface-title { font-size:.92rem;font-weight:800;color:#f1f5f9;margin-bottom:.6rem; }

    .muted { color:#9ba5bd; }

    .mono { font-family:'DM Mono',monospace;font-size:.78rem; }

    .status-dot { display:inline-block;width:7px;height:7px;border-radius:100%;background:#34d399;margin-right:7px;box-shadow:0 0 10px #34d39955; }

    .empty-state { border:1px dashed rgba(167,139,250,.28);border-radius:22px;padding:2.4rem 1.2rem;text-align:center;background:rgba(17,21,34,.5); }

    .empty-icon { font-size:2.4rem;margin-bottom:.5rem; }

    .empty-title { font-size:1.15rem;font-weight:800;color:#f8fafc; }

    .empty-copy { color:#9ba5bd;max-width:600px;margin:.4rem auto 0;font-size:.9rem; }

    .stTextInput input,.stTextArea textarea { background:#0d111d!important;color:#f8fafc!important;border-color:#30374c!important;border-radius:12px!important; }

    .stSelectbox [data-baseweb="select"]>div { background:#0d111d;border-color:#30374c;border-radius:12px; }

    .stButton>button,.stDownloadButton>button { border-radius:12px;min-height:2.7rem;font-weight:800;border:1px solid rgba(167,139,250,.35);transition:all .15s ease; }

    .stButton>button[kind="primary"] { background:linear-gradient(100deg,#8b5cf6,#6366f1);color:white;border:0; }

    .stButton>button:hover,.stDownloadButton>button:hover { border-color:#67e8f9;transform:translateY(-1px); }

    [data-testid="stTabs"] button { font-weight:700; }

    [data-testid="stMetric"] { background:#111522;border:1px solid var(--line);padding:1rem;border-radius:16px; }

    [data-testid="stMetricLabel"] { color:#9ba5bd; }

    [data-testid="stMetricValue"] { color:#f8fafc; }

    .stAlert { border-radius:14px; }

    hr { border-color:var(--line); }

    footer { visibility:hidden; }

    </style>

    """,

    unsafe_allow_html=True,

)

for key, default in {

    "video_result": None,

    "chat_history": [],

    "last_source": "",

    "last_language": "english",

}.items():

    if key not in st.session_state:

        st.session_state[key] = default

def process_video(source: str, language: str) -> dict[str, Any]:

    """Use the project's existing modules; do not duplicate backend logic."""

    from utils.audio_processor import process_input

    from core.transcriber import transcribe_all

    from core.summarizer import summarize, generate_title

    from core.extractor import (

        extract_action_items,

        extract_key_decisions,

        extract_questions,

    )

    from core.rag_engine import build_rag_chain

    chunks = process_input(source)

    transcript = transcribe_all(chunks, language)

    if not transcript or not transcript.strip():

        raise RuntimeError("Transcription returned no text. Check the source, language, and logs.")

    title = generate_title(transcript)

    summary = summarize(transcript)

    action_items = extract_action_items(transcript)

    decisions = extract_key_decisions(transcript)

    questions = extract_questions(transcript)

    rag_chain = build_rag_chain(transcript)

    return {

        "source": source,

        "language": language,

        "title": title or "Untitled video",

        "transcript": transcript,

        "summary": summary or "",

        "action_items": action_items or "",

        "key_decisions": decisions or "",

        "open_questions": questions or "",

        "rag_chain": rag_chain,

        "created_at": datetime.now().strftime("%d %b %Y, %I:%M %p"),

    }

def make_report(result: dict[str, Any]) -> str:

    return f"""# {result.get('title', 'Video report')}

\- **Source:** {result.get('source', '')}

\- **Language:** {result.get('language', '')}

\- **Processed:** {result.get('created_at', '')}

## Summary

{result.get('summary', '')}

## Action items

{result.get('action_items', '')}

## Key decisions

{result.get('key_decisions', '')}

## Open questions

{result.get('open_questions', '')}

## Transcript

{result.get('transcript', '')}

"""

def safe_filename(text: str) -> str:

    text = re.sub(r"[^\w -]+", "", text, flags=re.UNICODE).strip().lower()

    return re.sub(r"[\s-]+", "_", text)[:70] or "video_report"

def sentence_estimate(text: str) -> int:

    return len([part for part in re.split(r"[.!?।]+\s*", text.strip()) if part.strip()])

with st.sidebar:

    render_html(

        """<div class="brand-row"><div class="brand-mark">▶</div><div>

        <div class="brand-name">Video Intelligence</div><div class="brand-sub">Local AI workspace</div>

        </div></div>""",

    )

    st.markdown("### Workspace")

    language_label = st.selectbox(

        "Transcription language",

        ["English · Whisper", "Hindi · Sarvam AI"],

        index=0 if st.session_state.last_language == "english" else 1,

        help="Choose the language supported by your current transcriber.",

    )

    language = "english" if language_label.startswith("English") else "hindi"

    st.markdown("---")

    st.markdown("### Your local stack")

    render_html(

        """<div class="surface" style="padding:.9rem 1rem">

        <div><span class="status-dot"></span><b>Pipeline modules</b></div>

        <div class="muted" style="font-size:.78rem;margin-top:.4rem">Audio · Transcription · Summary · RAG</div>

        <div class="mono muted" style="margin-top:.8rem">LLM: Ollama / Qwen</div></div>""",

    )

    st.caption("Uses your existing Python modules.")

    st.caption("Long videos may take several minutes.")

    if st.session_state.video_result and st.button("↻ Start a fresh session", use_container_width=True):

        st.session_state.video_result = None

        st.session_state.chat_history = []

        st.session_state.last_source = ""

        st.rerun()

render_html(

    """<div class="hero"><div class="eyebrow">AI-powered video understanding</div>

    <h1>From video to<br>usable knowledge.</h1>

    <p>Transform a YouTube video or local recording into a clear brief, searchable transcript,

    action items, key decisions, and a chat grounded in the content.</p>

    <div class="hero-chips"><span class="chip">✦ Local LLM workflow</span>

    <span class="chip">⌕ Transcript Q&amp;A</span><span class="chip">↧ Exportable report</span></div></div>""",

)

st.markdown(

    '<div class="section-head"><h2>01 / Ingest a source</h2><span class="section-note">YouTube URL or local media path</span></div>',

    unsafe_allow_html=True,

)

with st.container(border=True):

    source_col, action_col = st.columns([5, 1.5], vertical_alignment="bottom")

    with source_col:

        source = st.text_input(

            "Video source",

            value=st.session_state.last_source,

            placeholder="Paste a YouTube URL or enter a local audio/video file path…",

            label_visibility="collapsed",

            help="Passed directly to utils.audio_processor.process_input().",

        )

    with action_col:

        process_clicked = st.button("✦  Analyze video", type="primary", use_container_width=True)

    c1, c2, c3 = st.columns(3)

    c1.markdown("**01 · Extract**  \n<span class='muted'>Prepare audio and chunks</span>", unsafe_allow_html=True)

    c2.markdown("**02 · Understand**  \n<span class='muted'>Transcribe and summarize</span>", unsafe_allow_html=True)

    c3.markdown("**03 · Explore**  \n<span class='muted'>Ask questions with RAG</span>", unsafe_allow_html=True)

if process_clicked:
    if not source.strip():
        st.warning("Add a YouTube URL or local media path before starting.")
    else:
        st.session_state.last_source = source.strip()
        st.session_state.last_language = language
        st.session_state.chat_history = []

        progress_box = st.container(border=True)
        with progress_box:
            st.markdown("### ✦ Analyzing your video")
            progress_label = st.empty()
            progress_bar = st.progress(1)
            progress_percent = st.empty()

        try:
            start_time = time.time()
            percent = 1

            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(process_video, source.strip(), language)

                while not future.done():
                    if percent < 25:
                        percent += 1
                    elif percent < 60:
                        percent += 2
                    else:
                        percent += 3

                    # This is estimated progress, not a measured pipeline percentage.
                    percent = min(percent, 94)
                    elapsed = int(time.time() - start_time)
                    minutes, seconds = divmod(elapsed, 60)

                    if percent < 25:
                        stage = "Preparing audio and splitting it into chunks…"
                    elif percent < 60:
                        stage = "Transcribing and understanding the content…"
                    elif percent < 85:
                        stage = "Generating summary and extracting insights…"
                    else:
                        stage = "Finishing the report and preparing video Q&A…"

                    progress_label.markdown(
                        f"**{stage}**  \\nElapsed time: {minutes:02d}:{seconds:02d}"
                    )
                    progress_bar.progress(percent)
                    progress_percent.markdown(f"**{percent}%**")
                    time.sleep(0.35)

                result = future.result()

            st.session_state.video_result = result
            progress_bar.progress(100)
            elapsed = int(time.time() - start_time)
            minutes, seconds = divmod(elapsed, 60)
            progress_label.markdown(
                f"**Analysis complete!**  \\nCompleted in {minutes:02d}:{seconds:02d}."
            )
            progress_percent.markdown("**100% complete**")
            st.success("Your report is ready.")

        except Exception as exc:
            st.session_state.video_result = None
            st.error("The pipeline stopped before completing. Detailed error:")
            st.exception(exc)

result = st.session_state.video_result

if not result:

    render_html(

        """<div class="empty-state"><div class="empty-icon">◈</div>

        <div class="empty-title">Your next video, understood.</div>

        <div class="empty-copy">Start an analysis above. Your summary, transcript, extracted insights,

        downloads, and transcript-grounded Q&amp;A will appear here when processing finishes.</div></div>""",

    )

    a, b, c = st.columns(3)

    with a:

        st.markdown('<div class="surface"><div class="surface-title">📝 Executive brief</div><div class="muted">Get the core ideas without replaying the whole video.</div></div>', unsafe_allow_html=True)

    with b:

        st.markdown('<div class="surface"><div class="surface-title">🎯 Structured insights</div><div class="muted">Review extracted action items, decisions, and questions.</div></div>', unsafe_allow_html=True)

    with c:

        st.markdown('<div class="surface"><div class="surface-title">💬 Ask the transcript</div><div class="muted">Ask questions and get answers from retrieved context.</div></div>', unsafe_allow_html=True)

    st.stop()

transcript = result.get("transcript", "")

word_count = len(transcript.split())

char_count = len(transcript)

sentences = sentence_estimate(transcript)

is_hindi = result.get("language") == "hindi"

language_name = "Hindi" if is_hindi else "English"

engine_name = "Sarvam AI" if is_hindi else "Whisper"

source_label = "YouTube" if re.search(r"(youtube\.com|youtu\.be)", result.get("source", ""), re.I) else "Local file / URL"

filename = safe_filename(result.get("title", "video_report"))

st.markdown(

    '<div class="section-head"><h2>02 / Intelligence report</h2><span class="section-note">Generated from your source</span></div>',

    unsafe_allow_html=True,

)

st.markdown(f"## {result.get('title') or 'Untitled video'}")

st.caption(f"Processed {result.get('created_at', '')} · {source_label}")

m1, m2, m3, m4 = st.columns(4)

with m1:

    st.markdown(f'<div class="metric-card"><div class="metric-label">TRANSCRIPT WORDS</div><div class="metric-value">{word_count:,}</div><div class="metric-sub">Recognized words</div></div>', unsafe_allow_html=True)

with m2:

    st.markdown(f'<div class="metric-card"><div class="metric-label">CHARACTERS</div><div class="metric-value">{char_count:,}</div><div class="metric-sub">Transcript length</div></div>', unsafe_allow_html=True)

with m3:

    st.markdown(f'<div class="metric-card"><div class="metric-label">SENTENCE ESTIMATE</div><div class="metric-value">{sentences:,}</div><div class="metric-sub">Approximate count</div></div>', unsafe_allow_html=True)

with m4:

    st.markdown(f'<div class="metric-card"><div class="metric-label">LANGUAGE</div><div class="metric-value" style="font-size:1.25rem">{language_name}</div><div class="metric-sub">{engine_name}</div></div>', unsafe_allow_html=True)

left, right = st.columns([1.1, .9], gap="large")

with left:

    st.markdown('<div class="section-head"><h2>Executive summary</h2><span class="section-note">Quick read</span></div>', unsafe_allow_html=True)

    with st.container(border=True):

        st.markdown(result.get("summary") or "_No summary was generated._")

with right:

    st.markdown('<div class="section-head"><h2>Source details</h2><span class="section-note">Session metadata</span></div>', unsafe_allow_html=True)

    with st.container(border=True):

        st.markdown("**Source**")

        st.code(result.get("source", ""), language=None)

        st.markdown("**Processing language**")

        st.write(f"{language_name} · {engine_name}")

        st.markdown("**Processed at**")

        st.write(result.get("created_at", "—"))

st.markdown(

    '<div class="section-head"><h2>03 / Export</h2><span class="section-note">Take your results with you</span></div>',

    unsafe_allow_html=True,

)

e1, e2, e3 = st.columns([1, 1, 2])

with e1:

    st.download_button("↧ Download full report", data=make_report(result), file_name=f"{filename}_report.md", mime="text/markdown", use_container_width=True)

with e2:

    st.download_button("↧ Download transcript", data=transcript, file_name=f"{filename}_transcript.txt", mime="text/plain", use_container_width=True)

with e3:

    st.caption("The Markdown report includes summary, extracted insights, metadata, and the full transcript.")

st.markdown(

    '<div class="section-head"><h2>04 / Explore the content</h2><span class="section-note">Switch between report views</span></div>',

    unsafe_allow_html=True,

)

tab_summary, tab_transcript, tab_actions, tab_decisions, tab_questions = st.tabs(
    ["✦ Summary", "▤ Transcript", "✓ Action items", "◆ Decisions", "? Open questions"]
)

with tab_summary:

    st.markdown("### Key takeaways")

    st.markdown(result.get("summary") or "_No summary available._")

    st.caption("AI-generated summary. Verify critical facts against the original source.")

with tab_transcript:

    query = st.text_input("Find text in transcript", key="transcript_search", placeholder="Search names, terms, or phrases…")

    if query.strip():

        matches = [(i, line) for i, line in enumerate(transcript.splitlines(), start=1) if query.casefold() in line.casefold()]

        if matches:

            st.success(f"Found {len(matches)} matching line(s).")

            for line_no, line in matches[:100]:

                st.markdown(f"**Line {line_no}** · {line}")

        else:

            st.info("No matching lines found.")

    st.text_area("Full transcript", value=transcript, height=430, key="transcript_view")

    st.download_button("Download plain-text transcript", data=transcript, file_name=f"{filename}_transcript.txt", mime="text/plain", key="download_transcript_tab")

with tab_actions:

    st.markdown("### Action items")

    st.markdown(result.get("action_items") or "_No action items were identified._")

    st.caption("Model-extracted suggestions; verify before treating them as assigned tasks.")

with tab_decisions:

    st.markdown("### Key decisions")

    st.markdown(result.get("key_decisions") or "_No key decisions were identified._")

with tab_questions:

    st.markdown("### Open questions")

    st.markdown(result.get("open_questions") or "_No open questions were identified._")

st.markdown("---")
st.markdown(
    """
    <div class="section-head">
        <h2>05 / Ask Your Video</h2>
        <span class="section-note">AI-powered transcript Q&amp;A</span>
    </div>
    <div class="surface">
        <div class="surface-title">💬 Have a question about this video?</div>
        <div class="muted">
            Ask about key concepts, examples, decisions, or specific details.
            Answers use your existing transcript-grounded RAG pipeline.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

quick_questions = [
    "What are the main takeaways?",
    "Explain the most important concepts.",
    "What examples were mentioned?",
]
qcols = st.columns(3)
for idx, quick_question in enumerate(quick_questions):
    with qcols[idx]:
        if st.button(
            quick_question,
            key=f"quick_q_{idx}",
            use_container_width=True,
        ):
            st.session_state.pending_question = quick_question

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_question = st.chat_input("Ask anything about this video…")
if st.session_state.get("pending_question"):
    user_question = st.session_state.pop("pending_question")

if user_question and user_question.strip():
    question = user_question.strip()
    st.session_state.chat_history.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.markdown(question)

    try:
        with st.chat_message("assistant"):
            with st.spinner("Searching the transcript and preparing your answer…"):
                from core.rag_engine import ask_question
                answer = ask_question(result["rag_chain"], question)
            st.markdown(answer)

        st.session_state.chat_history.append(
            {"role": "assistant", "content": answer}
        )
    except Exception as exc:
        if (
            st.session_state.chat_history
            and st.session_state.chat_history[-1]["role"] == "user"
            and st.session_state.chat_history[-1]["content"] == question
        ):
            st.session_state.chat_history.pop()
        st.error("Could not answer this question. Check your RAG/vector-store configuration.")
        st.exception(exc)

st.markdown("---")

st.markdown(

    """<div style="display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;color:#77819a;font-size:.75rem">

    <span>VIDEO INTELLIGENCE STUDIO · Existing Python pipeline</span>

    <span>Review generated content before relying on important details.</span></div>""",

    unsafe_allow_html=True,

)
