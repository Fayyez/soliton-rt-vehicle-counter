# displaying control panel
import streamlit as st
from streamlit_option_menu import option_menu
from utils.input import on_upload, handle_camera_stream, handle_ip_stream, load_instance
from utils.onlycams import list_hot_cameras_on_my_device
from utils.deleteFiles import delete_all_reports
def reset_options():
    st.session_state.menu_options = ["Upload", "With IP Address", "Use Camera"]

def display_option_menu():
    with st.session_state.main_pane[0]:
        # heading
        st.header("Control Panel")
        # option menu
        if "menu_options" not in st.session_state:
            st.session_state.menu_options = ["Upload", "With IP Address", "Use Camera"]
        st.session_state.selected = option_menu("Select Video",
                                options=st.session_state.menu_options,
                                icons=["upload", "hdd-network", "camera"],
                                orientation="horizontal",
                                menu_icon="record-btn",
                                default_index=0)

        # empty container for input option
        st.session_state.input_option_bucket = st.empty()
        st.session_state.start_button, st.session_state.download_button = st.columns([1,1], gap="medium")

        if len(st.session_state.menu_options) == 1:
            # if only one option is present, then display the add more camera option
            st.subheader("Note:")
            if len(load_instance().get_active_sources()) >= 5: # if limit has reached
                st.write("You have reached the limit of adding 5 cameras. Please remove some cameras to add more.")
            else:
                with st.session_state.start_button:
                    st.button(label="Add More",
                            key="add_more_btn",
                            help="click this button to add more cameras to the session",
                            on_click=reset_options,
                            type="primary")
                st.write("You may add upto 5 cameras for counting vehicles simultaneously in one sesssion. Click \"Add More\" below to add more cameras.")

        elif st.session_state.selected == "Upload":
            # create and upload file dropbox and opload button
            uploaded_file =  st.session_state.input_option_bucket.file_uploader(label="Upload Video:hot_pepper:",
                            type=["mp4", "avi", "mov", "mkv"],
                            help="Upload a video file. Allowed formats: mp4, avi, mov, mkv",
                            accept_multiple_files=False)
            with st.session_state.start_button:
                st.session_state.upload_button = st.button(label="Upload Video",
                                                        key="upload_btn",
                                                        help="Run the model inference and start counting vehicles",
                                                        on_click=on_upload,
                                                        use_container_width=True)
            st.session_state.uploaded_file = uploaded_file

        elif st.session_state.selected == "With IP Address":
            form = st.session_state.input_option_bucket.columns(2)
            username = form[0].text_input("Username") # username input
            password = form[1].text_input("Password") # password input
            ip = form[0].text_input("IP Address") # ip address input
            port = form[1].number_input("Port", value=554) # port input
            channel_no = form[0].number_input("Channel No", value=1) # channel number input
            type_no = form[1].number_input("Type No", value=0) # type number input
            with st.session_state.start_button:
                st.button("Get RTSP Stream",
                        on_click=handle_ip_stream,
                        use_container_width=True,
                        args=(username, password, ip, port, channel_no, type_no)) # button to get the rtsp stream

        elif st.session_state.selected == "Use Camera":
            # display all available web cams in dropdown
            all_cams = list_hot_cameras_on_my_device()
            st.session_state.selected_cam =  st.session_state.input_option_bucket.selectbox(label="Select camera from the list below",
                                                        options=list(all_cams.keys()))
            with st.session_state.start_button:
                st.session_state.run_cam_button = st.button("Open Camera",
                                                            help="Run the model inference and start counting vehicles from selected camera input",
                                                            key="run_cam_btn",
                                                            on_click=handle_camera_stream,
                                                            use_container_width=True)
        # delete all the csv files in the storage folder
        st.button("🗑️ Delete All Reports",
                on_click=delete_all_reports,
                type="primary",
                help="Warning: This button will delete all the reports generated till now.",
                use_container_width=True,
                key="delete_all_reports_btn")