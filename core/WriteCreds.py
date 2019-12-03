# coding: utf-8

# Author:       Lyderic LEFEBVRE
# Twitter:      @lydericlefebvre
# Mail:         lylefebvre.infosec@gmail.com
# LinkedIn:     https://www.linkedin.com/in/lydericlefebvre


# Imports
import logging
from core.Colors import *
from core.Paths import *

def write_credentials(target, credentials):
    credsFile = open(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'misc', 'results', 'creds.txt'), 'a')
    
    for credential in credentials:
        credsFile.write("%s:%s:%s" % (target, credential[0], credential[1]))
        if credential[2] is not 'NA':
            credsFile.write(":%s" % (credential[2]))
        else:
            credsFile.write(":")
        if credential[3] is not 'NA':
            credsFile.write(":%s" % (credential[3]))
        else:
            credsFile.write(":")
        if credential[4] is not 'NA':
            credsFile.write(":%s" % (credential[4]))
        
        credsFile.write("\n")
