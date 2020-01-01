# coding: utf-8

# Author:       Lyderic LEFEBVRE
# Twitter:      @lydericlefebvre
# Mail:         lylefebvre.infosec@gmail.com
# LinkedIn:     https://www.linkedin.com/in/lydericlefebvre


# Imports
from core.Colors import *

def print_credentials(target, credentials):
    for credential in credentials:
        print("")
        print("\t\t machine: ", target)
        if credential[0] is not 'NA':
            print("\t\t  domain: ", credential[0])
        print("\t\tusername: ", credential[1])
        if credential[2] is not 'NA':
            print("\t\tpassword:  %s%s%s" % (green, credential[2], white))
        if credential[3] is not 'NA':
            print("\nlmhash: \t%s%s%s" % (green, credential[3], white))
        if credential[4] is not 'NA':
            print("\t\t  nthash:  %s%s%s" % (green, credential[4], white))
    
    print("")
