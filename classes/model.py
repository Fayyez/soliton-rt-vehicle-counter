from copy import deepcopy
from csv import writer
from ultralytics import YOLO
from ultralytics.solutions import ObjectCounter
from cv2 import imshow, waitKey, destroyAllWindows, VideoCapture
from cv2 import CAP_PROP_POS_FRAMES
from cv2.typing import MatLike
from datetime import datetime
from datetime import datetime
from os.path import exists
from os import makedirs

def getName(source: str):
    if isinstance(source, int):
        source = str(source)
    source = source.split("\\")[-1]
    if "http" in source or "https" in source:
        source = source.removeprefix("http://").removeprefix("https://").replace(".com","").replace("www.", "").replace("/", "_").replace(".", "_"). replace(":", "_")
    elif source.isdigit():
        source = f"cam{source}"
    else:
        source = source.split("/")[-1].split(".")[0]

    return f"counts_{source}_{datetime.now().strftime("%d-%m-%y")}.csv"

class MODEL:
    __model = None

    def __init__(self, name: str = "Default") -> None:
        self.name = name
        self.stopped = False
        pass

    def __str__(self) -> str:
        if isinstance(self.__model, YOLO):
            return f"<class 'MODEL':YOLO ({self.name})>"
        else:
            return "<class 'MODEL'>"

    def __repr__(self) -> str:
        return self.__str__()

    def mount(self, model: any) -> None:
        self.__model = model

    def unmount(self) -> None:
        self.__model = None

    def execute(self, source: str = "0", skip: int = 1) -> None:
        if isinstance(self.__model, YOLO):
            try:
                source = source if source != "0" else 0
                for result in self.__model.predict(source=source, task="detect", vid_stride=skip, stream=True, stream_buffer=True):
                    frame = result.plot()
                    imshow('Video', frame)
                    if waitKey(1) == ord('q'):
                        break
            except Exception as e:
                print(f"Error occurred: {e}")
            destroyAllWindows()
        elif self.__model is None:
            print("No model detected. Mount a model first using `MODEL.mount(your_model)`")
        else:
            print("Operation unsupported for the mounted model.")

    def __dump(self, counts: dict, source: str, output: str = "storage") -> None:
        classes = self.__model.names
        if not exists(output):
            makedirs(output)
        filename = getName(source)
        with open(output + "/" + filename, "w", newline="") as file:
            csv_writer = writer(file)
            csv_writer.writerow(["class", "counts"])
            for cls in list(classes.values()):
                if cls in list(counts.keys()):
                    csv_writer.writerow([cls, counts[cls]["IN"]])
                else:
                    csv_writer.writerow([cls, 0])

    def __clean_count(self, counts: dict, source:str) -> None:
        print(f"\nRAW = {counts}")
        print(f"Object Counts for {getName(source):}")
        for cls, val in counts.items():
            if isinstance(val, dict):
                keys = list(val.keys())
                if "IN" in keys and "OUT" in keys:
                    for direction in keys:
                        print(f"{cls.capitalize()} ({direction}) = {val[direction]}")

    def count(self, source: str = "0", skip: int = 1, region_points: list = [(500, 450), (500, 1300)], show_vid: bool = False) -> None:
        if isinstance(self.__model, YOLO):
            try:
                frame_count = 0
                source = source if source != "0" else 0
                capture = VideoCapture(source)

                object_counter = ObjectCounter(
                    view_img=show_vid,
                    reg_pts=region_points,
                    classes_names=self.__model.names,
                    draw_tracks=show_vid,
                    view_in_counts=show_vid,
                    view_out_counts=show_vid,
                    line_thickness=2
                )

                old_classwise_count = {}
                while capture.isOpened():
                    success, im0 = capture.read()
                    if not success:
                        break
                    tracks = self.__model.track(im0, persist=True, show=False, verbose=True)
                    im0 = object_counter.start_counting(im0, tracks)

                    new_classwise_count = object_counter.class_wise_count

                    if new_classwise_count != old_classwise_count:
                        self.__dump(new_classwise_count, source)
                        old_classwise_count = deepcopy(new_classwise_count)

                    frame_count += skip
                    capture.set(CAP_PROP_POS_FRAMES, frame_count)

                    if self.stopped:
                        break

                capture.release()
                destroyAllWindows()
            except Exception as e:
                print(f"Error occurred: {e}")
        elif self.__model is None:
            print("No model detected. Mount a model first using `MODEL.mount(your_model)`")
        else:
            print("Operation unsupported for the mounted model.")

    def stop(self):
        self.stopped = True