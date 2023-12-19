import time
from utils.args import parse_args
from broadcast import Broadcaster, Subscriber


if __name__ == "__main__":
    args = parse_args()
    if args.broadcast:
        broadcaster = Broadcaster()
        broadcaster.add_player("assets/synctest.mp4")
        broadcaster.add_player("assets/video2.mp4")
        # broadcaster.add_player("assets/2.mp4")
        broadcaster.pipeline()
        broadcaster.register_function()
    if args.subscribe:
        subscriber = Subscriber()
        print("subscriber id: ", subscriber.id)
        subscriber.player.load_media("assets/synctest.mp4")
        # subscriber.player.load_media("assets/video2.mp4")
        subscriber.register_function()
        subscriber.receive()
