import os
import enum


class IMAGETYPE(enum.Enum):
    JPG = ".jpg"
    JPEG = ".jpeg"
    PNG = ".png"
    BMP = ".bmp"
    GIF = ".gif"


class VIDEOTYPE(enum.Enum):
    MP4 = ".mp4"
    MKV = ".mkv"
    AVI = ".avi"
    WMV = ".wmv"
    FLV = ".flv"


def check_file_extension(media_path: str) -> enum.Enum:
    _, extension = os.path.splitext(media_path)
    for i in IMAGETYPE:
        if i.value in media_path:
            return IMAGETYPE
    for i in VIDEOTYPE:
        if i.value in media_path:
            return VIDEOTYPE
