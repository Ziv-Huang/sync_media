import os
import time
import threading
import setproctitle
from loguru import logger as log

from utils._logger import LogInitialization
from utils.args import parse_args
from broadcast import Broadcaster, Subscriber


schedule_id = ["aaaaa", "bbbbb"]

play_list = {
             schedule_id[0]: [
                "assets/SnapSave.io-202230sec_-1080p.mp4",
                "assets/2.mp4"],
             schedule_id[1]: [
                "assets/2.mp4",
                "assets/SnapSave.io-202230sec_-1080p.mp4"
                ]
            }


def play(broadcaster, player_id, play_list):
    for v in play_list:
        broadcaster.player_load_media(player_id, v)
        broadcaster.broadcast(broadcaster.sync_handlers[player_id])


def broadcast():
    broadcaster = Broadcaster()
    broadcaster.register_function()
    broadcaster.add_player(schedule_id)

    test1 = threading.Thread(target=play, args=(broadcaster, schedule_id[0], play_list[schedule_id[0]]))
    test2 = threading.Thread(target=play, args=(broadcaster, schedule_id[1], play_list[schedule_id[1]]))

    test1.start()
    test2.start()
    test1.join()
    test2.join()
    log.info("broadcast end")


def subscribe():
    subscriber = Subscriber(schedule_id[0])
    log.info("subscriber id: ", subscriber.id)
    subscriber.register_function()
    subscriber.receive()


if __name__ == "__main__":
    setproctitle.setproctitle("sync media")
    LogInitialization("DEBUG")
    log.info("process name: {}, pid: {}".format("sync media", os.getppid()))
    args = parse_args()
    if args.broadcast:
        broadcast()
    if args.subscribe:
        subscribe()
