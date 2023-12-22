import cv2
import time
from loguru import logger as log

from . import media_utils


class MediaSyncHandler():
    def __init__(self, id: str) -> None:
        self.id = id
        self.media_type = None
        self.cap = None
        self.fps = 0  # for video
        self.sec = 0  # for image
        self.count = 0
        self.media_path = None
        self.adjust_rate = 10
        self.frame_name = None

    def get_id(self) -> str:
        return str(self.id)

    def get_media_sec(self) -> int:
        return self.sec

    def get_media_path(self) -> str:
        return self.media_path

    def load_media(self, media: dict) -> bool:
        self.count = 0
        self.sec = media["sec"]
        self.media_path = media["media"]
        self.media_type = media_utils.check_file_extension(self.media_path)

        if self.media_type == media_utils.IMAGETYPE:
            self.cap = cv2.imread(self.media_path)
            if self.cap is None:
                log.warning("Load media failed, skip this media...")
                return False
            self.fps = -1
        elif self.media_type == media_utils.VIDEOTYPE:
            self.cap = cv2.VideoCapture(self.media_path)
            if not self.cap.isOpened():
                log.warning("Load media failed, skip this media...")
                return False
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        else:
            log.warning("Unsupported media type: {}".format(self.media_path))
            return False
        log.info("Load media success")
        return True

    def render(self, idx: int, frame_name: str = None) -> bool:
        if self.frame_name is None:
            self.frame_name = frame_name
            cv2.namedWindow(frame_name, cv2.WINDOW_NORMAL)
            cv2.setWindowProperty(frame_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        while True:
            if self.media_type == media_utils.IMAGETYPE:
                if self.cap is None:
                    log.info("cap is closed, next media")
                    return False
                cv2.imshow(frame_name, self.cap)  # show image
                cv2.waitKey(1)
                return True
            if self.media_type == media_utils.VIDEOTYPE:
                if not self.cap.isOpened():
                    log.warning("cap is closed, next media")
                    return False
                ret = self.cap.grab()
                self.count += 1
                if idx - self.count > self.fps:
                    # log.info("skip: {}".format(self.count))
                    continue

                ret, frame = self.cap.retrieve()
                if ret:
                    cv2.imshow(frame_name, frame)
                    cv2.waitKey(1)
                if idx < self.count:
                    time.sleep(1/self.fps)
                else:
                    time.sleep(1/self.fps/self.adjust_rate)
                return True
                # if cv2.waitKey(1) & 0xFF == ord("q"):
                #     break
                # else:
                #     break

    def monitor_generator(self) -> int:
        start_time = time.time()
        while True:
            if self.media_type == media_utils.IMAGETYPE:
                if self.cap is None:
                    break
                if time.time() - start_time > self.sec:
                    break
                if self.count % self.adjust_rate == 0:
                    yield self.count
                self.count += 1
                time.sleep(1/self.adjust_rate)
                # cv2.imshow(str(self.id), self.cap)
                # if cv2.waitKey(1) & 0xFF == ord('q'):
                #     break
            elif self.media_type == media_utils.VIDEOTYPE:
                if not self.cap.isOpened():
                    break
                ret, frame = self.cap.read()
                if ret:
                    if self.count % int(self.fps/self.adjust_rate) == 0:  # sync rate
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
        try:
            self.cap.release()
            cv2.destroyAllWindows()
        except Exception:
            pass


if __name__ == "__main__":
    mediasync = MediaSyncHandler()
    mediasync.load_media("assets/synctest.mp4")
    # for i in mediasync.monitor_generator():
    #     log.info(i)
    for i in range(1000):
        mediasync.render(i)
    mediasync.close()
