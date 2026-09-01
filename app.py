import streamlit as st
from rag_pipeline import ask_hr_assistant

st.set_page_config(
    page_title="AI HR Policy Assistant",
    page_icon="🤖"
)

st.markdown("""
<style>
.user-message {
    display: flex;
    justify-content: flex-end;
    margin: 10px 0;
}

.user-bubble {
    background-color: #DCF8C6;
    color: black;
    padding: 10px 15px;
    border-radius: 15px;
    max-width: 70%;
}

.ai-message {
    display: flex;
    justify-content: flex-start;
    margin: 10px 0;
}

.ai-bubble {
    background-color: #F1F1F1;
    color: black;
    padding: 10px 15px;
    border-radius: 15px;
    max-width: 70%;
}
</style>
""", unsafe_allow_html=True)

st.title("🤖 AI HR Policy Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

st.write("Ask questions about the HR Employee Policy Handbook.")

for message in st.session_state.messages:

    if message["role"] == "user":
        st.markdown(
            f"""
            <div class="user-message">
                <div class="user-bubble">
                    👤 {message["content"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.markdown(
            f"""
            <div class="ai-message">
                <div class="ai-bubble">
                    🤖 {message["content"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

question = st.chat_input("Ask your HR policy question...")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    st.markdown(
    f"""
    <div class="user-message">
        <div class="user-bubble">
            👤 {question}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

    result = ask_hr_assistant(question)

    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"]
    })

    st.markdown(
    f"""
    <div class="ai-message">
        <div class="ai-bubble">
            🤖 {result["answer"]}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

    with st.expander("📚 Source & Retrieved Policy"):
        st.write(f"**Policy ID:** {result['policy_id']}")
        st.write(f"**Page:** {result['page']}")
        st.write(f"**Similarity Distance:** {result['distance']:.4f}")

        if result["policy_id"] is not None:
            st.write("### 📄 Retrieved Policy")
            st.write(result["context"])