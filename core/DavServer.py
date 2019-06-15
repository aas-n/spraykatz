# coding: utf-8

# Author:	Lyderic LEFEBVRE
# Twitter:	@lydericlefebvre
# Mail:		lylefebvre.infosec@gmail.com
# LinkedIn:	https://www.linkedin.com/in/lydericlefebvre


# Imports
import os, logging, pexpect
from core.Colors import *
from core.Paths import *


def launchDavServer(q, port):
	try:
		logging.warning("%sStarting WebDAV Server." % (warningGre))
		os.chdir(homeDir)
		child = pexpect.spawn('wsgidav --host=0.0.0.0 --port=%s --root=. --auth=anonymous --server=gevent' % (int(port)), timeout=10)
		child.expect('Serving on ')
		st = child.read_nonblocking(timeout=2)
	except pexpect.TIMEOUT:
		logging.info("%s   WebDAV Server successfuly launched." % (infoYellow))
		q.put(0)
		child.expect(pexpect.EOF, timeout=None)
	except KeyboardInterrupt:
		logging.warning("%s   Keyboard interrupt. Exiting WebDAV Server..." % (warningRed))
	except Exception as e:
		logging.warning("%s   Error: %s" % (warningRed, e))
	finally:
		logging.warning("%s   A problem occurs when launching WebDAV server. Common problems:\n\t- port 80 is already in use ?\n\t- You don't have enough privileges" % (warningRed))
		q.put(1337)
		child.close()
		exit()