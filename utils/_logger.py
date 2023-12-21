import sys
from loguru import logger
from pathlib import Path
from loguru import logger as log


class LogInitialization:

    def __init__(self, _level="INFO"):
        project_path = Path.cwd()
        log_path = Path(project_path, "LOG")
        error_log_path = Path(project_path, "ERROR_LOG")

        logger.remove()
        logger.add(
            sys.stderr,
            level=_level,
            format=  # noqa: E251
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> <level>[{level}] [{file.name}:{line}]: {message}</level>",
            enqueue=True)

        logger.add(
            "{}/record.log".format(log_path),
            level=_level,
            format=  # noqa: E251
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> <level>[{level}] [{file.name}:{line}]: {message}</level>",
            rotation="00:00",
            encoding="utf-8",
            retention="1 months",
            enqueue=True)

        logger.add(
            "{}/Error.log".format(error_log_path),
            level="ERROR",
            format=  # noqa: E251
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> - <level>{level}: [{file.name}:{line}] - {message}</level>",
            rotation="5 seconds",
            encoding="utf-8",
            retention="3 days",
            enqueue=True)


# if __name__ == "__main__":
#     LogInitialization()
#     logger.info("info")
#     logger.debug("debug")
#     logger.warning("warning")
#     logger.error("error")
