from infra.config import config
from datetime import datetime, timedelta
import time

timestamp1 = datetime.now()
time.sleep(2)
timestamp2 = datetime.now()
difference = abs(timestamp1 - timestamp2)


print(   difference > timedelta(seconds=3)   )
# print(datetime.now())