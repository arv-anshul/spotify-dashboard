# Spotify Dashbord Web App

This web app made with `python + pandas + streamlit`. This app uses the user's listening data which is downloaded from the spotify [website](https://www.spotify.com/in-en/account/privacy/).

Clone this repository to run the web app by running these following commands:

```bash
# To install streamlit library
pip install streamlit

# To open the streamlit web app in your browser
streamlit run 1_🗒️_README.py
```

## Process:

1. Download the requested data from spotify. And merge similar files.
2. Also `delete credential files`. Some files may contains your spotify login ID.

```bash
# File Structure:
.
├── 1_🗒️_README.py
├── README.md
├── __pycache__
│   └── analysis.cpython-311.pyc
├── __rough__.ipynb
├── analysis.py
├── data_files
│   ├── Playlist1.json
│   ├── Playlist2.json
└── pages
    ├── 2_💬_Overview.py
    ├── 3_🗂️_Playlist.py
    └── 4_🎙_Artist.py
```

3. Did some EDA on `StreamingHistory*.json` files to get some `MoM` and `YoY` insights.
4. On `Playlist*.json` files:
   1. Import the file with `pd.read_json()`.
   2. Normalize it with `pd.normalize_json(data, record_path, record_prefix, meta, meta_prefix)`.
   3. Then drop some blank columns.
   4. Finally, apply `pd.merge()` to merge the df on `'name'` column.

---

## Created by [arv-anshul](https://github.com/arv-anshul)

- I first did some analysis on this data with `jupyter notebook` about 6 months ago.
- But now I learned the `streamlit` (a python library which helps to create web apps).
- Then, I created this `my spotify` listening data dashboard with `streamlit`.
