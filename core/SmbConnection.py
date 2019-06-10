# coding: utf-8

# Author:	Lyderic LEFEBVRE
# Twitter:	@lydericlefebvre
# Mail:		lylefebvre.infosec@gmail.com
# LinkedIn:	https://www.linkedin.com/in/lydericlefebvre


# Imports
import socket
from core.Colors import *
from impacket.smbconnection import SMBConnection, SessionError
from impacket.smb import SMB_DIALECT


class SmbConnection:
	def __init__(self):
		self.smbConnection = None
		self.smbv1 = None

	def create_smbv1_conn(self, target):
		try:
			self.smbConnection = SMBConnection(target, target, None, 445, preferredDialect=SMB_DIALECT)
			self.smbv1 = True
		except socket.error as e:
			if str(e).find('Connection reset by peer') != -1:
				logging.warning("%sSMBv1 might be disabled on %s%s%s" % (warningRed, target, white))
			return False
		except Exception as e:
			#logging.warning("%sError creating SMBv1 connection to %s%s%s: %s" % (warningRed, red, target, white, e))
			return False
		return True

	def create_smbv3_conn(self, target):
		try:
			self.smbConnection = SMBConnection(target, target, None, 445)
			self.smbv1 = False
		except socket.error:
			return False
		except Exception as e:
			loggin.warning("%sError creating SMBv3 connection to %s%s%s: %s" % (warningRed, red, target, white, e))
			return False
		return True

	def create_conn_obj(self, target):
		if self.create_smbv1_conn(target):
			return True
		elif self.create_smbv3_conn(target):
			return True
		return False