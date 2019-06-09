#!/usr/bin/env python
# -*- coding: utf8 -*-
# This file is part of PywerView.
# Yannick Méheut [yannick (at) meheut (dot) org] - Copyright © 2016

from submodules.pywerview.misc import Misc

def invoke_checklocaladminaccess(target_computername, domain, user, password=str(), lmhash=str(), nthash=str()):
    misc = Misc(target_computername, domain, user, password, lmhash, nthash)
    return misc.invoke_checklocaladminaccess()