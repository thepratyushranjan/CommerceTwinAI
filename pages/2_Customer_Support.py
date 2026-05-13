import streamlit as st
from modules.support.agent import run_agent
import json

st.set_page_config(page_title="Customer Support Agent", page_icon="🤖", layout="wide")

st.title("🤖 Customer Support AI Assistant")
st.markdown("""
Welcome! I can help you check your **order status**, explain our **policies** (returns, shipping, etc.), 
or escalate your issue to a human agent if needed.
""")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize trace for the last query
if "last_trace" not in st.session_state:
    st.session_state.last_trace = []

# Sidebar for Agent Trace
with st.sidebar:
    st.header("🔍 Agent Reasoning Trace")
    st.info("Watch the agent's 'thinking steps' and tool usage here.")
    
    if st.session_state.last_trace:
        for i, step in enumerate(st.session_state.last_trace):
            with st.expander(f"Step {i+1}: {step['tool']}", expanded=True):
                st.markdown("**Tool Output:**")
                st.text(step['output'][:500] + ("..." if len(step['output']) > 500 else ""))
    else:
        st.write("No tool calls yet. Ask a question about an order or policy!")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("How can I help you today?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Agent is thinking and searching tools..."):
            try:
                # Prepare history for the agent (convert from dict to tuples)
                history = [(m["role"], m["content"]) for m in st.session_state.messages[:-1]]
                
                # Run the agent
                result = run_agent(prompt, history)
                
                # Display response
                st.markdown(result["response"])
                
                # Update trace in session state for the sidebar
                st.session_state.last_trace = result["trace"]
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": result["response"]})
                
                # Rerun to update sidebar
                st.rerun()
                
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
