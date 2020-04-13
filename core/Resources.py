# coding: utf-8
# Author:	@aas_s3curity

# Imports
import os, sys, logging, time
import wget, zipfile
from core.Colors import debugBlue, infoYellow, warningRed, warningGre

def initSpraykatz():
    logging.warning("%sHey, did you read the code?\n" % (debugBlue))

    # Ensure procdump binaries are available to be used by Spraykatz.
    procdumpPath = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'misc', 'procdump')
    procdumpZip = os.path.join(procdumpPath, 'procdump.zip')
    procdump32 = os.path.join(procdumpPath, 'procdump32.exe')
    procdump64 = os.path.join(procdumpPath, 'procdump64.exe')
    if not os.path.isfile(procdump32) or not os.path.isfile(procdump64):
        choices = ['y','yes','Y','Yes','YES']
        choice = input("%sProcDump binaries have not been found. Do you want Spraykatz to download them? [y/N]" % (infoYellow)).lower()

        if choice in choices:
            url = 'https://download.sysinternals.com/files/Procdump.zip'
            wget.download(url, procdumpZip)
            with zipfile.ZipFile(procdumpZip, 'r') as zip_ref:
                zip_ref.extractall(procdumpPath)
            os.rename(os.path.join(procdumpPath, 'procdump.exe'), procdump32)
            os.remove(procdumpZip)
            logging.warning("\n")
        else:
            logging.warning("\n%sYou can manually download and put 'procdump32.exe' and 'procdump64.exe' into misc/procdump folder." % (warningRed))
            sys.exit(2)

def joinThreads(jobs, timeout):
    start = cur_time = time.time()

    while cur_time <= (start + int(timeout)):
        for job in jobs:
            if not job.is_alive():
                job.join()

        if all(not p.is_alive() for p in jobs):
            break
        else:
            time.sleep(1)
            cur_time = time.time()

    if cur_time >= int(timeout):
        for job in jobs:
            job.terminate()
            job.join()

    logging.debug("%sSpray threads terminated." % (debugBlue))

def freeSpraykatz(jobs, timeout):
    joinThreads(jobs, timeout)

def exit_gracefully(jobs, timeout):
    logging.warning("%sExiting Gracefully..." % (warningGre))
    freeSpraykatz(jobs, timeout)
