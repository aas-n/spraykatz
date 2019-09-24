#!/usr/bin/env python3
# coding: utf-8

# Author:	Lyderic LEFEBVRE
# Twitter:	@lydericlefebvre
# Mail:		lylefebvre.infosec@gmail.com
# LinkedIn:	https://www.linkedin.com/in/lydericlefebvre


# Imports
import os
from core.Colors import *
from core.Resources import *
from core.Engine import *
from core.Args import *

def printBanner():
	''' Print the tool banner '''
	os.system("clear")
	print ("")
	print ("███████╗██████╗ ██████╗  █████╗ ██╗   ██╗██╗  ██╗ █████╗ ████████╗███████╗")
	print ("██╔════╝██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝██║ ██╔╝██╔══██╗╚══██╔══╝╚══███╔╝")
	print ("███████╗██████╔╝██████╔╝███████║ ╚████╔╝ █████╔╝ ███████║   ██║     ███╔╝ ")
	print ("╚════██║██╔═══╝ ██╔══██╗██╔══██║  ╚██╔╝  ██╔═██╗ ██╔══██║   ██║    ███╔╝  ")
	print ("███████║██║     ██║  ██║██║  ██║   ██║   ██║  ██╗██║  ██║   ██║   ███████╗")
	print ("╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝%sv0.9.1%s" % (green, white))
	print ("                                                                          ")
	print ("                    Written by %s@lydericlefebvre%s                       " % (red, white))
	print ("                                                                          ")


if __name__ == '__main__':
	printBanner()
	args = parseArgs(menu())
	initSpraykatz()

	# Fire!
	run(args)
