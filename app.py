# imports
import streamlit as st
from datetime import datetime
from utils.stats import render_statistics
from components.main_pane import display_option_menu
from components.active_camera_table import update_model_status_table
from utils.input import load_instance
from classes.inference import kill_dead_threads
from components.download_component import file_downloader
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def main(_args):

    # page configurations
    page_config = st.set_page_config(
        page_title="Object Counter",
        page_icon="🚗",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    # creating dataframe
    instance = load_instance()
    kill_dead_threads(instance.instances) # kill all dead instances if any
    st.session_state.sources = instance.get_active_sources()
    st.session_state.active_cams_present = True if len(st.session_state.sources) > 0 else False

    if st.session_state.active_cams_present:
        st.session_state.main_pane_cols = 2
    else:
        st.session_state.main_pane_cols = 1

    # title of page
    logo_image_base64 = get_base64_image("assets/logo.png")
    soliton_image_base64 = get_base64_image("assets/soliton-logo.png")
    st.markdown(f'''
    <h1 style='text-align: center; font-style: italic; font-size: 56px; margin: 0; padding: 0; line-height: 56px; margin-left: 0px;'>
        <img src="data:image/png;base64,{logo_image_base64}" alt="icon" width="80" style="vertical-align: middle; margin-right: 0px; padding-right: 0px;">
        ountistics
    </h1>
        <p style='text-align: center; font-size: 17px;'>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            ~ Powered by
            <a href="https://www.solitontechnologies.com/" target="_blank">
                <img src="data:image/png;base64,{soliton_image_base64}" alt="logo" width="80">
            </a>
        </p>
    ''', unsafe_allow_html=True)

    st.session_state.main_pane = st.columns([3, 2] if st.session_state.main_pane_cols == 2 else st.session_state.main_pane_cols,
                                            gap="medium",
                                            vertical_alignment="top")


    if "instance" not in st.session_state:
        st.session_state.instance = load_instance()

    # display options menu
    display_option_menu()

    # creating running cameras summary in table here
    if st.session_state.active_cams_present:
        update_model_status_table()

    # downalod button
    with st.session_state.download_button:
        st.button(label="Download Report",
                help="Download the vehicle count report in CSV format and visualise the data",
                on_click=file_downloader,
                use_container_width=True)

    # page footer
    st.markdown("""
    <footer style="text-align:center; padding: 0px; background-color: transparent; bottom: 0; width: 100%;">
        <br>© 2024 Autoistics. All rights reserved. Developed by Eehab and Fayyez. ✨
    </footer>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main(None)