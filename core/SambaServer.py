# coding: utf-8

# Author:       Lyderic LEFEBVRE
# Twitter:      @lydericlefebvre
# Mail:         lylefebvre.infosec@gmail.com
# LinkedIn:     https://www.linkedin.com/in/lydericlefebvre


###
#
# For Debug Purpose Only
#
###

# Imports
import os, logging, sys
from subprocess import Popen, PIPE

from core.Colors import *
from core.Paths import *


def launchSambaServer(q, local_ip, alea, verbosity):
    logging.warning("%sStarting SAMBA Server..." % (warningGre))

    if verbosity == "debug":
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.WARNING)

    try:
        cmd = "/etc/init.d/smbd stop ; i=\"%s\" ; useradd $i ; (echo $i; echo $i) | smbpasswd -a $i ; sed -i -E \"s/[A-Z]{5}/$i/g\" /etc/samba/smb.conf ; /etc/init.d/smbd restart" % (alea)
        ret = Popen(cmd, stdout=PIPE, shell=True).communicate()[0].decode("utf8").strip()
        print(ret)
    except Exception as e:

        logging.warning("%s   Error: %s" % (warningRed, e))
