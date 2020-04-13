# coding: utf-8
# Author:	@aas_s3curity

# Imports
import logging, sys, traceback
from core.Colors import warningRed, red, blue, white
from core.Utils import skip_duplicates
from pypykatz.pypykatz import pypykatz

def parseDump(dump, target):
    credentials = []
    result = []

    try:
        result = pypykatz.parse_minidump_external(dump)
        
        for luid in result.logon_sessions:

            for cred in result.logon_sessions[luid].msv_creds:
                if cred.username != None:
                    credentials.append((cred.domainname, cred.username, 'NA', (cred.LMHash.hex() if cred.LMHash else 'NA'), (cred.NThash.hex() if cred.NThash else 'NA')))

            for cred in result.logon_sessions[luid].wdigest_creds:
                if cred.password and type(cred.password) != bytes:
                    if 'TBAL' not in cred.password:
                        credentials.append((cred.domainname, cred.username, cred.password, 'NA', 'NA'))
                        
            for cred in result.logon_sessions[luid].ssp_creds:
                if cred.password and type(cred.password) != bytes:
                    if 'TBAL' not in cred.password:
                        credentials.append((cred.domainname, cred.username, cred.password, 'NA', 'NA'))
                        
            for cred in result.logon_sessions[luid].livessp_creds:
                if cred.password and type(cred.password) != bytes:
                    if 'TBAL' not in cred.password:
                        credentials.append((cred.domainname, cred.username, cred.password, 'NA', 'NA'))
                        
            for cred in result.logon_sessions[luid].kerberos_creds:
                if cred.password and type(cred.password) != bytes:
                    if 'TBAL' not in cred.password:
                        credentials.append((cred.domainname, cred.username, cred.password, 'NA', 'NA'))
                        
            for cred in result.logon_sessions[luid].credman_creds:
                if cred.password and type(cred.password) != bytes:
                    if 'TBAL' not in cred.password:
                        credentials.append(("NA", cred.username, cred.password, 'NA', 'NA'))
                        
            for cred in result.logon_sessions[luid].tspkg_creds:
                if cred.password and type(cred.password) != bytes:
                    if 'TBAL' not in cred.password:
                        credentials.append((cred.username, cred.domainname, cred.password, 'NA', 'NA'))

    except Exception as e:
        logging.warning("%sA problem occurs during the parse of %s%s%s's dump. Err: %s." % (warningRed, red, target, white, e))
        logging.debug("%s==== STACKTRACE ====" % (blue))
        if logging.getLogger().getEffectiveLevel() <= 10: traceback.print_exc(file=sys.stdout)
        logging.debug("%s==== STACKTRACE ====%s" % (blue, white))

    credentials = list(skip_duplicates(credentials))

    return credentials
