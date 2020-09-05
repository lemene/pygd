import sys, os
import time
import argparse


mydir, _ = os.path.split(os.path.abspath(__file__))
sys.path.append(mydir + "/..")

import pygd.cluster as cluster
import pygd.logger as logger
import pygd.config as config



cfg = config.Config()
cfg.set("project", "", "project")
cfg.set("reads", "")

cfg.parse_argv(sys.argv[1:])



