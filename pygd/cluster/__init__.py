from .cluster_local import *
from .cluster_pbs import *


def create(sysname, nodesize):
        from . import cluster_local, cluster_pbs

        cluster_classes = [ClusterPbs, ClusterLocal ]

        for rcls in cluster_classes:
            print(rcls.name)
            if rcls.name == sysname or sysname == "auto":
                r = rcls()
                if r.valid():
                    return r
                else:
                    if rcls.name == sysname:
                        raise Exception("没有检测到 %s" % sysname)

        return None