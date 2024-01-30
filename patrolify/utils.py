import time
from .globals import threadlocal


def local_test_setup():
    threadlocal.check_id = str(int(time.time()))
    threadlocal.check_name = "localtest.mychecker"
