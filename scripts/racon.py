import sys, os

mydir, _ = os.path.split(os.path.abspath(__file__))
sys.path.append(mydir + "/..")

from pygd.pipeline import Pipeline
import pygd.job as pljob
import pygd.task as pltask

class PolishTask(pltask.Task):
    def __init__(self, pl):
        super().__init__(pl, "polish", "polish contigs with minimap2+racon")

    def preprocess(self, argv):
        if not os.path.exists("./scripts"):
            os.makedirs("./scripts")

        self.pipeline.configs.parse_argv(argv)
        self.add_job(self.job_polish())

    def job_polish(self):
        j = pljob.SerialJob(self.pipeline, "polish_all")
        rounds = self.pipeline.get_config("number-of-rounds", int)
        contigs = self.pipeline.get_config("contigs", str)

        for i in range(rounds):
            polished = os.path.join(self.pipeline.get_main_folder(), str(i), "polished.fasta")
            j.add_job(self.job_polish_one_round(i, contigs, polished))
            contigs = polished
            print(polished)

    
        return j

    def job_polish_one_round(self, i, contigs, polished):
        job = pljob.SerialJob(self.pipeline, "polish_" + str(i))
        folder = self.get_work_folder(i)
        rd2ctg = os.path.join(folder, "rd2ctg.paf")
        reads = self.pipeline.get_config("reads", str)

        job.add_job(self.job_minimap2(i, contigs, rd2ctg));
        #j.add_job(self.job_racon())
        return job

    def job_minimap2(self, i, contigs, rd2ctg):
        job = pljob.ScriptJob(self.pipeline, "minimap2_%d" % i)
        options = self.pipeline.get_config("minimap2_options", str)
        reads = self.pipeline.get_config("reads", str)
        job.add_command("minimap2 %s %s %s > %s" % (options, contigs, reads, rd2ctg))
        return job

    def job_racon(self):
        pass

    def job_split_reads(self, i, reads):
        j = pljob.ScriptJob(self, "split_reads_%d" % i )
        
        j.add_script(f"seqkit split2 -1 {reads}")

    def get_work_folder(self, i):
        return os.path.join(self.pipeline.get_main_folder(), str(i))

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
            ["number-of-rounds", 1],
            ["minimap2_options", "-x map-pb"],
            ["racon_options", ""]
        ])

        self.add_task(cmd.ConfigCommand(self))
        self.add_command(PolishCommand(self))

    def create_polish_job(self):
        pol_job = pljob.SerialJob(self, "polish_all")

    

if __name__ == "__main__":
    prj = RaconPipeline()
    prj.run(sys.argv[1:])