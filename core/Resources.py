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


def initSpraykatz():
	if not os.path.isdir(tmpDir) : os.mkdir(tmpDir)
	if not os.path.isdir(dumpDir) : os.mkdir(dumpDir)
	return menu()

def joinThreads(davServer, jobs, timeout):
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
	
	if davServer.is_alive():
		davServer.terminate()
		davServer.join()
	logging.debug("%sDavServer thread terminated." % (debugBlue))

def freeSpraykatz(davServer, jobs, timeout):
	joinThreads(davServer, jobs, timeout)
	#for f in os.listdir(tmpDir):
	#	os.remove(os.path.join(tmpDir, f))

	for f in os.listdir(dumpDir):
		os.remove(os.path.join(dumpDir, f))

def exit_gracefully(davServer, jobs):
	logging.warning("\n%sExiting Gracefully..." % (warningGre))
	freeSpraykatz(davServer, jobs, 2)
