import os
import time

import helpers.constants as tc


def start():
    """starts behavior subsystem as a detached process using same start script used to start on the bot"""
    cmd = f"LOG_ALL_MESSAGES=1 HUB_PORT={tc.CENTRAL_HUB_TEST_PORT} poetry run ./start.sh behavior"
    exit_code = os.system(cmd)
    assert exit_code == 0
    time.sleep(1)


def stop():
    """stops behavior subsystem"""
    exit_code = os.system("./stop.sh behavior")

    # note that this only shows up when a test module fails
    print("\nBehavior subsystem logs")
    print("===================================================================")
    os.system("cat logs/behavior.log")
    print("===================================================================")

    assert exit_code == 0
