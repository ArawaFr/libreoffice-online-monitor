import sys

name = "loolmonitor"

if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    raise Exception("Python 3.6 or a more recent version is required.")
