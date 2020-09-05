import sys

class Task(object):
    def __init__(self, pl, name, desc):
        self.pipeline = pl
        self.name = name
        self.description = desc

    def run(self, argv):
        self.preprocess(argv)
        self.runcore(argv)
        self.postprocess(argv)

    def preprocess(self, argv): pass
    def postprocess(self, argv): pass

    def usage(self):
        print("%s: %s" % (self.name, self.description), file=sys.stderr)


class ConfigTask(Task):
    def __init__(self, pl):
        super().__init__(pl, "config", "generate default config")

    def runcore(self, argv):
        fname = argv[0]
        
        self.pipeline.configs.save(fname)


class JobTask(Task):
    def __init__(self, pl, name, desc):
        super().__init__(pl, name, desc)
        self.jobs = []

    def runcore(self, argv):
        print(self.jobs)
        for job in self.jobs:
            job.run()

    def add_job(self, job):
        self.jobs.append(job)