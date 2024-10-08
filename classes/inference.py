from threading import Thread
from classes.model import MODEL
from ultralytics import YOLO
from time import sleep

def kill_dead_threads(instances: dict) -> None:
    for key in list(instances.keys()):
        thread, model = instances[key]
        if not thread.is_alive():
            model.stop()
            del thread
            del model
            del instances[key]

class INSTANCE:
    instances : dict = {}

    def __init__(self):
        pass

    def add(self, model: MODEL, source: str = "0", show_vid: bool = False) -> int:
        '''
        returns 0: for successful model upload

        returns 1: for MAX model limit reached

        returns 2: for source already present in the dictionary
        '''
        source = 0 if source == "0" else source

        kill_dead_threads(self.instances)

        if (len(self.instances) >= 5):
            print("Maximum number of instances reached. Please stop some instances before adding new ones.")
            return 1

        if str(source) in list(self.instances.keys()):
            print(f"Source {source} already exists in the list of instances.")
            return 2

        thread = Thread(target=model.count, kwargs={"source": source, "show_vid": show_vid})
        thread.start()
        if isinstance(source, int):
            source = str(source)
        self.instances[source] = (thread, model)
        return 0

    def print_vitals(self):
        print(f"Instances: {self.instances}")

    def get_active_sources(self):
        return list(self.instances.keys())

    def stop(self, source: str) -> None:
        if isinstance(source, int):
            source = str(source)

        val = self.instances.pop(source, None)
        if val is not None:
            thread, model = val
            model.stop()
            del thread
            del model
        else:
            print(f"Source {source} not found in the list of instances.")

    def stop_all(self):
        for key in list(self.instances.keys()):
            val = self.instances.pop(key, None)
            if val is not None:
                thread, model = val
                model.stop()
                del thread
                del model

if __name__ == "__main__":
    model1 = MODEL("MyModel1")
    model1.mount(YOLO("weights/final.pt"))
    model2 = MODEL("MyModel2")
    model2.mount(YOLO("weights/final.pt"))
    instance = INSTANCE()
    instance.add(model1)
    print("Added model 1")
    instance.add(model2, "samples/sample.mp4")
    print("Added model 2")
    instance.print_vitals()
    sleep(30)
    print("Sleep over!")
    instance.stop_all()
    sleep(5)
    instance.print_vitals()