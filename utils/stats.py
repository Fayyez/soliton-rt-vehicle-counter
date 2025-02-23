import streamlit as st
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
from streamlit_theme import st_theme
import random

random.seed()  # Seed the random number generator

def get_theme():
    # theme = st_theme()
    theme = None
    if theme is None:
        theme = {
            "backgroundColor": "#ffffff",
            "textColor": "#000000"
        }
    return theme

@st.cache_data
def draw_chart(data: DataFrame, theme: dict):
    fig, ax = plt.subplots()
    fig.patch.set_facecolor(theme["backgroundColor"])
    wedges, texts, autotexts = ax.pie(data["counts"], labels=data["class"], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    for text in texts + autotexts:
        text.set_color(theme["textColor"])
    return fig

@st.fragment(run_every=10)
def render_statistics():
    # get the current system theme
    theme = get_theme()
    # create tabs
    tabs = st.tabs(["📝 Table", "📈 Visualization"])

    with tabs[0]:
        st.dataframe(st.session_state.data_for_visualization, use_container_width=True, hide_index=True)

    with tabs[1]:

        # layout = st.columns(2)

        # with layout[0]:
        #     fig = draw_chart(st.session_state.data_for_visualization, theme)
        #     st.pyplot(fig)

        # with layout[1]:
        st.bar_chart(st.session_state.data_for_visualization, x="class", y="counts")