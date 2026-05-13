import streamlit as st

st.set_page_config(
    page_title="AI Assistant Platform for E-commerce",
    page_icon="🛍️",
    layout="wide"
)

st.title("🛍️ AI Assistant Platform for E-commerce")

st.markdown("""
Welcome to the AI Assistant Platform. This integrated suite provides powerful AI tools 
to streamline your e-commerce operations, from generating high-converting marketing 
content to providing world-class customer support.
""")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("📸 Content Generator")
        st.write("""
        Transform your product images into complete marketing packages. 
        Get professional titles, descriptions, SEO keywords, and social media posts 
        instantly.
        """)
        st.page_link("pages/1_Content_Generator.py", label="Go to Content Generator", icon="🎨")

with col2:
    with st.container(border=True):
        st.subheader("🤖 Customer Support")
        st.write("""
        An agentic chatbot that handles customer inquiries using RAG and tool calling. 
        Check order status, search knowledge base, and escalate when necessary.
        """)
        st.page_link("pages/2_Customer_Support.py", label="Go to Customer Support", icon="💬")

st.sidebar.success("Select a module above to get started.")
