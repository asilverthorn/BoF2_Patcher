import logging, os
from log.format import *

import args
name, ext = os.path.splitext(args.output_file)
log_file = "{}{}".format(name, ".txt")
if args.stdout_log:
    import sys
    logging.basicConfig(stream = sys.stdout, filemode = 'w', level = logging.INFO, format = "%(message)s")
else:
    logging.basicConfig(filename = log_file, filemode = 'w', level = logging.INFO, format = "%(message)s")

import time
import version
log_msg =  f"Version   {version.__version__}\n"
log_msg += f"Generated {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
log_msg += f"Input     {os.path.basename(args.input_file)}\n"
log_msg += f"Output    {os.path.basename(args.output_file)}\n"
log_msg += f"Log       {os.path.basename(log_file)}\n"

if args.debug:
    log_msg += "\nDebug Mode"

logging.info(log_msg)

if not args.stdout_log:
    print(log_msg)

args.log()
