# coding: utf-8
# Author:       @aas_s3curity

# Imports
import logging
from impacket.dcerpc.v5.transport import DCERPCTransportFactory
from impacket.dcerpc.v5.rpcrt import DCERPCException
from impacket.dcerpc.v5.epm import MSRPC_UUID_PORTMAP
from core.Colors import warningRed

def get_os_arch(target):
    try:
        stringBinding = r'ncacn_ip_tcp:{}[135]'.format(target)
        transport = DCERPCTransportFactory(stringBinding)
        transport.set_connect_timeout(5)
        dce = transport.get_dce_rpc()
        dce.connect()

        try:
            dce.bind(MSRPC_UUID_PORTMAP, transfer_syntax=('71710533-BEBA-4937-8319-B5DBEF9CCC36', '1.0'))
        except DCERPCException as e:
            if str(e).find('syntaxes_not_supported') >= 0:
                return 32
            else:
                pass
        else:
            return 64
        dce.disconnect()
    except Exception as e:
        logging.warning('%sErr with get_os_arch for %s: %s' % (warningRed, target, str(e)))
