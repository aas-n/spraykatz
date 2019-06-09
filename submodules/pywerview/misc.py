# -*- coding: utf8 -*-
# This file is part of PywerView.
# Yannick Méheut [yannick (at) meheut (dot) org] - Copyright © 2016

from submodules.impacket.impacket.dcerpc.v5.rpcrt import DCERPCException
from submodules.impacket.impacket.dcerpc.v5 import scmr
from submodules.pywerview.requester import LDAPRPCRequester

class Misc(LDAPRPCRequester):
    @LDAPRPCRequester._rpc_connection_init(r'\svcctl')
    def invoke_checklocaladminaccess(self):
        try:
            ans = scmr.hROpenSCManagerW(self._rpc_connection, '{}\x00'.format(self._target_computer), 'ServicesActive\x00', 0xF003F)
        except DCERPCException:
            return False
        return True
