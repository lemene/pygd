import sys, os

mydir, _ = os.path.split(os.path.abspath(__file__))
sys.path.append(mydir + "/..")

from pygd.pipeline import Pipeline
import pygd.job as pljob
import pygd.task as pltask

class PolishTask(pltask.JobTask):
    def __init__(self, pl):
        super().__init__(pl, "polish", "polish contigs with minimap2+racon")

    def preprocess(self, argv):
        self.pipeline.configs.parse_argv(argv)

        if not os.path.exists(self.pipeline.get_main_folder()):
            os.makedirs(self.pipeline.get_main_folder())

        if not os.path.exists(self.pipeline.get_script_folder()):
            os.makedirs(self.pipeline.get_script_folder())

        self.add_job(self.pipeline.job_polish())



class RaconPipeline(Pipeline):
    def __init__(self):
        super().__init__()

        self.set_default_configs([
            ["project", ""],
            ["reads", ""],
            ["contigs", ""],
            ["threads", "4"],
            ["cleanup", "0"],
            ["grid_node", "0"],
            ["read_block_size", "4000000000"],
            ["contig_block_size", "500000000"],
            ["number_of_rounds", 1],
            ["minimap2_options", "-x map-pb"],
            ["racon_options", ""]
        ])

        self.add_task(pltask.ConfigTask(self))
        self.add_task(PolishTask(self))

    def job_polish(self):
        job = pljob.SerialJob(self, "polish_all")
        rounds = self.get_config("number_of_rounds", int)
        contigs = self.get_config("contigs", str)
        for i in range(rounds):
            polished = os.path.join(self.get_main_folder(), str(i), "polished.fasta")
            job.add_job(self.job_polish_one_round(i, contigs, polished))
            contigs = polished

        return job

    def job_polish_one_round(self, i, contigs, polished):
        job = pljob.SerialJob(self, "polish_" + str(i))
        folder = self.get_work_folder(i)
        rd2ctg = os.path.join(folder, "rd2ctg.paf")
        reads = self.get_config("reads", str)

        job.add_job(self.job_minimap2(i, contigs, rd2ctg))
        job.add_job(self.job_racon(i, contigs, reads, rd2ctg, polished))
        return job

    def job_minimap2(self, i, contigs, rd2ctg):
        options = self.get_config("minimap2_options", str)
        reads = self.get_config("reads", str)
        threads = self.get_config("threads", int)

        job = pljob.ScriptJob(self, "minimap2_%d" % i)
        job.set_ifiles([contigs, reads])
        job.set_ofiles([rd2ctg])
        job.add_command("mkdir -p %s" % self.get_work_folder(i))
        job.add_command("minimap2 -t %d %s %s %s > %s" % (threads, options, contigs, reads, rd2ctg))
        return job

    def job_racon(self, i, contigs, reads, rd2ctg, polished):
        options = self.get_config("racon_options", str)
        reads = self.get_config("reads", str)
        threads = self.get_config("threads", int)

        job = pljob.ScriptJob(self, "racon_%d" % i)
        job.set_ifiles([contigs, reads, rd2ctg])
        job.set_ofiles([polished])
        job.add_command("racon -t %d %s %s %s %s > %s" % (threads, options, reads, rd2ctg, contigs, polished))
        return job

    def job_split_reads(self, i, reads):
        j = pljob.ScriptJob(self, "split_reads_%d" % i )
        
 
    def get_work_folder(self, i):
        return os.path.join(self.get_main_folder(), str(i))

if __name__ == "__main__":
    prj = RaconPipeline()
    prj.run(sys.argv[1:])