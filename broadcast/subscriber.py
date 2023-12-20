import time
import uuid
import threading
from loguru import logger as log

from IPC import Slave
from media_sync import MediaSyncHandler


class Subscriber():
    def __init__(self, player_id):
        self.slave = Slave()
        self.player = MediaSyncHandler(player_id)
        self.id = str(uuid.uuid4())

    def receive(self):
        while True:
            '''
            message format
            {
                "action": "sync",
                "id": "schedule_id",
                "data": {
                    "media":"xxx.mp4",
                    "frame_index":frame_index,  // int
                }
            }
            '''
            message, status = self.slave.receive()
            if status:
                if message["id"] != self.player.get_id():
                    continue
                self.render(message)
            else:
                log.warning("receive error: ", message)
                time.sleep(1)

    def render(self, message):
        log.info(message)
        frame_index = message["data"]["frame_index"]
        if self.player.get_media_path() != message["data"]["media"]:
            self.player.load_media(message["data"]["media"])
            log.info("load media: ", message["data"]["media"])
        self.player.render(frame_index, "sub_"+self.id)

    def heartbeat(self):
        while True:
            log.info("heartbeat")
            time.sleep(5*60)  # 5 minutes

    def register_function(self, config=None):
        self.slave.register_function()
        threading.Thread(target=self.heartbeat).start()


if __name__ == "__main__":
    subscriber = Subscriber()
    # subscriber.player.load_media("assets/synctest.mp4")
    subscriber.register_function()
    subscriber.receive()
