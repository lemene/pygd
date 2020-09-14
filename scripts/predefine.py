import sys, os

mydir, _ = os.path.split(os.path.abspath(__file__))
sys.path.append(mydir + "/..")

from pygd.pipeline import Pipeline
import pygd.job as pljob
import pygd.task as pltask

class ExtractXJob(pljob.ScriptJob):
    def __init__(self, pipeline, name, ifname, ofname, )
