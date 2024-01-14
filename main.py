import os
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from garth.http import Client
import garth
import keyring

TOKENDIR = ".tokens"

# Garmin Connect API
class GarminConnectAPI:
    def __init__(self):
        self.client = Client()

    def login(self, email, password):
        try:
            garth.resume(TOKENDIR)
            garth.client.username
        except:
            try:
                self.client.login(email, password)
                garth.save(TOKENDIR)
            except Exception as e:
                print(e)
                return

    def upload(self, file_path):
        # Upload
        with open(file_path, "rb") as f:
            try:
                res = self.client.upload(f)
                print(res)
                print(f'Upload successful, activity id: {res["activityId"]}')
            except Exception as e:
                print(e)
                return

class Watchdog:
    def on_created(event):
        print(f"Hey, {event.src_path} has been created!")
        file_path = event.src_path
        if not file_path.endswith("inProgressActivity.fit"):
            print("Upload to Garmin Connect")
            garminConnect.upload(file_path)

    def __init__(
        self,
        patterns=["*"],
        ignore_patterns=None,
        ignore_directories=False,
        case_sensitive=True,
        path=".",
        go_recursively=True,
    ):
        self.my_event_handler = PatternMatchingEventHandler(
            patterns, ignore_patterns, ignore_directories, case_sensitive
        )
        self.my_event_handler.on_created = Watchdog.on_created
        self.path = path
        self.go_recursively = go_recursively

    def run(self):
        self.my_observer = Observer()
        self.my_observer.start()
        self.my_observer.schedule(
            self.my_event_handler, self.path, recursive=self.go_recursively
        )
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.my_observer.stop()
            self.my_observer.join()

email = os.environ.get("GARMIN_EMAIL")
password = keyring.get_password("Garmin", email)
garminConnect = GarminConnectAPI()
garminConnect.login(email, password)

if __name__ == "__main__":
    zwift_dir = os.environ.get("ZWIFT_DIR")
    watchdog = Watchdog(
        path=zwift_dir,
    )
    watchdog.run()
