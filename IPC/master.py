import asyncio
import websockets
import threading
import time


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


class Master():

    def __init__(self):
        self.clients = set()

    def register(self, websocket):
        self.clients.add(websocket)

    def unregister(self, websocket):
        self.clients.remove(websocket)

    def broadcast(self, message):
        websockets.broadcast(self.clients, message)

    async def entry(self, websocket):
        try:
            self.register(websocket)
            async for message in websocket:
                print(message)
                await websocket.send(message)
            await websocket.wait_closed()
        finally:
            self.unregister(websocket)

    async def loop_broadcast(self, message):
        while True:
            print(self.clients)
            websockets.broadcast(self.clients, message)
            await asyncio.sleep(1)

    async def launch_server(self):
        async with websockets.serve(self.entry, "localhost", 8110):
            # await self.loop_broadcast("Hello world!")
            print("localhost: {} server start".format(8110))
            await asyncio.Future()  # run forever

    def register_function(self):
        threading.Thread(target=asyncio.run, args=(self.launch_server(),)).start()


if __name__ == "__main__":
    master = Master()
    master.register_function()
    time.sleep(1000)
    # threading.Thread(target=master.broadcast, args=("Hello world!",)).start()
    # asyncio.run(master.start_broadcast())
