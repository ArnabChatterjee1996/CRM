import logging

#logger configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - File_Name- %(filename)s - Function_Name- %(funcName)s - Line_No- %(lineno)d - %(message)s')
logging.basicConfig(level="INFO")
logging.info("Creating handler")
root = logging.getLogger()
hdlr = root.handlers[0]
json_format = logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}')
hdlr.setFormatter(json_format)