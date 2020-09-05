import os
import re
import subprocess


from .cluster import *

class ClusterPbs(Cluster):
    name = "pbs"
    def __init__(self):
        self.version = ""
        self.detect()


    def valid(self):
        return self.path != ""


    def sumbit_script(self, script, threads, memory, options):
        
        _, name = os.path.split(script)
        cmd = ["qsub -j oe"]
        cmd.append("-N %s" % name)
        if threads > 0: cmd.append("-l nodes=1:pnn=%d" % threads)
        if memory > 0: cmd.append("-l mem=%d" % memory)
        cmd.append("-o %s.log" % script)
        cmd.append(options)
        cmd.append(script)
        # TODO
        
        popen = subprocess.Popen(" ".join(cmd), stdout=subprocess.PIPE)
        popen.wait()
        lines = popen.stdout.readlines()
        
        return ProcessPbs(lines[0].decode("utf8").strip())

    def detect(self):
        self.path = os.popen("which pbsnodes 2> /dev/null").read()

        if not self.path == "":
            info = os.popen("pbsnodes --version 2>&1").read()

            for line in info.split("\n"):
                n = re.match(r"Version:\s+(.*)", line)
                if n:
                    self.version = n.group(1)

    

class ProcessPbs(Process):
    def __init__(self, jid):
        self.jid = jid