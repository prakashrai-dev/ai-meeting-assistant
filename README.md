# 🎙️ AI Meeting Assistant

AI-powered Meeting Assistant that transcribes meetings/videos, generates summaries, extracts action items, and allows users to chat with transcripts using RAG (Retrieval-Augmented Generation).

---

## 🚀 Features

- 🎥 YouTube Video Transcription
- 📂 Audio/Video Upload Support
- 🧠 AI-Powered Meeting Summaries
- ✅ Action Item Extraction
- 🔑 Key Decision Extraction
- ❓ Open Question Detection
- 💬 Chat with Transcript using RAG
- 📄 Transcript & Summary Download
- 🌐 English + Hinglish Support

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend / AI
- Python
- LangChain
- Mistral AI
- Whisper
- ChromaDB
- HuggingFace Embeddings

---

## 📸 Screenshots

### Home Page
(Add screenshot here later)

### Summary Output
(Add screenshot here later)

### RAG Chat
(Add screenshot here later)

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/prakashrai-dev/ai-meeting-assistant.git
cd ai-meeting-assistant
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate Virtual Environment

#### Windows

```bash
.venv\Scripts\activate
```

#### Mac/Linux

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in root directory:

```env
MISTRAL_API_KEY=your_api_key_here
```

---

## ▶️ Run Application

```bash
streamlit run app.py
```

---

## 📂 Project Structure

```bash
ai-meeting-assistant/
│
├── core/
│   ├── extractor.py
│   ├── rag_engine.py
│   ├── summarize.py
│   ├── transcriber.py
│   └── vector_store.py
│
├── utils/
│   └── audio_pro.py
│
├── app.py
├── main.py
├── requirements.txt
└── README.md
```

---

## 🧠 How It Works

1. User uploads file or pastes YouTube URL
2. Audio gets processed and chunked
3. Whisper transcribes audio
4. LLM generates:
   - Summary
   - Action Items
   - Key Decisions
   - Open Questions
5. Transcript embeddings stored in ChromaDB
6. User chats with transcript using RAG pipeline

---

## 🎯 Future Improvements

- Speaker Identification
- PDF Export
- Real-time Meeting Processing
- Improved UI/UX

---

## 👨‍💻 Author

Prakash Rai

GitHub:
https://github.com/prakashrai-dev
