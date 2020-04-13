# coding: utf-8
# Author:      @aas_s3curity

# Imports
from __future__ import division
from __future__ import print_function

import logging
from core.Colors import debugBlue
from impacket.smbconnection import SMBConnection, SMB_DIALECT, SMB2_DIALECT_002, SMB2_DIALECT_21

class Connection:
    def __init__(self, username='', password='', domain='', hashes=None, aesKey=None, share='ADMIN$', noOutput=False, doKerberos=False, kdcHost=None):
        self.__username = username
        self.__password = password
        self.__domain = domain
        self.__lmhash = ''
        self.__nthash = ''
        self.__aesKey = aesKey
        self.__share = share
        self.__noOutput = noOutput
        self.__doKerberos = doKerberos
        self.__kdcHost = kdcHost
        self.shell = None
        if hashes is not None:
            self.__lmhash, self.__nthash = hashes.split(':')

    def run(self, addr):
        smbConnection = SMBConnection(addr, addr)
        smbConnection.login(self.__username, self.__password, self.__domain, self.__lmhash, self.__nthash)

        dialect = smbConnection.getDialect()
        if dialect == SMB_DIALECT:
            logging.debug("%sSMBv1 dialect used" % (debugBlue))
        elif dialect == SMB2_DIALECT_002:
            logging.debug("%sSMBv2.0 dialect used" % (debugBlue))
        elif dialect == SMB2_DIALECT_21:
            logging.debug("%sSMBv2.1 dialect used" % (debugBlue))
        else:
            logging.debug("%sSMBv3.0 dialect used" % (debugBlue))

        return smbConnection
