import time
import uuid
import json
import threading
from loguru import logger as log

from IPC import Master
from media_sync import MediaSyncHandler


class Broadcaster():
    def __init__(self):
        self.master = Master()
        self.sync_handlers: dict[str, MediaSyncHandler] = dict()

    def add_player(self, players: list):
        for p in players:
            sync_handler = MediaSyncHandler(p)
            self.sync_handlers[p] = sync_handler

    def player_load_media(self, player_idx, media_path):
        self.sync_handlers[player_idx].load_media(media_path)

    def broadcast(self, sync_handler: MediaSyncHandler) -> bool:
        try:
            monitor = sync_handler.monitor_generator()
            for i in monitor:
                # log.info(sync_handler.get_media_path()+": "+str(i))
                message = {
                    "action": "sync",
                    "id": sync_handler.get_id(),  # schedule_id or list_id
                    "data": {
                        "media": sync_handler.get_media_path(),
                        "frame_index": i
                    }
                }
                self.master.broadcast(json.dumps(message))
                # log.info("{}: {}".format(sync_handler, i))
        except Exception:
            return False
        return True

    def pipeline(self):
        for sync_handler in self.sync_handlers:
            log.info("sync_handler: ", sync_handler.get_media_path())
            threading.Thread(target=self.broadcast, args=(sync_handler,)).start()

    def heartbeat(self):
        while True:
            log.info("heartbeat")
            time.sleep(5*60)  # 5 minutes

    def register_function(self):
        self.master.register_function()
        threading.Thread(target=self.heartbeat).start()


if __name__ == "__main__":
    broadcaster = Broadcaster()
    broadcaster.add_player("assets/synctest.mp4")
    broadcaster.pipeline()
    broadcaster.register_function()
