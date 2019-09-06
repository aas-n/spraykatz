# coding: utf-8

# Author:	Lyderic LEFEBVRE
# Twitter:	@lydericlefebvre
# Mail:		lylefebvre.infosec@gmail.com
# LinkedIn:	https://www.linkedin.com/in/lydericlefebvre


# Imports
import logging


def setLogging(verbosity):
	formatter = logging.Formatter('%(message)s')
	ch = logging.StreamHandler()
	ch.setFormatter(formatter)

	if verbosity == "warning":
		logging.getLogger().setLevel(logging.WARNING)
	elif verbosity == "info":
		logging.getLogger().setLevel(logging.INFO)
	else:
		logging.getLogger().setLevel(logging.DEBUG)

	logging.getLogger().addHandler(ch)
