# coding: utf-8
# Author:      @aas_s3curity

# Imports
from core.Colors import green, white

def print_credentials(target, credentials):
    for credential in credentials:
        print("")
        print("\t\t machine: ", target)
        if credential[0] != 'NA':
            print("\t\t  domain: ", credential[0])
        print("\t\tusername: ", credential[1])
        if credential[2] != 'NA':
            print("\t\tpassword:  %s%s%s" % (green, credential[2], white))
        if credential[3] != 'NA':
            print("\nlmhash: \t%s%s%s" % (green, credential[3], white))
        if credential[4] != 'NA':
            print("\t\t  nthash:  %s%s%s" % (green, credential[4], white))
    
    print("")
