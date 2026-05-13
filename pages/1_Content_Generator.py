import streamlit as st
from PIL import Image
import io
import concurrent.futures
from modules.content.vision import analyze_image
from modules.content.text_gen import generate_text_content
from modules.content.banner import generate_banner

st.set_page_config(page_title="Content Generator", page_icon="🎨", layout="wide")

# Custom CSS for better aesthetics
st.markdown("""
<style>
    .reportview-container .main .block-container{
        padding-top: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .stCodeBlock {
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📸 Product Content Generator")
st.markdown("Transform your product images into complete, high-converting marketing packages instantly.")

# Initialize session state
if "content_generated" not in st.session_state:
    st.session_state.content_generated = False
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None
if "text_results" not in st.session_state:
    st.session_state.text_results = None
if "banner_image" not in st.session_state:
    st.session_state.banner_image = None

uploaded_file = st.file_uploader("Upload a high-quality product image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image_bytes = uploaded_file.getvalue()
    image = Image.open(io.BytesIO(image_bytes))
    
    col1, col2 = st.columns([1, 1.2], gap="large")
    with col1:
        st.image(image, caption="Source Product Image", width='stretch')
    
    with col2:
        st.write("### AI Analysis & Generation")
        st.info("Our multimodal AI will extract product attributes, write targeted copy, and design a promotional banner.", icon="🤖")
        
        if st.button("✨ Generate Marketing Content", type="primary", use_container_width=True):
            try:
                progress_text = "Analyzing visual attributes..."
                my_bar = st.progress(0, text=progress_text)
                
                attributes = analyze_image(image_bytes)
                st.session_state.analysis_results = attributes
                
                my_bar.progress(33, text="Drafting SEO copy & social media content...")
                
                # Run text and banner generation in parallel
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    text_future = executor.submit(generate_text_content, attributes)
                    banner_future = executor.submit(generate_banner, attributes, attributes.get("subcategory", "Product"))
                    
                    st.session_state.text_results = text_future.result()
                    my_bar.progress(66, text="Designing promotional banner...")
                    
                    st.session_state.banner_image = banner_future.result()
                
                my_bar.progress(100, text="Generation complete!")
                st.session_state.content_generated = True
                st.success("Successfully generated your marketing package!")
            except Exception as e:
                st.error(f"An error occurred during generation: {e}")

if st.session_state.content_generated:
    st.divider()
    st.header("📦 Your Marketing Package")
    
    res = st.session_state.text_results
    attrs = st.session_state.analysis_results
    
    # Use tabs for a cleaner, organized layout
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Product Copy", "🎯 SEO & Social", "🖼️ Promotional Banner", "🧠 AI Analysis Data"])
    
    with tab1:
        st.subheader("Product Title")
        st.code(res["title"], language=None)
        
        st.subheader("Product Description")
        st.code(res["description"], language=None)
        
        st.subheader("Key Features")
        features_text = "\n".join([f"- {feature}" for feature in res["features"]])
        st.code(features_text, language=None)

    with tab2:
        col_seo, col_social = st.columns(2, gap="large")
        
        with col_seo:
            st.subheader("SEO Optimization")
            st.markdown("**Target Keywords**")
            st.code(", ".join(res["seo_keywords"]), language=None)
            
            st.markdown("**Hashtags**")
            st.code(" ".join([f"#{t}" for t in res["hashtags"]]), language=None)
            
        with col_social:
            st.subheader("Social Media")
            st.markdown("**Instagram Caption**")
            st.code(res["instagram_caption"], language=None)
            
            st.markdown("**Twitter / X Caption**")
            st.code(res["twitter_caption"], language=None)

    with tab3:
        if st.session_state.banner_image:
            col_b1, col_b2 = st.columns([2, 1])
            with col_b1:
                st.image(st.session_state.banner_image, width='stretch', caption="Ready-to-use 16:9 Promotional Banner")
            with col_b2:
                st.write("### Usage")
                st.write("This banner is optimized for email marketing, website headers, and social media promotion.")
                st.download_button(
                    label="📥 Download High-Res Banner",
                    data=st.session_state.banner_image,
                    file_name="promo_banner.png",
                    mime="image/png",
                    type="primary"
                )
        else:
            st.warning("Banner generation failed. Please try again.")
            
    with tab4:
        st.write("### Extracted Visual Attributes")
        st.write("Our AI analyzed the image and extracted the following data to drive the content generation:")
        
        # Top-level categorizations
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            st.metric("Category", attrs.get("category", "N/A").title())
        with col_c2:
            st.metric("Subcategory", attrs.get("subcategory", "N/A").title())
        with col_c3:
            st.metric("Target Audience", attrs.get("target_audience", "N/A").title())
            
        st.divider()
        
        # Details layout
        col_d1, col_d2 = st.columns(2)
        
        with col_d1:
            st.markdown("#### 🎨 Design & Aesthetics")
            st.markdown(f"**Primary Color:** `{attrs.get('primary_color_hex', 'N/A')}`")
            if attrs.get('secondary_color_hex'):
                st.markdown(f"**Secondary Color:** `{attrs.get('secondary_color_hex')}`")
            
            st.markdown("**Style Adjectives:**")
            for style in attrs.get("style_adjectives", []):
                st.markdown(f"- {style.title()}")
                
        with col_d2:
            st.markdown("#### 🧶 Product Details")
            st.markdown("**Materials:**")
            for mat in attrs.get("materials", []):
                st.markdown(f"- {mat.title()}")
                
            st.markdown("**Distinctive Features:**")
            for feat in attrs.get("distinctive_features", []):
                st.markdown(f"- {feat.title()}")
                
        st.divider()
        st.markdown("#### 💡 Suggested Use Cases")
        for use_case in attrs.get("use_cases", []):
            st.markdown(f"- {use_case.capitalize()}")
