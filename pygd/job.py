import os.path
from .logger import logger


# name, ifiles, ofiles, gfiles, mfiles, cmds/func/jobs/pjobs, msg, prefunc, postfunc.
class Job(object):
    def __init__(self, pipeline, name, desc=""):
        self.pipeline = pipeline
        self.name = name
        self.ifname = []
        self.ofname = []
        self.prefunc = None
        self.postfunc = None
        self.description = desc
        
    def is_done(self):
        '''check whether the job was done'''
        done_fname = self.get_done_fname()
        if os.path.exists(done_fname):
            return False

        if len(self.ifname) == 0 or len(self.ofname) == 0:
            return False

        if self.get_newest_mtime(self.ifname) > self.get_oldest_mtime(self.ofname + [done_fname]):
            return False

        return True

    def preprocess(self):
        logger.info("Start run job " + self.name)
        if self.prefunc != None:
            self.prefunc(self)
            
    def postprocess(self, skipped):
        pass


    def get_script_folder(self):
        return "./scripts"

    def get_script_fname(self):
        return os.path.join(self.get_script_folder(), self.name) + ".sh"

    def get_done_fname(self):
        return self.get_script_fname() + ".done"

    def get_log_fname(self):
        return self.get_script_fname() + ".log"

    def get_done_value():pass
    def get_oldest_mtime(self, fnames):
        return min([os.path.getmtime(fn) for fn in fnames])

    def get_newest_mtime(self, fnames):
        return max([os.path.getmtime(fn) for fn in fnames])

    def run(self):
        self.preprocess()

        skipped = self.is_done()
        if not skipped:
            self.runcore()
        
        self.postprocess(self, skipped)

    def runcore(self):
        pass

class SerialJob(Job):
    def __init__(self, pipeline, name):
        super().__init__(pipeline, name)

        self.jobs = []

    def add_job(self, job):
        self.jobs.append(job)

    def runcore(self):
        for job in self.jobs:
            job.run()


class ParallelJob(Job):
    def __init__(self):
        pass


class ScriptJob(Job):
    def __init__(self, pl, name, desc=""):
        super().__init__(self, name, desc)
        self.commands = []

        
    def add_command(self, cmd):
        self.commands.append(cmd)


    def runcore(self):
        script_fname = self.get_script_fname()
        self.write(script_fname)
        pass

    def write(self, fname):
        ofile = open(fname, "w")
        ofile.write("#!/bin/bash\n\n")
        # ofile.write("env");
        ofile.write("retVal=0\n")
        for cmd in self.commands:
            ofile.write(self.wrap_command(cmd))
            ofile.write("\n")

        ofile.write("echo $retVal > %s\n" % self.get_done_fname())

    def wrap_command(self, cmd):
        codes = [
            "if [ $retVal -eq 0 ]; then",
            "  %s" % cmd,
            "  temp_result=(${PIPESTATUS[*]})",
            "  for i in ${temp_result[*]}",
            "  do",
            "    if [ $retVal -eq 0 ]; then",
            "      retVal=$i",
            "    else",
            "      break",
            "    fi",
            "  done",
            "fi"
        ]
        return "\n".join(codes)

class FunctionJob(Job):
    def __init__(self, pl):
        super().__init__(pl)
        pass
