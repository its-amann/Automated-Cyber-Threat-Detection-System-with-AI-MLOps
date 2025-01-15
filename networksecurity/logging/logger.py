import logging
import os
from datetime import datetime

logfile = f"{datetime.now().strftime('%m_%d_%Y_H_%M_%S')}.log"

log_path = os.path.join(os.get_cwd(), 'logs', logfile)

os.makedirs(log_path, exist_ok=True)

log_file_path = os.path.join(log_path, logfile)


logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='[%(asctime)s] %(lineno)d - %(name)s - %(levelname)s - %(message)s')