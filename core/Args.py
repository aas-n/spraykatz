# coding: utf-8

# Author:	Lyderic LEFEBVRE
# Twitter:	@lydericlefebvre
# Mail:		lylefebvre.infosec@gmail.com
# LinkedIn:	https://www.linkedin.com/in/lydericlefebvre


# Imports
import sys, os, argparse
from core.Colors import *
from core.Logs import *
from core.Utils import *

class SpraykatzParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help()
        print("\n%sError: %s\n" % (warningRed, message))
        sys.exit(2)

def parseArgs(parser):
    args = parser.parse_args()

    if os.path.isfile(args.targets):
        args.targets = [line.rstrip('\n') for line in open(args.targets)]
    else:
        args.targets = args.targets.split(',')
    targets = list(skip_duplicates(args.targets))
    args.targets = targets
    setLogging(args.verbosity)

    return args

def menu():
    parser = SpraykatzParser(prog="spraykatz.py", description="A tool to spray love around the world!", epilog="=> Be careful, dumps are retrieved locally! A dump > 40MB. Ten dumps > 400MB.")
    mandatoryArgs = parser.add_argument_group('Mandatory Arguments')
    mandatoryArgs.add_argument("-u", "--username", help="User to spray with. He must have admin rights on targeted systems in order to gain remote code execution.", required=True)
    mandatoryArgs.add_argument("-p", "--password", help="User's password or NTLM hash in the LM:NT format.", required=True)
    mandatoryArgs.add_argument("-t", "--targets", help="IP addresses and/or IP address ranges. You can submit them via a file of targets (one target per line), or inline (separated by commas).", required=True)

    optionalArgs = parser.add_argument_group('Optional Arguments')
    optionalArgs.add_argument("-d", "--domain", help="User's domain. If he is not member of a domain, simply use \"-d .\" instead.", default="")
    optionalArgs.add_argument("-k", "--keep", help="Keep dumps into misc/dumps (no deletion when spraykatz ends).", action="store_true")
    optionalArgs.add_argument("-v", "--verbosity", help="Verbosity mode.", choices=['warning', 'info', 'debug'], default="info")

    return parser
