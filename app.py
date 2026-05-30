import streamlit as st
import tempfile
import os

from main import run_pipeline
from core.rag_engine import ask_question

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AI Meeting Assistant",
    page_icon="🎙️",
    layout="wide"
)

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

h1, h2, h3 {
    color: white;
}

.stTextInput > div > div > input {
    border-radius: 12px;
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 3em;
    font-weight: bold;
}

.card {
    background-color: #161B22;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #30363D;
    margin-bottom: 20px;
}

.chat-user {
    background-color: #1F6FEB;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
    color: white;
}

.chat-bot {
    background-color: #262730;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 20px;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ---------------- #

if "result" not in st.session_state:
    st.session_state.result = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- HEADER ---------------- #

st.title("🎙️ AI Meeting Assistant")

st.caption(
    "Summarize meetings, extract action items, and chat with transcripts using AI."
)

# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.header("⚙️ Settings")

    language = st.selectbox(
        "Language",
        ["english", "hinglish"]
    )

    st.markdown("---")

    st.markdown(
        """
        ### 🚀 Features
        
        - YouTube Transcription
        - Multilingual Support
        - AI Summaries
        - Action Items
        - RAG Chat
        - Transcript Export
        """
    )

# ---------------- INPUT AREA ---------------- #

st.markdown("## 📥 Input Source")

col1, col2 = st.columns([1, 1])

source = None

with col1:

    source_type = st.radio(
        "Choose Input Type",
        ["YouTube URL", "Upload File"]
    )

with col2:

    if source_type == "YouTube URL":

        source = st.text_input(
            "Paste YouTube URL"
        )

    else:

        uploaded_file = st.file_uploader(
            "Upload audio/video file",
            type=["mp3", "wav", "mp4", "m4a"]
        )

        if uploaded_file is not None:

            temp_dir = tempfile.mkdtemp()

            temp_path = os.path.join(temp_dir, uploaded_file.name)

            with open(temp_path, "wb") as f:
                f.write(uploaded_file.read())

            source = temp_path

# ---------------- PROCESS BUTTON ---------------- #

if st.button("🚀 Process Meeting"):

    if not source:

        st.warning("Please provide a valid input source.")


else:

    with st.spinner("Processing meeting with AI..."):

        try:

            st.session_state.result = run_pipeline(
                source,
                language
            )

            st.success("Meeting Processed Successfully ✅")

        except Exception as e:

            st.error(
                "⚠️ Failed to process YouTube link.\n\n"
                "YouTube sometimes blocks cloud requests.\n\n"
                "Please try:\n"
                "- another video\n"
                "- a shorter video\n"
                "- or upload the file directly."
            )

            st.stop()




# ---------------- RESULTS ---------------- #

if st.session_state.result:

    result = st.session_state.result

    st.markdown("---")

    # ---------------- TITLE ---------------- #

    st.markdown(
        f"""
        <div class="card">
            <h2>📌 {result['title']}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------- GRID SECTION ---------------- #

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            <div class="card">
                <h3>📋 Summary</h3>
                <p>{result['summary']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="card">
                <h3>✅ Action Items</h3>
                <p>{result['action_items']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="card">
                <h3>🔑 Key Decisions</h3>
                <p>{result['key_decisions']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="card">
                <h3>❓ Open Questions</h3>
                <div style="white-space: pre-line;">
                {result['open_questions']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---------------- TRANSCRIPT ---------------- #

    with st.expander("📝 View Full Transcript"):

        st.text_area(
            "Transcript",
            result["transcript"],
            height=400
        )

    # ---------------- DOWNLOADS ---------------- #

    st.markdown("## ⬇️ Export Results")

    d1, d2 = st.columns(2)

    with d1:

        st.download_button(
            label="📄 Download Transcript",
            data=result["transcript"],
            file_name="transcript.txt",
            mime="text/plain"
        )

    with d2:

        st.download_button(
            label="📄 Download Summary",
            data=result["summary"],
            file_name="summary.txt",
            mime="text/plain"
        )

    # ---------------- CHAT SECTION ---------------- #

    st.markdown("---")

    st.markdown("## 💬 Chat With Your Meeting")

    user_question = st.text_input(
        "Ask something about the meeting"
    )

    if st.button("Ask AI"):

        if user_question.strip():

            with st.spinner("Thinking..."):

                answer = ask_question(
                    result["rag_chain"],
                    user_question
                )

            st.session_state.chat_history.append(
                {
                    "question": user_question,
                    "answer": answer
                }
            )

    # ---------------- CHAT HISTORY ---------------- #

    for chat in st.session_state.chat_history:

        st.markdown(
            f"""
            <div class="chat-user">
                <strong>🧑 You:</strong><br>
                {chat['question']}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="chat-bot">
                <strong>🤖 Assistant:</strong><br>
                {chat['answer']}
            </div>
            """,
            unsafe_allow_html=True
        )

# import streamlit as st
# import tempfile
# import os
# from dotenv import load_dotenv

# load_dotenv()

# st.set_page_config(
#     page_title="MeetingMind AI",
#     page_icon="🎙️",
#     layout="wide",
#     initial_sidebar_state="collapsed",
# )

# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

# html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
# .stApp { background: #0d0f12; color: #e8e6e0; }
# #MainMenu, footer, header { visibility: hidden; }
# .block-container { padding: 2rem 3rem 4rem; max-width: 1100px; }

# .hero-title {
#     font-family: 'DM Serif Display', serif;
#     font-size: 3.2rem; font-weight: 400; color: #f0ede6;
#     letter-spacing: -0.02em; line-height: 1.1; margin-bottom: 0.3rem;
# }
# .hero-sub {
#     font-size: 1rem; color: #7a7670; font-weight: 300;
#     margin-bottom: 2rem; letter-spacing: 0.01em;
# }

# /* Input card */
# .input-card {
#     background: #161a1f; border: 1px solid #2a2d33;
#     border-radius: 16px; padding: 1.5rem 2rem; margin-bottom: 1.5rem;
# }

# /* All text inputs / selects */
# .stTextInput > div > div > input,
# .stSelectbox > div > div > div {
#     background: #0d0f12 !important; border: 1px solid #2a2d33 !important;
#     border-radius: 10px !important; color: #e8e6e0 !important;
#     font-family: 'DM Sans', sans-serif !important; font-size: 0.95rem !important;
# }
# .stTextInput > div > div > input:focus {
#     border-color: #c4a882 !important;
#     box-shadow: 0 0 0 3px rgba(196,168,130,0.12) !important;
# }
# .stTextInput label, .stSelectbox label {
#     color: #9a9590 !important; font-size: 0.78rem !important;
#     font-weight: 600 !important; letter-spacing: 0.07em !important;
#     text-transform: uppercase !important;
# }

# /* Hide the radio group label text only (not the options) */
# .stRadio > label {
#     display: none !important;
# }
# .stRadio div[role="radiogroup"] label {
#     color: #ccc9c3 !important; font-size: 0.9rem !important;
#     font-weight: 400 !important;
# }

# /* Buttons */
# div[data-testid="stButton"] > button {
#     background: #c4a882 !important; color: #0d0f12 !important;
#     border: none !important; border-radius: 10px !important;
#     font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important;
#     font-size: 0.88rem !important; padding: 0.6rem 1.6rem !important;
#     letter-spacing: 0.02em !important; transition: background 0.15s, transform 0.1s !important;
# }
# div[data-testid="stButton"] > button:hover {
#     background: #d4b892 !important; transform: translateY(-1px) !important;
# }

# /* Download buttons */
# div[data-testid="stDownloadButton"] > button {
#     background: transparent !important; color: #c4a882 !important;
#     border: 1px solid #3a3530 !important; border-radius: 10px !important;
#     font-family: 'DM Sans', sans-serif !important; font-size: 0.82rem !important;
#     font-weight: 500 !important; padding: 0.5rem 1.2rem !important; width: 100% !important;
# }
# div[data-testid="stDownloadButton"] > button:hover {
#     border-color: #c4a882 !important; background: rgba(196,168,130,0.06) !important;
# }

# /* Stats bar */
# .stats-bar {
#     display: flex; background: #161a1f; border: 1px solid #2a2d33;
#     border-radius: 14px; margin-bottom: 1.5rem; overflow: hidden;
# }
# .stat-item {
#     flex: 1; text-align: center; padding: 1.1rem 0.5rem;
#     border-right: 1px solid #2a2d33;
# }
# .stat-item:last-child { border-right: none; }
# .stat-value {
#     font-family: 'DM Serif Display', serif; font-size: 1.7rem;
#     color: #c4a882; font-weight: 400; line-height: 1;
# }
# .stat-label {
#     font-size: 0.68rem; font-weight: 600; letter-spacing: 0.09em;
#     text-transform: uppercase; color: #5a5650; margin-top: 4px;
# }

# /* Meeting title card */
# .title-card {
#     background: #161a1f; border: 1px solid #2a2d33;
#     border-left: 3px solid #c4a882; border-radius: 14px;
#     padding: 1.4rem 1.8rem; margin-bottom: 1.5rem;
# }
# .title-eyebrow {
#     font-size: 0.7rem; font-weight: 600; letter-spacing: 0.1em;
#     text-transform: uppercase; color: #c4a882; margin-bottom: 0.4rem;
# }
# .title-text {
#     font-family: 'DM Serif Display', serif; font-size: 1.55rem;
#     color: #f0ede6; font-weight: 400; line-height: 1.3;
# }

# /* Tabs */
# .stTabs [data-baseweb="tab-list"] {
#     background: transparent !important; border-bottom: 1px solid #2a2d33 !important; gap: 0 !important;
# }
# .stTabs [data-baseweb="tab"] {
#     background: transparent !important; color: #7a7670 !important;
#     border: none !important; font-family: 'DM Sans', sans-serif !important;
#     font-size: 0.83rem !important; font-weight: 500 !important;
#     padding: 0.55rem 1.3rem !important; letter-spacing: 0.04em !important;
# }
# .stTabs [aria-selected="true"] {
#     color: #c4a882 !important; border-bottom: 2px solid #c4a882 !important;
# }
# .stTabs [data-baseweb="tab-panel"] { padding-top: 1.2rem !important; }

# /* Expander */
# .stExpander {
#     background: #161a1f !important; border: 1px solid #2a2d33 !important;
#     border-radius: 14px !important;
# }
# .stExpander summary { color: #9a9590 !important; }

# /* Export label */
# .export-label {
#     font-size: 0.7rem; font-weight: 600; letter-spacing: 0.09em;
#     text-transform: uppercase; color: #5a5650; margin-bottom: 0.7rem;
# }

# /* Divider */
# .divider { border: none; border-top: 1px solid #2a2d33; margin: 2rem 0; }

# /* Chat */
# .chat-header {
#     font-family: 'DM Serif Display', serif; font-size: 1.45rem;
#     color: #f0ede6; margin-bottom: 1rem; font-weight: 400;
# }
# .user-bubble {
#     background: #1f2530; border: 1px solid #2a3040;
#     border-radius: 14px 14px 4px 14px; padding: 0.75rem 1.1rem;
#     margin: 0.5rem 0; font-size: 0.9rem; color: #c4c0ba;
#     max-width: 78%; margin-left: auto;
# }
# .assistant-bubble {
#     background: #161a1f; border: 1px solid #2a2d33;
#     border-radius: 14px 14px 14px 4px; padding: 0.75rem 1.1rem;
#     margin: 0.5rem 0; font-size: 0.9rem; color: #ccc9c3;
#     max-width: 85%; line-height: 1.75;
# }
# .bubble-role {
#     font-size: 0.65rem; font-weight: 600; letter-spacing: 0.09em;
#     text-transform: uppercase; color: #5a5650; margin-bottom: 0.25rem;
# }

# /* Empty state */
# .empty-state { text-align: center; padding: 5rem 2rem; }
# .empty-icon { font-size: 2.8rem; margin-bottom: 1rem; }
# .empty-title {
#     font-family: 'DM Serif Display', serif; font-size: 1.25rem;
#     color: #4a4840; margin-bottom: 0.4rem;
# }
# .empty-hint { font-size: 0.82rem; color: #3a3830; }
# </style>
# """, unsafe_allow_html=True)


# # ── Session state ─────────────────────────────────────────────────────────────
# for key, default in [("result", None), ("chat_history", [])]:
#     if key not in st.session_state:
#         st.session_state[key] = default


# # ── Hero ──────────────────────────────────────────────────────────────────────
# st.markdown('<div class="hero-title">MeetingMind</div>', unsafe_allow_html=True)
# st.markdown(
#     '<div class="hero-sub">Drop a recording or paste a URL — walk away with a full briefing.</div>',
#     unsafe_allow_html=True,
# )


# # ── Input card ────────────────────────────────────────────────────────────────
# st.markdown('<div class="input-card">', unsafe_allow_html=True)

# meta_col1, meta_col2 = st.columns([3, 1])

# with meta_col1:
#     # label="" so the empty string renders nothing — avoids the visible "Input type" heading
#     source_type = st.radio("", ["YouTube URL", "Upload File"], horizontal=True)

# with meta_col2:
#     language = st.selectbox("Language", ["english", "hinglish"])

# source = None

# if source_type == "YouTube URL":
#     source = st.text_input(
#         "url_field",
#         placeholder="https://www.youtube.com/watch?v=...",
#         label_visibility="collapsed",
#     )
# else:
#     uploaded_file = st.file_uploader(
#         "Upload audio or video",
#         type=["mp3", "wav", "mp4", "m4a", "webm"],
#         label_visibility="collapsed",
#     )
#     if uploaded_file:
#         tmp_dir = tempfile.mkdtemp()
#         tmp_path = os.path.join(tmp_dir, uploaded_file.name)
#         with open(tmp_path, "wb") as f:
#             f.write(uploaded_file.read())
#         source = tmp_path

# st.markdown("<br>", unsafe_allow_html=True)
# run_btn = st.button("Analyse meeting →")
# st.markdown("</div>", unsafe_allow_html=True)


# # ── Run pipeline ──────────────────────────────────────────────────────────────
# if run_btn:
#     if not source:
#         st.warning("Please provide a YouTube URL or upload a file first.")
#     else:
#         st.session_state.chat_history = []
#         st.session_state.result = None

#         # Remove stale cache so pipeline re-processes
#         for stale in ["transcript.txt", "vector_db"]:
#             if os.path.exists(stale):
#                 if os.path.isdir(stale):
#                     import shutil
#                     shutil.rmtree(stale)
#                 else:
#                     os.remove(stale)

#         with st.spinner("Transcribing and analysing — this may take a minute..."):
#             try:
#                 from main import run_pipeline
#                 st.session_state.result = run_pipeline(source, language)
#                 st.success("Done ✓")
#             except Exception as e:
#                 st.error(f"Pipeline error: {e}")


# # ── Helper: render text content safely ───────────────────────────────────────
# def render_content(text: str):
#     """
#     Use st.markdown instead of raw HTML so Streamlit handles
#     escaping and newlines correctly. Applies gold-tinted styling via CSS class.
#     """
#     if not text or not text.strip():
#         st.markdown(
#             "<p style='color:#5a5650;font-size:0.88rem;font-style:italic'>Nothing found.</p>",
#             unsafe_allow_html=True,
#         )
#         return
#     # Render as native markdown — preserves numbered lists, bullets, newlines
#     st.markdown(
#         f"<div style='color:#ccc9c3;font-size:0.93rem;line-height:1.8'>\n\n{text}\n\n</div>",
#         unsafe_allow_html=True,
#     )


# def count_lines(text: str) -> int:
#     return len([l for l in (text or "").split("\n") if l.strip()])


# # ── Results ───────────────────────────────────────────────────────────────────
# if st.session_state.result:
#     r = st.session_state.result
#     transcript = r.get("transcript", "")

#     words = len(transcript.split())
#     action_count  = count_lines(r.get("action_items", ""))
#     decision_count = count_lines(r.get("key_decisions", ""))
#     question_count = count_lines(r.get("open_questions", ""))

#     st.markdown(f"""
#     <div class="stats-bar">
#         <div class="stat-item"><div class="stat-value">{words:,}</div><div class="stat-label">Words</div></div>
#         <div class="stat-item"><div class="stat-value">{action_count}</div><div class="stat-label">Actions</div></div>
#         <div class="stat-item"><div class="stat-value">{decision_count}</div><div class="stat-label">Decisions</div></div>
#         <div class="stat-item"><div class="stat-value">{question_count}</div><div class="stat-label">Questions</div></div>
#     </div>
#     """, unsafe_allow_html=True)

#     st.markdown(f"""
#     <div class="title-card">
#         <div class="title-eyebrow">Meeting Title</div>
#         <div class="title-text">{r.get('title', 'Untitled Meeting')}</div>
#     </div>
#     """, unsafe_allow_html=True)

#     tab_summary, tab_actions, tab_decisions, tab_questions = st.tabs(
#         ["Summary", "Action Items", "Key Decisions", "Open Questions"]
#     )
#     with tab_summary:
#         render_content(r.get("summary"))
#     with tab_actions:
#         render_content(r.get("action_items"))
#     with tab_decisions:
#         render_content(r.get("key_decisions"))
#     with tab_questions:
#         render_content(r.get("open_questions"))

#     st.markdown("<br>", unsafe_allow_html=True)
#     with st.expander("📄 Full transcript"):
#         st.text_area("transcript_area", transcript, height=380, label_visibility="collapsed")

#     # Export
#     st.markdown("<br>", unsafe_allow_html=True)
#     st.markdown('<div class="export-label">Export</div>', unsafe_allow_html=True)

#     full_report = "\n\n".join([
#         f"MEETING TITLE\n{r.get('title','')}",
#         f"SUMMARY\n{r.get('summary','')}",
#         f"ACTION ITEMS\n{r.get('action_items','')}",
#         f"KEY DECISIONS\n{r.get('key_decisions','')}",
#         f"OPEN QUESTIONS\n{r.get('open_questions','')}",
#     ])

#     ec1, ec2, ec3 = st.columns(3)
#     with ec1:
#         st.download_button("⬇ Transcript", data=transcript, file_name="transcript.txt", mime="text/plain")
#     with ec2:
#         st.download_button("⬇ Summary", data=r.get("summary", ""), file_name="summary.txt", mime="text/plain")
#     with ec3:
#         st.download_button("⬇ Full Report", data=full_report, file_name="meeting_report.txt", mime="text/plain")

#     # Chat
#     st.markdown('<hr class="divider">', unsafe_allow_html=True)
#     st.markdown('<div class="chat-header">Ask anything about this meeting</div>', unsafe_allow_html=True)

#     for msg in st.session_state.chat_history:
#         if msg["role"] == "user":
#             st.markdown(f"""
#             <div style="display:flex;justify-content:flex-end;margin:0.4rem 0">
#                 <div class="user-bubble">
#                     <div class="bubble-role">You</div>{msg['content']}
#                 </div>
#             </div>""", unsafe_allow_html=True)
#         else:
#             st.markdown(f"""
#             <div style="display:flex;justify-content:flex-start;margin:0.4rem 0">
#                 <div class="assistant-bubble">
#                     <div class="bubble-role">MeetingMind</div>{msg['content']}
#                 </div>
#             </div>""", unsafe_allow_html=True)

#     with st.form("chat_form", clear_on_submit=True):
#         q_col, btn_col = st.columns([5, 1])
#         with q_col:
#             user_q = st.text_input(
#                 "q", placeholder="What were the main blockers discussed?",
#                 label_visibility="collapsed",
#             )
#         with btn_col:
#             send = st.form_submit_button("Send →", use_container_width=True)

#     st.markdown(
#         "<div style='font-size:0.78rem;color:#3a3830;margin-top:0.3rem'>"
#         "Ask about decisions, action owners, or request a follow-up email draft.</div>",
#         unsafe_allow_html=True,
#     )

#     if send and user_q.strip():
#         from core.rag_engine import ask_question
#         st.session_state.chat_history.append({"role": "user", "content": user_q})
#         with st.spinner("Thinking..."):
#             try:
#                 answer = ask_question(r["rag_chain"], user_q)
#             except Exception as e:
#                 answer = f"Error: {e}"
#         st.session_state.chat_history.append({"role": "assistant", "content": answer})
#         st.rerun()

# else:
#     st.markdown("""
#     <div class="empty-state">
#         <div class="empty-icon">🎙</div>
#         <div class="empty-title">Nothing analysed yet</div>
#         <div class="empty-hint">Paste a YouTube URL or upload a file above, then hit Analyse</div>
#     </div>
#     """, unsafe_allow_html=True)