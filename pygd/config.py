import argparse

class Config(object):
    def __init__(self):
        self.configs = []
        self.index = {}

        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("--cfgfile", default="")

    def load(self, fname):
        '''从文件里面加载配置信息'''
        print("load")
        for line in open(fname):
            line = line.strip()
            if len(line) > 0 and line[0] != '#':
                items = [i.strip() for i in line.split('=')]
                self.set(items[0], items[1])
                print(items)


    def save(self, fname):
        '''将配置信息保存到文件'''

        file = open(fname, "w")
        for cfg in self.configs:

            if len(cfg) >= 3 and cfg[2] != "":
                file.write("# %s\n" % cfg[2])          
            file.write("%s = %s\n" % (cfg[0], cfg[1]))

    def parse_argv(self, argv):
        '''从参数得到配置信息'''
        args = self.parser.parse_args(argv)
        print(args.cfgfile)
        if args.cfgfile != "":
            self.load(args.cfgfile)
            
        #for item in self.configs:
        #    item[1] = getattr(args, item[0].replace("-", "_"))

    def set(self, name, value, desc=""):
        '''设置配置信息'''

        if name in self.index:
            self.configs[self.index[name]][1] = value
        else:
            self.index[name] = len(self.configs)
            self.configs.append([name, value, desc])
            self.parser.add_argument("--" + name, default=value, help=desc)

    def get(self, name, type):
        return type(self.configs[self.index[name]][1])