import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_scraped_content,
    split_dom_content, extract_images, detect_type
)
from parse import parse_with_ollama

# =======================
#   PAGE CONFIGURATION
# =======================
st.set_page_config(
    page_title="ScrapePilot - WebScrape with AI",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =======================
#   HEADER SECTION
# =======================
st.markdown("""
<div class="main-header">
    <h1 style="font-size: 3em; margin: 0;">🌐 ScrapePilot</h1>
    <p style="font-size: 1.2em; opacity: 0.9; margin-top: 10px;">
    Intelligent Web Scraping & AI-Powered Content Extraction
    </p>
</div>
""", unsafe_allow_html=True)

url = st.text_input("Enter Website URL")

# =======================
#   SCRAPE SECTION
# =======================
if st.button("Scrape Website"):
    if not url:
        st.error("⚠️ Enter a URL first.")
    else:
        st.write(f"🔍 Starting scrape for: **{url}**")
        st.info("⏳ Scraping in progress...")
        print(f"[INFO] Starting scrape for: {url}")

        result = scrape_website(url)
        body_content = extract_body_content(result)
        cleaned_content = clean_scraped_content(body_content)

        with st.spinner("⏳ Parsing website type..."):
            website_type = detect_type(cleaned_content)
        st.info(f"🔍 Detected Type: {website_type}")
        
        images = extract_images(result)
        if images:
            st.info(f"🖼️ Found {len(images)} images on the page.")
                
        if cleaned_content:
            st.session_state.dom_content = cleaned_content
            st.success("🎉 Scraping complete!")
            # Uncomment if you want preview:
            # with st.expander("📄 View Extracted Content"):
            #     st.text_area("DOM Content", cleaned_content, height=300)
        else:
            st.error("❌ Scrape failed. Check logs.")
            st.session_state.dom_content = None

# =======================
#   PARSING SECTION
# =======================
if "dom_content" in st.session_state and st.session_state.dom_content:

    parse_description = st.text_area("🧠 Describe what you want to parse:")

    # Parse Button
    if st.button("Parse Content"):
        if not parse_description:
            st.error("⚠️ Please enter what you want to extract.")
        else:
            st.write("🔍 Parsing content with AI...")
            dom_chunks = split_dom_content(st.session_state.dom_content)
            parsed_output = parse_with_ollama(dom_chunks, parse_description)

            st.success("🎯 Parsing complete!")
            st.text_area("Parsed Output", parsed_output, height=300)
            print("[INFO] Parsing completed successfully.")
