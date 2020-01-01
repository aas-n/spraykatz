# coding: utf-8

# Author:	Lyderic LEFEBVRE
# Twitter:	@lydericlefebvre
# Mail:		lylefebvre.infosec@gmail.com
# LinkedIn:	https://www.linkedin.com/in/lydericlefebvre


# Imports
import os, logging, time
from core.Paths import *
from core.Args import *
from core.Colors import *
from core.Logs import *

def initSpraykatz():
    logging.warning("%sHey, did you read the code?\n" % (debugBlue))

def joinThreads(jobs, timeout):
    start = cur_time = time.time()

    while cur_time <= (start + int(timeout)):
        for job in jobs:
            if not job.is_alive():
                job.join()

        if all(not p.is_alive() for p in jobs):
            break
        else:
            time.sleep(1)
            cur_time = time.time()

    if cur_time >= int(timeout):
        for job in jobs:
            job.terminate()
            job.join()

    logging.debug("%sSpray threads terminated." % (debugBlue))

def freeSpraykatz(jobs, timeout):
    joinThreads(jobs, timeout)

def exit_gracefully(jobs, timeout):
    logging.warning("%sExiting Gracefully..." % (warningGre))
    freeSpraykatz(jobs, timeout)
