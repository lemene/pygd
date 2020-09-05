import os
import re
import subprocess

from . import cluster

class ClusterLocal(cluster.Cluster):
    name = "local"
    def __init__(self):
        self.version = ""
        pass

    def valid(self):
        return True

    def run(self):
        pass

    def submit(self, cmd):
        proc = subprocess.Popen(cmd,shell=True)
        return ProcessLocal(proc)
    
    def submit_script(self, script, threads, memeory, options):
        cmd = [script]
        cmd.append(options)
        cmd.append(" 2>&1 | tee %s.log" % script)

        proc = subprocess.Popen(cmd,shell=True)
        return ProcessLocal(proc)
        

class ProcessLocal (cluster.Process):
    def __init__(self, proc):
        self.proc = proc

    def status(self):
        r = self.proc.poll()
        if r == None:
            return "R"
        else:
            return "C"

    def stop(self):
        self.proc.stop();