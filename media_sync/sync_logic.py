import cv2
import time
from loguru import logger as log


class MediaSyncHandler():
    def __init__(self, id: str) -> None:
        self.id = id
        self.cap = None
        self.fps = 0
        self.count = 0
        self.media_path = None

    def get_id(self) -> str:
        return str(self.id)

    def get_media_path(self) -> str:
        return self.media_path

    def load_media(self, media_path) -> bool:
        self.count = 0
        self.media_path = media_path
        self.cap = cv2.VideoCapture(media_path)
        if not self.cap.isOpened():
            log.warning("Load media failed, skip this media...")
            return False
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        log.info("Load media success")
        return True

    def render(self, idx: int, frame_name=None):
        while True:
            if self.cap.isOpened():
                ret = self.cap.grab()
                self.count += 1
                if idx < self.count:
                    ret, frame = self.cap.retrieve()
                else:
                    # log.info("skip: {}".format(self.count))
                    continue
                if ret:
                    cv2.imshow(frame_name, frame)
                    cv2.waitKey(1)
                time.sleep(1/self.fps)
                return True
                # if cv2.waitKey(1) & 0xFF == ord("q"):
                #     break
                # else:
                #     break
            else:
                log.info("cap is closed, next video")
                return False

    def monitor_generator(self) -> int:
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            # ret = self.cap.grab()
            if ret:
                if self.count % int(self.fps) == 0:
                    yield self.count
                self.count += 1
                # cv2.imshow(str(self.id), frame)
                # if cv2.waitKey(1) & 0xFF == ord('q'):
                #     break
            else:
                break
            time.sleep(1/self.fps)
        log.info("cap is closed")

    def close(self):
        self.cap.release()
        # cv2.destroyAllWindows()


if __name__ == "__main__":
    mediasync = MediaSyncHandler()
    mediasync.load_media("assets/synctest.mp4")
    # for i in mediasync.monitor_generator():
    #     log.info(i)
    for i in range(1000):
        mediasync.render(i)
    mediasync.close()
