import streamlit as st
from tempfile import NamedTemporaryFile
from utils.dialogBox import showDialogBox
from utils.onlycams import list_hot_cameras_on_my_device
from classes.model import MODEL
from classes.inference import INSTANCE
from ultralytics import YOLO
from pandas import DataFrame
from cv2 import VideoCapture, destroyAllWindows

@st.cache_resource
def load_instance():
    return INSTANCE()

def active_cams_present() -> bool:
    active_sources = load_instance().get_active_sources()
    if len(active_sources) == 0:
        return False
    else:
        return True

# function to load model and add to the instance
def add_model_to_instance(source: str, weights: str = "weights/final.pt"):

    # fetch instance and add model
    instance: INSTANCE = load_instance()
    # check if given source is valid video capture object
    if str(source) not in instance.get_active_sources():
        cap = VideoCapture(source)
        if not cap.isOpened():
            # if video cpture object cannot be created
            showDialogBox(heading="Error 03: Invalid Video Source",
                        message="The source of video given could not be loaded due to corrupt file, unstable connection or incorrect IP address")
            return
        else:
            cap.release()
            destroyAllWindows()

    # load model and mount the weights
    model = MODEL()
    model.mount(YOLO(weights))
    response =  instance.add(model, source)
    # manage all response conditions here
    if response == 0:
        return True # true for successful execution of add camera to instance
    elif response == 1:
        showDialogBox(heading="Error 01: Camera Limit Reached",
                    message="Only 5 cameras can be added at a time. Kindly remove active cameras before adding new cameras.")
    elif response == 2:
        showDialogBox(heading="Error 02: Camera Duplication",
                    message="This camera is already present in the active cameras list. Please choose another camera or hav patience.")
    return False # false indicates failure to add the camera source to instance

def on_upload() -> None:
    if st.session_state.get("uploaded_file") is not None: # if a file is uploaded
        st.session_state.menu_options = ["Upload"]
        video_file = st.session_state.uploaded_file
        # create a temporary copy of the uploaded file in storage folder
        with NamedTemporaryFile(delete=False, suffix=video_file.name.split(".")[-1]) as temp:
            temp.write(video_file.read())
            add_model_to_instance(temp.name)

    else:
        showDialogBox(heading="Upload Error",
                    message="File not uploaded properly. file not present, incompatible format or file size > 200mb.")

def handle_ip_stream(username: str, password: str, ip: str, port: int = 554, channel_no: int = 1, type_no: int = 0) -> None:
    url = f"rtsp://{username}:{password}@{ip}:{port}/cam/realmonitor?channel={channel_no}&subtype={type_no}"
    add_model_to_instance(url)

# handling case of using camera stream
def handle_camera_stream() -> None:
    st.session_state.menu_options = ["Use Camera"]
    selected_option = str(st.session_state.selected_cam)
    if selected_option == None:
        showDialogBox(heading="Error 05: Camera Not Found",
                    message="Please select a camera first before trying to use that camera's stream for detections")
        return None
    all_cams = list_hot_cameras_on_my_device()
    add_model_to_instance(all_cams[selected_option])
