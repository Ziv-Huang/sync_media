import time
import uuid

from IPC import Slave
from media_sync import MediaSyncHandler


class Subscriber():
    def __init__(self):
        self.slave = Slave()
        self.player = MediaSyncHandler()
        self.id = str(uuid.uuid4())

    def receive(self):
        while True:
            '''
            message format
            {
                "action": "sync",
                "id": "schedule_id",
                "data": {
                    "mdeia":"xxx.mp4",
                    "frame_index":frame_index,  // int
                }
            }
            '''
            message, status = self.slave.receive()
            if status:
                if message["id"] != self.player.get_media_path():
                    continue
                self.render(message)
            else:
                print("Error: ", message)
                time.sleep(5)

    def render(self, message):
        print(message)
        frame_index = message["data"]["frame_index"]
        self.player.render(frame_index, self.id)

    def register_function(self, config=None):
        self.slave.register_function()


if __name__ == "__main__":
    subscriber = Subscriber()
    subscriber.player.load_media("assets/synctest.mp4")
    subscriber.register_function()
    subscriber.receive()
