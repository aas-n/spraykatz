# coding: utf-8
# Author:	@aas_s3curity

# Imports
import re

class User:
	def __init__(self, domain, username, password):
		self.domain = domain
		self.username = username
		if re.search("([a-fA-F\\d]{32}:[a-fA-F\\d]{32})", password):
			self.lmhash, self.nthash = password.split(':')
			self.password = ""
		else:
			self.password = password
			self.lmhash = ""
			self.nthash = ""
