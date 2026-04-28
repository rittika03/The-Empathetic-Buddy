import streamlit as st
from core_engine import run_safety_check, extract_state, retrieve_framework, generate_response, update_profile

# 1. Page Configuration (Sets the clean wide/centered look with Sidebar)
st.set_page_config(page_title="TheAware.AI | Data AImers", layout="centered", initial_sidebar_state="expanded")

# 2. Sidebar Navigation
st.sidebar.markdown("### Menu")
# Using a selectbox or radio button for clean navigation
page = st.sidebar.radio("", ["Home", "Conversation History", "About"], label_visibility="collapsed")

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {"name": "User", "stressors": []}

# ==========================================
# PAGE 1: HOME (The Main Chatbot)
# ==========================================
if page == "Home":
    st.title("🧠 The Empathetic Buddy")
    st.caption("Track B: Implicit Emotion Detection & Orchestration")
    st.markdown("Welcome to The Empathetic Buddy, your personalized emotional support AI. Please feel free to share what's on your mind.")
    st.markdown("---")

    # Display Chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User Input
    if user_input := st.chat_input("Type your message here..."):
        # Render user message
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # 1. Safety Check
        is_crisis, crisis_msg = run_safety_check(user_input)
        if is_crisis:
            with st.chat_message("assistant"):
                st.error(f"🚨 **CRISIS ALERT ESCALATION**\n\n{crisis_msg}")
            st.session_state.messages.append({"role": "assistant", "content": crisis_msg})
            st.stop()

        with st.spinner("Analyzing implicit signals..."):
            # 2. Extract State (LLM-1)
            history_str = str([m["content"] for m in st.session_state.messages[-5:]])
            state = extract_state(user_input, history_str, st.session_state.user_profile)
           
            # Update Profile
            st.session_state.user_profile = update_profile(st.session_state.user_profile, state.get("extracted_entities", []))

            # 3. Retrieve Context
            search_query = f"{state.get('primary_state', '')} {state.get('cognitive_pattern', '')}"
            framework = retrieve_framework(search_query)

            # 4. Generate Output (LLM-2)
            response_text = generate_response(state, st.session_state.user_profile, framework, history_str, user_input)

        # Render assistant response
        with st.chat_message("assistant"):
            st.markdown(response_text)
            with st.expander("🔍 System Telemetry (Only for Judge's View)"):
                st.json(state)
                st.write("**Retrieved Framework:**", framework)
                st.write("**Updated Profile:**", st.session_state.user_profile)

        st.session_state.messages.append({"role": "assistant", "content": response_text})

# ==========================================
# PAGE 2: CONVERSATION HISTORY
# ==========================================
elif page == "Conversation History":
    st.title("🗂️ Conversation History")
    st.markdown("Review your past interactions below.")
    st.markdown("---")
   
    if not st.session_state.messages:
        st.info("No conversations yet. Go to 'Home' to start chatting!")
    else:
        for msg in st.session_state.messages:
            role = "🧑‍💻 You" if msg["role"] == "user" else "🤖 Buddy"
            st.markdown(f"**{role}:** {msg['content']}")
            st.divider()

# ==========================================
# PAGE 3: ABOUT
# ==========================================
elif page == "About":
    st.title("ℹ️ About the Project")
    st.markdown("---")
    st.markdown("""
    **Track:** OpenAImer Track B (Implicit Emotion Detection & Orchestration)  
    **Team:** Data AImers  
   
    ### System Architecture
    Our system utilizes an innovative **State-to-Text Orchestration** pipeline rather than standard RAG.
   
    1. **Emotion Router (LLM-1):** Extracts implicit emotional signals, cognitive distortions, and defense mechanisms into a structured JSON schema.
    2. **Vector Retrieval:** Queries a local ChromaDB ONNX database to retrieve specific clinical psychology frameworks (e.g., CBT, DBT).
    3. **Generative Core (LLM-2):** Formulates a concise, actionable, and hyper-personalized response grounded entirely in the extracted context and retrieved frameworks, completely avoiding generic sympathy.
    """)