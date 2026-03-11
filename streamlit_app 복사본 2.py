import streamlit as st
from openai import OpenAI

# ── 시스템 프롬프트 ───────────────────────────────────────────────
SYSTEM_PROMPT = """
당신은 기획/PM, 프로덕트 디자인, UX/UI 디자인 분야의 취준생을 돕는 친근하고 따뜻한 AI 커리어 코치입니다.

## 인사 감지 & 데일리 체커 규칙

### STEP 1 — 인사 감지
사용자가 인사말(안녕, 안녕하세요, 하이, hi, hello, ㅎㅇ, 좋은 아침 등)을 입력하면:
- 반갑게 인사한 뒤, 자연스럽게 아래 질문을 이어서 하세요.
  예: "안녕하세요! 반가워요 😊 오늘은 어떤 작업을 하셨나요? 포트폴리오, 공부, 지원서 작성 등 무엇이든 좋아요!"

### STEP 2 — 작업 내용 청취
사용자가 오늘 한 작업/공부 내용을 말하면, 아래 세 가지를 **순서대로** 답변하세요.

1. 🎉 **칭찬**: 오늘 한 작업에 대해 구체적이고 진심 어린 칭찬을 1~2문장으로 해주세요.
   예: "케이스 스터디 작성을 하셨군요! UX 포트폴리오의 핵심인 만큼 정말 알차게 시간을 쓰셨네요 💪"

2. 💡 **피드백**: 오늘 한 작업을 더 잘 활용하거나 보완할 수 있는 실용적인 팁을 1~2문장으로 주세요.
   예: "케이스 스터디에는 '문제 정의 → 리서치 → 솔루션 → 결과' 흐름을 명확히 드러내면 더욱 설득력 있어요."

3. 📋 **다음 할 일 추천**: 오늘 작업과 연결되는 다음 단계 할 일을 3가지 bullet로 추천해 주세요.
   - 난이도/우선순위를 고려해 쉬운 것부터 순서를 잡아주세요.
   - 각 항목은 구체적이고 실행 가능한 액션으로 작성해 주세요.
   예:
   - 📌 작성한 케이스 스터디에 Before/After 비교 이미지 추가하기
   - 📌 Behance나 Notion에 공개 포트폴리오 페이지로 정리해보기
   - 📌 비슷한 직군 합격자 포트폴리오 3개 참고해 구조 비교해보기

그 후 "오늘 추천 할 일 중 같이 해볼 것이 있으면 말씀해 주세요 😊" 라고 마무리하세요.

## 평소 응답 규칙
- 인사/체커 흐름이 아닌 일반 질문에는 기획·디자인·취업 관련 전문 지식으로 친절하게 답변하세요.
- 항상 한국어로 답변하세요.
- 이모지를 적절히 활용해 친근한 톤을 유지하세요.
""".strip()

# ── 페이지 설정 ───────────────────────────────────────────────────
st.set_page_config(page_title="커리어 챗봇", page_icon="💬")
st.title("💬 커리어 챗봇")
st.write("기획/PM · 프로덕트 디자인 · UX/UI 취준생을 위한 AI 커리어 코치예요. 인사하면 오늘 작업을 체크하고 칭찬 · 피드백 · 다음 할 일을 추천해드려요 🎉")

# ── API 키 입력 ───────────────────────────────────────────────────
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("OpenAI API 키를 입력해야 이용할 수 있어요.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # ── 세션 상태 초기화 ──────────────────────────────────────────
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
        "👋 데일리 체크": [
            "안녕하세요!",
            "오늘도 화이팅!",
        ],
        "📄 기획/PM": [
            "PM 신입 포트폴리오에 꼭 들어가야 할 항목은?",
            "PRD 작성하는 법을 알려주세요.",
            "PM 면접 자주 나오는 질문과 팁은?",
            "사용자 리서치 방법에는 어떤 것들이 있나요?",
        ],
        "🎨 프로덕트/UX·UI 디자인": [
            "UX 포트폴리오 케이스 스터디 구성법은?",
            "Figma 프로토타입 만드는 기초 과정은?",
            "디자인 시스템이란 무엇이고 왜 중요한가요?",
            "사용성 테스트, 처음에 어떻게 시작하나요?",
        ],
        "🚀 취업 준비": [
            "기획·디자인 직무 자소서 핵심 포인트는?",
            "비전공자도 PM·UX 디자이너로 취업 가능한가요?",
            "포트폴리오 없이 첫 인턴십 지원하는 방법은?",
        ],
    }

    st.markdown("**💡 추천 질문**")
    for category, questions in suggested_questions.items():
        st.markdown(f"<small style='color:gray;'>{category}</small>", unsafe_allow_html=True)
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

        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            ],
            stream=True,
        )

        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})