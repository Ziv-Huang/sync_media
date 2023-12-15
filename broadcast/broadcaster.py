import time
import json
import threading

from IPC import Master
from media_sync import MediaSyncHandler


class Broadcaster():
    def __init__(self):
        self.master = Master()
        self.sync_handlers: list[MediaSyncHandler] = list()

    def add_player(self, media_path):
        sync_handler = MediaSyncHandler()
        sync_handler.load_media(media_path)
        self.sync_handlers.append(sync_handler)

    def broadcast(self, sync_handler: MediaSyncHandler):
        monitor = sync_handler.monitor_generator()
        for i in monitor:
            message = {
                "action": "sync",
                "id": sync_handler.get_media_path(),  # schedule_id or list_id
                "data": {
                    "media": sync_handler.get_media_path(),
                    "frame_index": i
                }
            }
            self.master.broadcast(json.dumps(message))
            # print("{}: {}".format(sync_handler, i))

    def pipeline(self):
        for sync_handler in self.sync_handlers:
            threading.Thread(target=self.broadcast, args=(sync_handler,)).start()

    def heartbeat(self):
        while True:
            print("heartbeat")
            time.sleep(5*60)  # 5 minutes

    def launch(self):
        self.master.register_function()
        self.heartbeat()


if __name__ == "__main__":
    broadcaster = Broadcaster()
    # broadcaster.add_player("assets/2.mp4")
    broadcaster.add_player("assets/synctest.mp4")
    broadcaster.pipeline()
    broadcaster.launch()
