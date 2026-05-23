import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger("closira")

logger.setLevel(logging.INFO)

if not logger.handlers:

    handler = logging.StreamHandler()

    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(message)s"
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)