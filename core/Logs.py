# coding: utf-8
# Author:	@aas_s3curity

# Imports
import sys, os, logging
from contextlib import contextmanager

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

@contextmanager
def suppress_std():
    old_logger = logging.getLogger().getEffectiveLevel()
    logging.getLogger().setLevel(logging.CRITICAL)
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = devnull
        sys.stderr = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            logging.getLogger().setLevel(old_logger)
