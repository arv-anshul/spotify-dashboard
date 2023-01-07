import streamlit as st

# --- page config ---
st.set_page_config('README.md', '🗒️', 'wide')

# Reading README.md file
# To display it as markdown in streamlit app
with open('README.md', 'r') as f:
    st.markdown(f.read())
