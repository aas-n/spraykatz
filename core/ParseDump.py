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
from core.Dump import *
from pypykatz.pypykatz import pypykatz


def parseDump(dump):
    credentials = []
    results = {}
    dico = {}

    result = pypykatz.parse_minidump_external(dump)

    for luid in result.logon_sessions:
        try:
            dico = result.logon_sessions[luid].to_dict()

            for cred in result.logon_sessions[luid].msv_creds:
                if '$' not in cred.username:
                    credentials.append((cred.domainname, cred.username, 'NA', (cred.LMHash.hex() if cred.LMHash else 'NA'), (cred.NThash.hex() if cred.NThash else 'NA')))

            for cred in result.logon_sessions[luid].wdigest_creds:
                if cred.password and "TBAL" not in cred.password and '$' not in cred.username:
                    credentials.append((cred.domainname, cred.username, cred.password, 'NA', 'NA'))

            ''' Little bug with this one ?
            for cred in result.logon_sessions[luid].ssp_creds:
                if cred.password and "TBAL" not in cred.password and '$' not in cred.username:
                    credentials.append((cred.domainname, cred.username, cred.password, 'NA', 'NA'))
            '''

            for cred in result.logon_sessions[luid].livessp_creds:
                if cred.password and "TBAL" not in cred.password and '$' not in cred.username:
                    credentials.append((cred.domainname, cred.username, cred.password, 'NA', 'NA'))

            for cred in result.logon_sessions[luid].kerberos_creds:
                if cred.password and "TBAL" not in cred.password and '$' not in cred.username:
                    credentials.append((cred.domainname, cred.username, cred.password, 'NA', 'NA'))

            for cred in result.logon_sessions[luid].credman_creds:
                if cred.password and "TBAL" not in cred.password and '$' not in cred.username:
                    credentials.append((cred.domain, cred.username, cred.password, 'NA', 'NA'))

            for cred in result.logon_sessions[luid].tspkg_creds:
                if cred.password and "TBAL" not in cred.password and '$' not in cred.domainname:
                    credentials.append((cred.username, cred.domainname, cred.password, 'NA', 'NA'))
        except Exception as e:
            logging.warning("%sA problem occurs with target when accessing value (pypykatz). Err: %s" % (warningRed, e))

    credentials = list(skip_duplicates(credentials))

    return credentials
