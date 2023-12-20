import json
import time
import threading
from loguru import logger as log

import websockets
from websockets.sync.client import connect


'''
message format
{
    "action": "sync",
    "id": "schedule_id",
    "data": {
        "media":"xxx.mp4",
        "current":frame_index,  // int
    }
}
'''


class Slave():

    def __init__(self):
        self.ws = None

    def receive(self) -> tuple:
        try:
            message = self.ws.recv()
            return json.loads(message), True
        except websockets.ConnectionClosed:
            return "ConnectionClosed", False
        except json.decoder.JSONDecodeError as e:
            return "Json parse error: {}".format(e), False
        except Exception as e:
            return "Error: {}".format(e), False

        # with connect("ws://localhost:8110") as websocket:
        #     while True:
        #         message = websocket.recv()
        #         try:
        #             self.message = json.loads(message)
        #             log.info(self.message)
        #         except Exception as e:
        #             log.info("json parse error: ", e)
        #             self.message = e

    def connection(self):
        while self.ws is None:
            try:
                log.info("websocket connecting...")
                self.ws = connect("ws://localhost:8110")
            except Exception as e:
                log.info("websocket connect error: ", e)
            time.sleep(3)
        log.info("websocket connected")

    def register_function(self):
        threading.Thread(target=self.connection).start()


if __name__ == "__main__":
    slave = Slave()
    while True:
        res, status = slave.receive()
        log.info(res)
        if not status:
            break
