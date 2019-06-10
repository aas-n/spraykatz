# coding: utf-8

# Author:	Lyderic LEFEBVRE
# Twitter:	@lydericlefebvre
# Mail:		lylefebvre.infosec@gmail.com
# LinkedIn:	https://www.linkedin.com/in/lydericlefebvre


# Imports
import logging


def setLogging(quiet):
	formatter = logging.Formatter('%(message)s')
	ch = logging.StreamHandler()
	ch.setFormatter(formatter)

	if quiet : logging.getLogger().setLevel(logging.WARNING)
	else : logging.getLogger().setLevel(logging.INFO)

	logging.getLogger().addHandler(ch)