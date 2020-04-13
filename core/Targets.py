# coding: utf-8
# Author:	@aas_s3curity

# Imports
import logging
from core.Colors import debugBlue, warningRed, warningGre, infoYellow, green, white, red
from core.Timeout import timeout
from subprocess import Popen, PIPE
from multiprocessing import Process, Manager
from submodules.pywerview.helpers import invoke_checklocaladminaccess
from impacket.smbconnection import SessionError


def listSmbTargets(args_targets):
    try:
        smbTargets = Popen("nmap -T3 -sT -Pn -n --open -p135 -oG - %s | grep \"135/open\" | cut -d \" \" -f 2" % (' '.join(args_targets)), stdout=PIPE, shell=True).communicate()[0].decode("utf8").strip().split()
        logging.debug("%sTargets found with nmap: %s" % (debugBlue, smbTargets))
    except Exception as e:
        logging.info("%s%s" % (e))

    if not smbTargets:
        logging.warning("%sNo targets with open port 135 available. Quitting." % (warningRed))
        exit(2) 
    return smbTargets

def listLocalAdminAccess(target, user, pwnableTargets):
        with timeout(5):
            try:
                if invoke_checklocaladminaccess(target, user.domain, user.username, user.password, user.lmhash, user.nthash):
                    logging.info("%s%s is %spwnable%s!" % (infoYellow, target, green, white))
                    pwnableTargets.append(target)
            except SessionError as e:
                error = e.getErrorString()
                logging.info("%s%s is %snot pwnable%s! (%s)" % (infoYellow, target, red, white, error))
            except Exception as e:
                logging.info("%s%s is %snot pwnable%s! (%s)" % (infoYellow, target, red, white, e))

def listPwnableTargets(args_targets, user):
    logging.warning("%sListing targetable machines into networks provided. Can take a while..." % (warningGre))
    pwnableTargets = []

    targets = listSmbTargets(args_targets)
    
    logging.warning("%sChecking local admin access on targets..." % (warningGre))
    with Manager() as manager:
        try:
            managerTargets = manager.list()
            processes = []
            for smbTarget in targets:
                p = Process(target=listLocalAdminAccess, args=(smbTarget, user, managerTargets))
                p.start()
                processes.append(p)
        except Exception as e:
	        logging.warning("%sErr: %s" % (warningRed, e))
        finally:
            for p in processes:
                p.join()
                
            pwnableTargets = [x for x in managerTargets]
    
    if not pwnableTargets:
        logging.warning("%sNo pwnable targets. Quitting." % (warningRed))
        exit(2)
    
    return pwnableTargets
