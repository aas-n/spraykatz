# coding: utf-8
# Author:   @aas_s3curity

# Imports
import os, sys

def write_credentials(target, credentials):
    credsFile = open(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'misc', 'results', 'creds.txt'), 'a')
    
    for credential in credentials:
        credsFile.write("%s" % (target))
        if credential[0] != 'NA':
            credsFile.write(":%s" % (credential[0]))
        credsFile.write(":%s" % (credential[1]))
        if credential[2] != 'NA':
            credsFile.write(":%s" % (credential[2]))
        else:
            credsFile.write(":")
        if credential[3] != 'NA':
            credsFile.write(":%s" % (credential[3]))
        else:
            credsFile.write(":")
        if credential[4] != 'NA':
            credsFile.write(":%s" % (credential[4]))
        
        credsFile.write("\n")
