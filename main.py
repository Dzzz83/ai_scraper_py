import streamlit as st
from scrape import scrape_website, extract_body_content, clean_body_content, split_dom_content
from dumb_ai import parse_with_ollama

# Streamlit UI
st.title("AI Web Scraper!")

url = st.text_input("Enter a website's URL: ")

# Check if scraping has been performed
if 'scraping_done' not in st.session_state:
    st.session_state.scraping_done = False

if st.button("Scrap Site"):
    if not st.session_state.scraping_done:
        st.write("Scraping the website...")
        scraped_data = scrape_website(url)
        body_content = extract_body_content(scraped_data)
        cleaned_content = clean_body_content(body_content)
        st.session_state.dom_content = cleaned_content
        st.session_state.scraping_done = True  # Mark scraping as done

        with st.expander("View DOM content: "):
            st.text_area("DOM content", cleaned_content, height=300)
    else:
        st.write("Scraping has already been performed. Please use the 'Parse Content' button to parse the data.")

if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse: ")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content ...")

            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks, parse_description)
            st.write(result)
        else:
            st.write("Please provide a description of what you want to parse.")
