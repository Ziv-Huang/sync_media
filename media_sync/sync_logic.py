import cv2
import time
import uuid


class MediaSyncHandler():
    def __init__(self) -> None:
        self.id = uuid.uuid4()
        self.cap = None
        self.fps = 0
        self.count = 0
        self.media_path = None

    def get_id(self) -> str:
        return str(self.id)

    def get_media_path(self) -> str:
        return self.media_path

    def load_media(self, media_path) -> bool:
        self.media_path = media_path
        self.cap = cv2.VideoCapture(media_path)
        if not self.cap.isOpened():
            print("Load media failed")
            return False
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        print("Load media success")
        return True

    def render(self, idx: int, frame_name=None):
        while True:
            if self.cap.isOpened():
                ret = self.cap.grab()
                self.count += 1
                if idx == self.count:
                    ret, frame = self.cap.retrieve()
                else:
                    print("skip ", self.count)
                    continue
                if ret:
                    cv2.imshow(frame_name, frame)
                    cv2.waitKey(1)
                return True
                # if cv2.waitKey(1) & 0xFF == ord("q"):
                #     break
                # else:
                #     break
            else:
                print("cap is closed")
                return False

    def monitor_generator(self) -> int:
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            # ret = self.cap.grab()
            if ret:
                yield self.count
                self.count += 1
                # cv2.imshow(str(self.id), frame)
                # if cv2.waitKey(1) & 0xFF == ord('q'):
                #     break
            else:
                break
            time.sleep(1/self.fps)
        print("cap is closed")

    def close(self):
        self.cap.release()
        # cv2.destroyAllWindows()


if __name__ == "__main__":
    mediasync = MediaSyncHandler()
    mediasync.load_media("assets/synctest.mp4")
    # for i in mediasync.monitor_generator():
    #     print(i)
    for i in range(1000):
        mediasync.render(i)
    mediasync.close()
