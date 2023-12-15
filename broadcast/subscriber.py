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
            message, status = self.slave.receive()
            if status:
                self.render(message)
            else:
                print("Error: ", message)
                time.sleep(5)

    def render(self, message):
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
        print(message)
        frame_index = message["data"]["frame_index"]
        self.player.render(frame_index, self.id)

    def register_function(self, config=None):
        self.player.load_media("assets/synctest.mp4")
        self.slave.register_function()


if __name__ == "__main__":
    subscriber = Subscriber()
    subscriber.register_function()
    subscriber.receive()
