# -*- coding: utf8 -*-
# coding: utf-8
#
# This file comes from Pywerview project by Yannick Méheut [yannick (at) meheut (dot) org] - Copyright © 2016
# Slightly modified for Spraykatz.

# Imports
from submodules.pywerview.requester import LDAPRPCRequester
from impacket.dcerpc.v5.rpcrt import DCERPCException
from impacket.dcerpc.v5 import scmr

class Misc(LDAPRPCRequester):
    @LDAPRPCRequester._rpc_connection_init(r'\svcctl')
    def invoke_checklocaladminaccess(self):
        try:
            scmr.hROpenSCManagerW(self._rpc_connection, '{}\x00'.format(self._target_computer), 'ServicesActive\x00', 0xF003F)
        except DCERPCException:
            return False
        return True
