import os
import re
import subprocess
import time

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
        cmd = "%s %s 2>&1 | tee %s.log" % (script, options, script)

        proc = subprocess.Popen(cmd, shell=True)
        return ProcessLocal(proc)

    def run_script(self, script, threads, memory, options):
        proc = self.submit_script(script, threads, memory, options)
        proc.wait()
        

class ProcessLocal (cluster.Process):
    def __init__(self, proc):
        self.proc = proc

    def status(self):
        r = self.proc.poll()
        if r == None:
            return "R"
        else:
            return "C"

    def wait(self):
        r = self.status()
        while r != "C":
            time.sleep(10)
            r = self.status()


    def stop(self):
        self.proc.stop()