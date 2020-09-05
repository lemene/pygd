import os
from .config import Config

class Pipeline(object):
    def __init__(self):
        self.configs = Config()
        self.eva = None
        self.runner = None

        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def set_default_configs(self, configs):
        for cfg in configs:
            self.configs.set(*cfg)

    def get_config(self, name, type):
        return self.configs.get(name, type)

    def load_config(self, fname):
        for line in open(fname):
            if line.strip().startswith("#"): continue

            name, value = line.split("=")

            self.configs[name.strip()] = value.strip()

    def run(self, argv):
        if len(argv) >= 1:
            for task in self.tasks:
                if task.name == argv[0]:
                    task.run(argv[1:])
                    break
            else:
                print("---");
        else:
            self.usage()

    def get_main_folder(self):
        return self.get_config("project", str)

    def get_script_folder(self):
        return os.path.join([self.get_main_folder(), "scripts"])

    def usage(self):
        for cmd in self.commands:
            cmd.usage()
