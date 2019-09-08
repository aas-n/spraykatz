# coding: utf-8

# Author:	Lyderic LEFEBVRE
# Twitter:	@lydericlefebvre
# Mail:		lylefebvre.infosec@gmail.com
# LinkedIn:	https://www.linkedin.com/in/lydericlefebvre


# Imports
import logging
from core.Colors import *
from core.Timeout import *
from subprocess import Popen, PIPE
from helpers import invoke_checklocaladminaccess


def listSmbTargets(args_targets):
    ''' List targetable machines '''
    smbTargets = Popen("nmap -T4 -Pn -n --open -p135 -oG - %s | awk '$NF~/msrpc/{print $2}'" % (' '.join(args_targets)), stdout=PIPE, shell=True).communicate()[0].decode("utf8").strip().split()
    if not smbTargets:
        logging.warning("%sNo targets with open port 135 available. Quitting." % (warningRed))
        exit(2)
    return smbTargets

def listPwnableTargets(args_targets, user):
    logging.warning("%sListing targetable machines into networks provided. Can take a while..." % (warningGre))
    pwnableTargets = []
    targets = []
    
    for smbTarget in listSmbTargets(args_targets):
        with timeout(1):
            try:
                if invoke_checklocaladminaccess(smbTarget, user.domain, user.username, user.password, user.lmhash, user.nthash):
                    logging.info("%s%s is %spwnable%s!" % (infoYellow, smbTarget, green, white))
                    pwnableTargets.append(smbTarget)
            except Exception as e:
                logging.debug("%s%s: %s" % (debugBlue, smbTarget, e))
                logging.info("%s%s is %snot pwnable%s!" % (infoYellow, smbTarget, red, white))
                
    if not pwnableTargets:
        logging.warning("%sNo pwnable targets. Quitting." % (warningRed))
        exit(2)
    
    return pwnableTargets
