# coding: utf-8
# Author:	@aas_s3curity

# Imports
import random, string, socket

def skip_duplicates(iterable, key=lambda x: x):
	fingerprints = set()
	for x in iterable:
		fingerprint = key(x)
		if fingerprint not in fingerprints:
			yield x
			fingerprints.add(fingerprint)


def retrieveMyIP():
	return (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]


def gen_random_string(length=10):
	return ''.join(random.sample(string.ascii_letters, int(length)))
