import logging

root_logger=logging.getLogger()
print(f"Root Logger: name={root_logger.name}, level={logging.getLevelName(root_logger.level)}")

app_logger=logging.getLogger("app")
print(f"Root Logger: name={app_logger.name}, level={logging.getLevelName(app_logger.level)}, parent={app_logger.parent.name}")

network_logger= logging.getLogger("app.network")
print(f"Root Logger: name={network_logger.name}, level={logging.getLevelName(network_logger.level)},parent={app_logger.parent.name}")



