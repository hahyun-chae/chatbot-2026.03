import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Session state to hold a suggested question that was clicked
    if "suggested_input" not in st.session_state:
        st.session_state.suggested_input = ""

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- Suggested Questions (기획/PM · 프로덕트 디자인 · UX/UI 디자인 취준생 맞춤) ---
    suggested_questions = {
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

    # Use suggested input if a button was clicked, otherwise use chat_input
    if st.session_state.suggested_input:
        prompt = st.session_state.suggested_input
        st.session_state.suggested_input = ""
    else:
        prompt = None

    chat_input = st.chat_input("궁금한 것을 물어보세요!")
    if chat_input:
        prompt = chat_input

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})