import streamlit as st
from utils.api import ask_question

def render_chat():
    st.markdown("""
        <style>
        .chat-container {
            padding: 1rem;
            max-width: 100%;
        }

        .bubble {
            padding: 1rem 1.2rem;
            margin-bottom: 0.7rem;
            border-radius: 18px;
            max-width: 80%;
            font-size: 0.95rem;
            line-height: 1.5;
        }

        .user-bubble {
            background: linear-gradient(135deg, #007bff, #00c6ff);
            color: white;
            align-self: flex-end;
            margin-left: auto;
        }

        .bot-bubble {
            background: #f0f2f5;
            color: #111;
            align-self: flex-start;
            margin-right: auto;
            border: 1px solid #ddd;
        }

        .chat-row {
            display: flex;
            flex-direction: row;
            margin-bottom: 0.5rem;
        }

        .avatar {
            font-size: 1.4rem;
            margin-right: 0.6rem;
            margin-top: 0.1rem;
        }

        .user-avatar {
            color: #007bff;
        }

        .bot-avatar {
            color: #444;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("## 🤖 Docscribe Assistant", unsafe_allow_html=True)
    st.markdown("Ask questions based on your uploaded PDFs. The AI answers only from those documents.", unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.container():
        for msg in st.session_state.messages:
            role = msg["role"]
            content = msg["content"]
            if role == "user":
                st.markdown(f"""
                <div class="chat-row">
                    <div class="bubble user-bubble">{content}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-row">
                    <div class="avatar bot-avatar">🤖</div>
                    <div class="bubble bot-bubble">{content}</div>
                </div>
                """, unsafe_allow_html=True)

    user_input = st.chat_input("Ask a question...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        st.markdown(f"""
            <div class="chat-row">
                <div class="bubble user-bubble">{user_input}</div>
            </div>
        """, unsafe_allow_html=True)

        with st.spinner("🧠 Thinking..."):
            response = ask_question(user_input)

        if response.status_code == 200:
            data = response.json()
            answer = data["response"]
            sources = data.get("sources", [])
            st.session_state.messages.append({"role": "assistant", "content": answer})

            st.markdown(f"""
                <div class="chat-row">
                    <div class="avatar bot-avatar">🤖</div>
                    <div class="bubble bot-bubble">{answer}</div>
                </div>
            """, unsafe_allow_html=True)

            if sources:
                with st.expander("📚 Sources"):
                    for src in sources:
                        st.markdown(f"- `{src}`")
        else:
            st.error("⚠️ Failed to get a response from the AI.")
