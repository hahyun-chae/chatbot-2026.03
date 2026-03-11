import streamlit as st
from openai import OpenAI

# ── 시스템 프롬프트 ───────────────────────────────────────────────
SYSTEM_PROMPT = """
당신은 기획/PM, 프로덕트 디자인, UX/UI 디자인 분야의 취준생을 돕는 친근하고 따뜻한 AI 커리어 코치입니다.

## 인사 감지 & 데일리 체커 규칙

### STEP 1 — 인사 감지
사용자 메시지에 인사말이 포함되어 있으면 (예: 안녕, 안녕하세요, 하이, hi, hello, ㅎㅇ, 좋은 아침, 오늘도, 화이팅 등)
반드시 아래 두 가지를 모두 해야 합니다:
1. 반갑게 인사 응대
2. "오늘은 어떤 작업을 하셨나요? 포트폴리오 작업, 공부, 지원서 작성 등 무엇이든 좋아요 😊" 라고 질문

절대로 인사에 그냥 답변만 하고 끝내지 마세요. 반드시 오늘 한 작업을 물어봐야 합니다.

### STEP 2 — 작업 내용 청취 후 응답
사용자가 오늘 한 작업/공부 내용을 말하면, 반드시 아래 세 가지를 순서대로 모두 답변하세요.

1. 🎉 **칭찬**
   오늘 한 작업에 대해 구체적이고 진심 어린 칭찬을 1~2문장으로 해주세요.

2. 💡 **피드백**
   오늘 한 작업을 더 잘 활용하거나 보완할 수 있는 실용적인 팁을 1~2문장으로 주세요.

3. 📋 **다음 할 일 추천 3가지**
   오늘 작업과 연결되는 다음 단계 할 일을 3가지 bullet로 추천해 주세요.
   - 난이도/우선순위를 고려해 쉬운 것부터 순서를 잡아주세요.
   - 각 항목은 구체적이고 실행 가능한 액션으로 작성하세요.

마지막에는 "추천 할 일 중 같이 해볼 것이 있으면 말씀해 주세요 😊" 라고 마무리하세요.

## 평소 응답 규칙
- 인사/체커 흐름이 아닌 일반 질문에는 기획·디자인·취업 관련 전문 지식으로 친절하게 답변하세요.
- 항상 한국어로 답변하세요.
- 이모지를 적절히 활용해 친근한 톤을 유지하세요.
""".strip()

# ── 커스텀 CSS ────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Gmarket+Sans&display=swap');

/* 전체 배경 */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f0f4ff 0%, #faf5ff 50%, #fff0f6 100%);
    font-family: 'Plus Jakarta Sans', sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

/* 메인 컨테이너 */
[data-testid="stMainBlockContainer"] {
    max-width: 820px;
    padding-top: 2rem;
}

/* 타이틀 */
h1 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 2rem !important;
    background: linear-gradient(135deg, #6366f1, #a855f7, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.5px;
}

/* 서브 텍스트 */
[data-testid="stMarkdownContainer"] p {
    font-size: 0.9rem;
    color: #6b7280;
    line-height: 1.6;
}

/* API 키 입력창 */
[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.8) !important;
    border: 1.5px solid #e0e7ff !important;
    border-radius: 12px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.9rem !important;
    color: #374151 !important;
    padding: 0.6rem 1rem !important;
    box-shadow: 0 2px 8px rgba(99,102,241,0.08) !important;
    transition: border-color 0.2s !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
}

/* 추천 질문 카테고리 레이블 */
.category-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #9ca3af;
    margin-bottom: 6px;
    margin-top: 12px;
}

/* 추천 질문 버튼 */
[data-testid="stButton"] button {
    background: rgba(255,255,255,0.85) !important;
    border: 1.5px solid #e5e7eb !important;
    border-radius: 10px !important;
    color: #374151 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    padding: 0.45rem 0.6rem !important;
    line-height: 1.4 !important;
    white-space: normal !important;
    word-break: keep-all !important;
    height: auto !important;
    min-height: 48px !important;
    transition: all 0.18s ease !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
    backdrop-filter: blur(8px) !important;
}
[data-testid="stButton"] button:hover {
    background: linear-gradient(135deg, #eef2ff, #faf5ff) !important;
    border-color: #a5b4fc !important;
    color: #4f46e5 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(99,102,241,0.15) !important;
}

/* 구분선 */
hr {
    border: none !important;
    border-top: 1px solid #e5e7eb !important;
    margin: 1.2rem 0 !important;
}

/* 채팅 메시지 */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.75) !important;
    border-radius: 16px !important;
    border: 1px solid rgba(229,231,235,0.6) !important;
    padding: 0.8rem 1rem !important;
    margin-bottom: 0.5rem !important;
    backdrop-filter: blur(10px) !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
}

/* 유저 메시지 */
[data-testid="stChatMessage"][data-testid*="user"] {
    background: linear-gradient(135deg, rgba(238,242,255,0.9), rgba(250,245,255,0.9)) !important;
    border-color: rgba(165,180,252,0.4) !important;
}

/* 채팅 입력창 */
[data-testid="stChatInput"] textarea {
    background: rgba(255,255,255,0.9) !important;
    border: 1.5px solid #e0e7ff !important;
    border-radius: 14px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.9rem !important;
    color: #374151 !important;
    box-shadow: 0 2px 12px rgba(99,102,241,0.1) !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: #818cf8 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12), 0 2px 12px rgba(99,102,241,0.1) !important;
}

/* 섹션 헤더 */
.section-header {
    font-size: 0.8rem;
    font-weight: 700;
    color: #6366f1;
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 10px;
}

/* info 박스 */
[data-testid="stAlert"] {
    background: rgba(238,242,255,0.8) !important;
    border: 1px solid #c7d2fe !important;
    border-radius: 12px !important;
    color: #4338ca !important;
}
</style>
""", unsafe_allow_html=True)

# ── 헤더 ─────────────────────────────────────────────────────────
st.title("✦ 커리어 챗봇")
st.markdown("기획/PM · 프로덕트 디자인 · UX/UI 취준생을 위한 AI 커리어 코치예요.<br>인사하면 오늘 작업을 체크하고 **칭찬 · 피드백 · 다음 할 일**을 추천해드려요 🎉", unsafe_allow_html=True)

st.divider()

# ── API 키 입력 ───────────────────────────────────────────────────
openai_api_key = st.text_input("🔑 OpenAI API Key", type="password", placeholder="sk-...")
if not openai_api_key:
    st.info("OpenAI API 키를 입력하면 시작할 수 있어요.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "suggested_input" not in st.session_state:
        st.session_state.suggested_input = ""

    # ── 대화 기록 표시 ────────────────────────────────────────────
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ── 추천 질문 ─────────────────────────────────────────────────
    suggested_questions = {
        "👋 데일리 체크인": [
            "안녕하세요! 👋",
            "오늘도 화이팅! 💪",
        ],
        "📄 기획 / PM": [
            "PM 신입 포트폴리오 필수 항목은?",
            "PRD 작성법 알려주세요",
            "PM 면접 자주 나오는 질문은?",
            "사용자 리서치 방법 종류는?",
        ],
        "🎨 프로덕트 / UX·UI 디자인": [
            "케이스 스터디 구성법은?",
            "Figma 프로토타입 기초는?",
            "디자인 시스템이란?",
            "사용성 테스트 시작하는 법은?",
        ],
        "🚀 취업 준비": [
            "자소서 핵심 포인트는?",
            "비전공자도 PM·UX 가능한가요?",
            "포트폴리오 없이 인턴 지원하는 법은?",
        ],
    }

    st.markdown('<div class="section-header">💡 추천 질문</div>', unsafe_allow_html=True)
    for category, questions in suggested_questions.items():
        st.markdown(f'<div class="category-label">{category}</div>', unsafe_allow_html=True)
        cols = st.columns(len(questions))
        for i, question in enumerate(questions):
            if cols[i].button(question, key=f"{category}_{i}", use_container_width=True):
                st.session_state.suggested_input = question

    st.divider()

    # ── 입력 처리 ─────────────────────────────────────────────────
    prompt = None
    if st.session_state.suggested_input:
        prompt = st.session_state.suggested_input
        st.session_state.suggested_input = ""

    chat_input = st.chat_input("메시지를 입력하세요...")
    if chat_input:
        prompt = chat_input

    # ── 응답 생성 ─────────────────────────────────────────────────
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 인사 키워드 사전 감지 → 시스템 프롬프트 강화
        greeting_keywords = ["안녕", "하이", "hi", "hello", "ㅎㅇ", "좋은 아침", "좋은 저녁", "오늘도", "화이팅", "반가"]
        is_greeting = any(kw in prompt.lower() for kw in greeting_keywords)

        extra_instruction = ""
        if is_greeting:
            extra_instruction = "\n\n[중요 지시] 지금 사용자가 인사를 했습니다. 반드시 인사에 답하고, 오늘 어떤 작업을 했는지 물어봐야 합니다. 이 단계를 절대 생략하지 마세요."

        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT + extra_instruction},
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            ],
            stream=True,
        )

        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})