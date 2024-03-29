"""
A streamlit web app which accepts `spotify` provided data.
Shows overview of the data with graphs and text after some EDA.
"""

# --- imports ---
import streamlit as st
import pandas as pd

from src.database.manage import stream_df

# --- Page config ---
st.set_page_config('Spotify Data Analysis', ':music:', 'wide')


# --- import files ---
# Listening history
df = stream_df()


def overall_analysis(df_group):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader('Songs played')
        st.bar_chart(df_group['trackName'].nunique())
    with col2:
        st.subheader('Artist played')
        st.bar_chart(df_group['artistName'].nunique())
    with col3:
        st.subheader('Minutes listened',)
        st.bar_chart((df_group['msPlayed'].sum()/60000).round())


def one_on_analysis(sf: pd.DataFrame, exp_text: str):
    with st.expander(exp_text, True):
        col1, col2, col3 = st.columns(3)
        with col1:
            res = sf['trackName'].value_counts()
            st.metric('Most times listend song', str(res.index[0]))
            st.bar_chart(res[:10])

            # Display the DataFrame with trackName and artistName columns
            display_df = (sf[sf['trackName'].isin(res[:12].index)]
                          [['trackName', 'artistName']]
                          .drop_duplicates()
                          .reset_index(drop=True))
            st.table(display_df[:12].sort_values(by='trackName'))
        with col2:
            res = sf['artistName'].value_counts()
            st.metric('Most times Listend artist', str(res.index[0]))
            st.bar_chart(res[:10])

            # Display the DataFrame with trackName and artistName columns
            display_df = (sf[sf['artistName'].isin(res[:12].index)]
                          [['trackName', 'artistName']]
                          .drop_duplicates()
                          .reset_index(drop=True))
            st.dataframe(display_df, height=460, use_container_width=True)
        with col3:
            res = sf.groupby('trackName')['msPlayed'].sum()/60000
            st.metric('Minutes listend', round(res.sum()))
            st.bar_chart((res.sort_values(ascending=False)[:10]).round())
            # Display the DataFrame
            st.table((res
                      .sort_values(ascending=False)[:12]
                      .reset_index()
                      .rename(columns={'msPlayed': 'minPlayed'})))


# --- --- Sidebar --- ---
with st.sidebar:
    st.title('Spotify Data Analysis')
    overall_analysis_btn = st.radio('Select Analysis',
                                    options=['YoY', 'MoM'])


# --- Hero page ---
# --- Overall year analysis ---
if overall_analysis_btn == 'YoY':
    st.title('YoY Analysis')

    year_group = df.groupby('year')

    with st.expander('All years analysis', True):
        overall_analysis(year_group)

    '---'
    # --- Each year analysis ---

    opt = df['year'].unique()
    # Selectbox
    year_selected = st.selectbox('Select month for analysis', opt)
    # Selected frame
    sf = df.query('year==@year_selected')

    # Summary of year - expander
    one_on_analysis(sf, f'Summary of {year_selected}')


# --- Overall month analysis ---
elif overall_analysis_btn == 'MoM':
    st.title('MoM Analysis')

    month_group = df.groupby('month')

    with st.expander('All month analysis', True):
        overall_analysis(month_group)

    '---'
    # --- Each month analysis ---

    opt = df['endTime'].dt.strftime('%B %Y').unique()
    # Selectbox
    month_selected, year_selected = str(st.selectbox(
        'Select month for analysis', opt)).split(' ')
    # Selected frame
    sf = df[(df['month'] == month_selected) &
            (df['year'] == int(year_selected))]

    # Summary of month - expander
    one_on_analysis(sf,
                    f'Summary of **{month_selected} {year_selected}** month')
