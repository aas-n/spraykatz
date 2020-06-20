#!/usr/bin/env python3
# coding: utf-8

# Author:	@aas_s3curity


# Imports
import os
from core.Colors import green, white, red
from core.Args import parseArgs, menu
from core.Resources import initSpraykatz
from core.Engine import run


def printBanner():
	''' Print the tool banner '''
	#os.system("clear")
	print ("")
	print ("███████╗██████╗ ██████╗  █████╗ ██╗   ██╗██╗  ██╗ █████╗ ████████╗███████╗")
	print ("██╔════╝██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝██║ ██╔╝██╔══██╗╚══██╔══╝╚══███╔╝")
	print ("███████╗██████╔╝██████╔╝███████║ ╚████╔╝ █████╔╝ ███████║   ██║     ███╔╝ ")
	print ("╚════██║██╔═══╝ ██╔══██╗██╔══██║  ╚██╔╝  ██╔═██╗ ██╔══██║   ██║    ███╔╝  ")
	print ("███████║██║     ██║  ██║██║  ██║   ██║   ██║  ██╗██║  ██║   ██║   ███████╗")
	print ("╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝%sv0.9.9%s" % (green, white))
	print ("                                                                          ")
	print ("                    Written by %s@aas_s3curity%s                       " % (red, white))
	print ("                                                                          ")


if __name__ == '__main__':
	printBanner()
	args = parseArgs(menu())
	initSpraykatz()

	# Fire!
	run(args)
