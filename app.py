
"""
TRUJARVIS - AI for Everything
Main Streamlit Application
"""

import streamlit as st

from core.config import APP_NAME, APP_VERSION, MODEL_NAME
from core.llm_engine import LLMEngine


from database.db import (
    initialize_database,
    create_conversation,
    get_conversations,
    get_messages,
    save_message,
    delete_conversation,
    delete_all_conversations,
    update_conversation_title,
    rename_conversation,
)



# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title=f"{APP_NAME} | AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# 2. CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #0b0f19;
    color: #e5e7eb;
}

[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #263244;
}

.main-title {
    font-size: 34px;
    font-weight: 750;
    color: #60a5fa;
    letter-spacing: 1px;
}

.subtitle {
    color: #9ca3af;
    font-size: 14px;
}

[data-testid="stChatMessage"] {
    background-color: #151e2e;
    border: 1px solid #263244;
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 12px;
}

.stChatInput {
    border-color: #334155;
}

div.stButton > button {
    border-radius: 9px;
    border: 1px solid #334155;
}

div.stButton > button:hover {
    border-color: #60a5fa;
    color: #60a5fa;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 3. INITIALIZE DATABASE AND AI ENGINE
# --------------------------------------------------

initialize_database()

@st.cache_resource
def get_ai_engine():
    return LLMEngine()

engine = get_ai_engine()


# --------------------------------------------------
# 4. SESSION STATE
# --------------------------------------------------

if "active_chat_id" not in st.session_state:
    st.session_state.active_chat_id = None

if st.session_state.active_chat_id is None:
    conversations = get_conversations()

    if conversations:
        st.session_state.active_chat_id = conversations[0]["id"]
    else:
        st.session_state.active_chat_id = create_conversation()


# --------------------------------------------------

# --------------------------------------------------
# 5. SIDEBAR - CONVERSATION MANAGEMENT
# --------------------------------------------------

with st.sidebar:

    st.markdown("## 🤖 TRUJARVIS")
    st.caption("AI for Everything")
    st.divider()

    # New conversation
    if st.button(
        "＋ New Chat",
        use_container_width=True,
        key="new_chat"
    ):

        new_id = create_conversation("New Chat")
        st.session_state.active_chat_id = new_id
        st.rerun()

    st.markdown("### Your Conversations")

    conversations = get_conversations()

    if not conversations:
        st.caption("No conversations yet.")

    for conversation in conversations:

        chat_id = conversation["id"]
        title = conversation["title"]

        col1, col2 = st.columns([5, 1])

        with col1:

            is_active = (
                chat_id == st.session_state.active_chat_id
            )

            label = (
                f"🔵 {title}"
                if is_active
                else f"💬 {title}"
            )

            if st.button(
                label,
                key=f"select_{chat_id}",
                use_container_width=True
            ):

                st.session_state.active_chat_id = chat_id
                st.rerun()

        with col2:

            with st.popover("⋮"):

                st.markdown("**Manage conversation**")

                # Rename conversation
                with st.form(
                    key=f"rename_form_{chat_id}"
                ):

                    new_title = st.text_input(
                        "Conversation title",
                        value=title,
                        key=f"rename_input_{chat_id}"
                    )

                    rename_clicked = st.form_submit_button(
                        "Rename",
                        use_container_width=True
                    )

                    if rename_clicked:

                        clean_title = new_title.strip()

                        if clean_title:

                            rename_conversation(
                                chat_id,
                                clean_title[:60]
                            )

                            st.success("Chat renamed!")
                            st.rerun()

                        else:
                            st.warning("Title cannot be empty.")

                st.divider()

                # Delete individual conversation
                if st.button(
                    "🗑️ Delete Chat",
                    key=f"delete_{chat_id}",
                    use_container_width=True
                ):

                    delete_conversation(chat_id)

                    if st.session_state.active_chat_id == chat_id:

                        remaining = get_conversations()

                        if remaining:
                            st.session_state.active_chat_id = (
                                remaining[0]["id"]
                            )
                        else:
                            st.session_state.active_chat_id = (
                                create_conversation()
                            )

                    st.rerun()

    # Delete all conversations
    st.divider()

    st.markdown("### 🧹 Chat Cleanup")

    with st.expander("Delete all conversations"):

        st.warning(
            "This permanently deletes all saved conversations."
        )

        confirm_delete = st.checkbox(
            "I understand. Delete all chats.",
            key="confirm_delete_all"
        )

        if st.button(
            "Delete Everything",
            disabled=not confirm_delete,
            use_container_width=True,
            type="primary"
        ):

            delete_all_conversations()

            new_id = create_conversation("New Chat")

            st.session_state.active_chat_id = new_id

            st.rerun()

    st.divider()

    # ------------------------------------------
    # ADVANCED MODEL SETTINGS
    # ------------------------------------------

    st.divider()

    with st.expander("🧠 Advanced Model Settings"):

        st.caption("Configure TRUJARVIS AI generation.")

        # Available Ollama models
        try:
            available_models = engine.get_available_models()
        except Exception:
            available_models = [MODEL_NAME]

        if MODEL_NAME not in available_models:
            available_models.insert(0, MODEL_NAME)

        selected_model = st.selectbox(
            "AI Model",
            options=available_models,
            index=available_models.index(MODEL_NAME),
            key="llm_model"
        )

        st.divider()

        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.5,
            value=0.7,
            step=0.1,
            key="llm_temperature",
            help="Controls response creativity."
        )

        top_p = st.slider(
            "Top P",
            min_value=0.1,
            max_value=1.0,
            value=0.9,
            step=0.05,
            key="llm_top_p"
        )

        context_length = st.select_slider(
            "Context Window",
            options=[1024, 2048, 3072, 4096],
            value=2048,
            key="llm_context"
        )

        max_tokens = st.select_slider(
            "Maximum Response Tokens",
            options=[128, 256, 512, 768, 1024],
            value=512,
            key="llm_max_tokens"
        )

        repeat_penalty = st.slider(
            "Repeat Penalty",
            min_value=1.0,
            max_value=1.5,
            value=1.1,
            step=0.05,
            key="llm_repeat_penalty"
        )

        st.caption("Settings are applied to subsequent AI responses.")

    # System information
    st.markdown("### ⚙️ System Information")

    st.caption(f"Model: `{MODEL_NAME}`")
    st.caption("Runtime: Local Ollama")

    connected, connection_message = engine.check_connection()

    if connected:
        st.success("AI Engine Online")
    else:
        st.error("AI Engine Offline")
        st.caption(connection_message)

    st.caption(f"TRUJARVIS v{APP_VERSION}")

# --------------------------------------------------
# 6. MAIN HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">TRUJARVIS</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your Personal AI Assistant · Powered by Local LLM'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# --------------------------------------------------
# 7. LOAD CURRENT CONVERSATION
# --------------------------------------------------

active_chat_id = st.session_state.active_chat_id

messages = get_messages(active_chat_id)


# --------------------------------------------------
# 8. DISPLAY CHAT HISTORY
# --------------------------------------------------

if not messages:

    st.markdown("### 👋 Welcome to TRUJARVIS")

    st.markdown(
        "I'm your personal AI assistant. "
        "Ask me anything to get started."
    )

    st.caption(
        "Running locally through Ollama and Llama 3.2."
    )

else:

    for message in messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])


# --------------------------------------------------
# 9. USER INPUT AND AI RESPONSE
# --------------------------------------------------

prompt = st.chat_input("Ask TRUJARVIS anything...")

if prompt:

    if not connected:

        st.error(
            "Ollama is not available. "
            "Please start Ollama and try again."
        )

        st.stop()

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare conversation context
    chat_history = [
        {
            "role": message["role"],
            "content": message["content"]
        }
        for message in messages
    ]

    chat_history.append({
        "role": "user",
        "content": prompt
    })

    # Save user message
    save_message(
        active_chat_id,
        "user",
        prompt
    )

    # Automatically generate conversation title
    if len(messages) == 0:

        title = prompt.strip().replace("\n", " ")[:40]

        if not title:
            title = "New Chat"

        update_conversation_title(
            active_chat_id,
            title
        )

    # Generate AI response
    with st.chat_message("assistant"):

        try:

            with st.spinner("TRUJARVIS is thinking..."):

                response = st.write_stream(
    engine.generate_response(
        messages=chat_history,
        model=selected_model,
        temperature=temperature,
        top_p=top_p,
        num_ctx=context_length,
        num_predict=max_tokens,
        repeat_penalty=repeat_penalty
    )
)

            if response:
                save_message(
                    active_chat_id,
                    "assistant",
                    response
                )

        except Exception as error:

            st.error("Something went wrong while generating the response.")

            st.caption(str(error))
