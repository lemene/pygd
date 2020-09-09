import os.path
from .logger import logger


# name, ifiles, ofiles, gfiles, mfiles, cmds/func/jobs/pjobs, msg, prefunc, postfunc.
class Job(object):
    def __init__(self, pipeline, name, desc=""):
        self.pipeline = pipeline
        self.name = name
        self.ifiles = []
        self.ofiles = []
        self.gfiles = []
        self.mfiles = []
        self.prefunc = None
        self.postfunc = None
        self.description = desc
        
    def is_done(self):
        '''check whether the job was done'''
        done_fname = self.get_done_fname()
        print(done_fname)
        if not os.path.exists(done_fname):
            return False

        if self.get_done_value() == 0:
            return False

        if len(self.ifiles) == 0 or len(self.ofiles) == 0:
            return False

        if self.get_newest_mtime(self.ifiles) > self.get_oldest_mtime(self.ofiles + [done_fname]):
            return False

        return True

    def preprocess(self):
        logger.info("Start run job " + self.name)
        if self.prefunc != None:
            self.prefunc(self)

        if self.is_done():
            return True
        else:
            self.remove_done_file()
            return False
            
    def postprocess(self, skipped):
        pass

    def set_ifiles(self, ifiles):
        self.ifiles = ifiles

    def set_ofiles(self, ofiles):
        self.ofiles = ofiles

    def get_script_folder(self):
        return self.pipeline.get_script_folder()

    def get_script_fname(self):
        return os.path.join(self.get_script_folder(), self.name) + ".sh"

    def get_done_fname(self):
        return self.get_script_fname() + ".done"

    def get_log_fname(self):
        return self.get_script_fname() + ".log"

    def get_done_value(self):
        f = open(self.get_done_fname())
        value = f.readline().strip()
        if len(value) == 0:
            return -1
        else:
            return int(value)
            
    def set_done_value(self, value):
        f = open(self.get_done_fname(), "w")
        f.write("%d" % value)

    def remove_done_file(self):
        fname = self.get_done_fname()
        if os.path.exists(fname):
            os.remove(fname)

    def get_oldest_mtime(self, fnames):
        return min([os.path.getmtime(fn) for fn in fnames])

    def get_newest_mtime(self, fnames):
        return max([os.path.getmtime(fn) for fn in fnames])

    def run(self):
        skipped = self.preprocess()
        print("skipped", skipped)
        if not skipped:
            self.runcore()
        
        self.postprocess(skipped)

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
        self.set_done_value(0)

        


class ParallelJob(Job):
    def __init__(self):
        pass


class ScriptJob(Job):
    def __init__(self, pl, name, desc=""):
        super().__init__(pl, name, desc)
        self.commands = []

        
    def add_command(self, cmd):
        self.commands.append(cmd)


    def runcore(self):
        script_fname = self.get_script_fname()
        self.write(script_fname)
        self.pipeline.cluster.run_script(script_fname, 0, 0, "")

    def write(self, fname):
        ofile = open(fname, "w")
        ofile.write("#!/bin/bash\n\n")
        # ofile.write("env");
        ofile.write("retVal=0\n")
        for cmd in self.commands:
            ofile.write(self.wrap_command(cmd))
            ofile.write("\n")

        ofile.write("echo $retVal > %s\n" % self.get_done_fname())
        os.chmod(fname, 0o744)

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
