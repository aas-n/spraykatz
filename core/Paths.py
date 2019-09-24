# coding: utf-8

# Author:	Lyderic LEFEBVRE
# Twitter:	@lydericlefebvre
# Mail:		lylefebvre.infosec@gmail.com
# LinkedIn:	https://www.linkedin.com/in/lydericlefebvre


# Imports
import os, sys


# Dirs
homeDir = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])))
tmpDir = os.path.join(homeDir, 'misc', 'tmp')
dumpDir = os.path.join(homeDir, 'misc', 'dumps')

# Submodules
sys.path.insert(0, os.path.join(homeDir, 'submodules', 'impacket'))
sys.path.insert(1, os.path.join(homeDir, 'submodules', 'pywerview'))
sys.path.insert(2, os.path.join(homeDir, 'submodules', 'customWmiExec'))
