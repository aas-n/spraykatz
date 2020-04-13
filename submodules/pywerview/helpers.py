# coding: utf-8
#
# This file comes from Pywerview project by Yannick Méheut [yannick (at) meheut (dot) org] - Copyright © 2016
# Slightly modified for Spraykatz.

# Imports
from submodules.pywerview.misc import Misc

def invoke_checklocaladminaccess(target_computername, domain, user, password=str(), lmhash=str(), nthash=str()):
    misc = Misc(target_computername, domain, user, password, lmhash, nthash)
    return misc.invoke_checklocaladminaccess()