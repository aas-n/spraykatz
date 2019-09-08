# coding: utf-8

# Author:	Lyderic LEFEBVRE
# Twitter:	@lydericlefebvre
# Mail:		lylefebvre.infosec@gmail.com
# LinkedIn:	https://www.linkedin.com/in/lydericlefebvre


# Imports
import os, logging, sys
from impacket.examples import logger
from impacket import smbserver, version
from impacket.ntlm import compute_lmhash, compute_nthash
from core.Colors import *
from core.Paths import *


def launchSmbServer(q, local_ip, alea, verbosity):
    logging.warning("%sStarting SMB Server..." % (warningGre))

    if verbosity == "debug":
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.WARNING)

    try:
        server = smbserver.SimpleSMBServer(local_ip, 445)
        server.addShare(alea, "misc", "")
        server.setSMB2Support(True)
        lmhash = compute_lmhash(alea)
        nthash = compute_nthash(alea)
        server.addCredential(alea, 0, lmhash, nthash)
        server.setSMBChallenge('')
        server.start()
    except KeyboardInterrupt:
        pass
        #logging.warning("%s   Keyboard interrupt. Exiting SMB Server..." % (warningRed))
    except Exception as e:
        logging.warning("%s   Error: %s" % (warningRed, e))
        logging.warning("%s   A problem occurs when launching SMB server. Common problems:\n\t- port 445 is already in use ?\n\t- You don't have enough privileges" % (warningRed))
    finally:
        q.put(-1)
        exit()
