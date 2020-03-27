#!/usr/bin/env python3
# coding: utf-8

# Author:	@aas_s3curity


# Imports
import os
from core.Colors import *
from core.Resources import *
from core.Engine import *
from core.Args import *

def printBanner():
	''' Print the tool banner '''
	#os.system("clear")
	print ("")
	print ("███████╗██████╗ ██████╗  █████╗ ██╗   ██╗██╗  ██╗ █████╗ ████████╗███████╗")
	print ("██╔════╝██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝██║ ██╔╝██╔══██╗╚══██╔══╝╚══███╔╝")
	print ("███████╗██████╔╝██████╔╝███████║ ╚████╔╝ █████╔╝ ███████║   ██║     ███╔╝ ")
	print ("╚════██║██╔═══╝ ██╔══██╗██╔══██║  ╚██╔╝  ██╔═██╗ ██╔══██║   ██║    ███╔╝  ")
	print ("███████║██║     ██║  ██║██║  ██║   ██║   ██║  ██╗██║  ██║   ██║   ███████╗")
	print ("╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝%sv0.9.8%s" % (green, white))
	print ("                                                                          ")
	print ("                    Written by %s@aas_s3curity%s                       " % (red, white))
	print ("                                                                          ")


if __name__ == '__main__':
	args = parseArgs(menu())
	printBanner()
	initSpraykatz()

	# Fire!
	run(args)
