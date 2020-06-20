# coding: utf-8
# Author:	@aas_s3curity

# Imports
import os, sys

# Dirs
homeDir = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])))
dumpDir = os.path.join(homeDir, 'misc', 'dumps')

# Submodules
sys.path.insert(0, os.path.join(homeDir, 'submodules', 'pywerview'))
sys.path.insert(1, os.path.join(homeDir, 'submodules', 'customWmiExec'))
