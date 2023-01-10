import streamlit as st

# --- page config ---
st.set_page_config('README', '🗒️', 'wide')

st.markdown(
    '## :blue[Made By] [:red[Anshul Raj Verma]](https://github.com/arv-anshul)')
# Reading README.md file
# To display it as markdown in streamlit app
with open('README.md', 'r') as f:
    st.markdown(f.read())
