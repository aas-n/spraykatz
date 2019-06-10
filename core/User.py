# coding: utf-8

# Author:	Lyderic LEFEBVRE
# Twitter:	@lydericlefebvre
# Mail:		lylefebvre.infosec@gmail.com
# LinkedIn:	https://www.linkedin.com/in/lydericlefebvre


# Imports
import re


class User:
	def __init__(self, domain, username, password):
		self.domain = domain
		self.username = username
		if re.search("([a-fA-F\d]{32}:[a-fA-F\d]{32})", password):
			self.lmhash, self.nthash = password.split(':')
			self.password = ""
		else:
			self.password = password
			self.lmhash = ""
			self.nthash = ""